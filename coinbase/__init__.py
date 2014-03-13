"""
Coinbase Python Client Library

AUTHOR

George Sibble
Github:  sibblegp

LICENSE (The MIT License)

Copyright (c) 2013 George Sibble "gsibble@gmail.com"

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

__author__ = 'gsibble'

from oauth2client.client import AccessTokenRefreshError, OAuth2Credentials, AccessTokenCredentialsError

import requests
import httplib2
import json
import os
import inspect
from urllib import urlencode
import hashlib
import hmac
import time


from .config import COINBASE_ENDPOINT, COINBASE_ITEMS_PER_PAGE
from .models import CoinbaseAmount, CoinbaseTransaction, CoinbaseUser, CoinbaseTransfer, CoinbaseError, CoinbaseButton, CoinbaseOrder


class CoinbaseAccount(object):
    """
    Primary object for interacting with a Coinbase account

    You may either use oauth credentials or a classic API key
    """

    def __init__(self,
                 oauth2_credentials=None,
                 api_key=None, api_secret=None):
        """

        :param oauth2_credentials: JSON representation of Coinbase oauth2 credentials
        :param api_key:  Coinbase API key
        """

        #Set up our requests session
        self.session = requests.session()

        #Set our Content-Type
        self.session.headers.update({'content-type': 'application/json'})

        if oauth2_credentials:

            #CA Cert Path
            ca_directory = os.path.abspath(__file__).split('/')[0:-1]

            ca_path = '/'.join(ca_directory) + '/ca_certs.txt'

            #Set CA certificates (breaks without them)
            self.http = httplib2.Http(ca_certs=ca_path)

            #Create our credentials from the JSON sent
            self.oauth2_credentials = OAuth2Credentials.from_json(oauth2_credentials)

            #Check our token
            self.token_expired = False
            try:
                self._check_oauth_expired()
            except AccessTokenCredentialsError:
                self.token_expired = True

            #Apply our oAuth credentials to the session
            self.oauth2_credentials.apply(headers=self.session.headers)

            #Set our request parameters to be empty
            self.global_request_params = {}

        elif api_key and api_secret:
            if type(api_key) is str and type(api_secret) is str:
                #Set our API Key
                self.api_key = api_key
                self.api_secret = api_secret
            else:
                print "Your api_key and api_secret must be strings"
        else:
            print "You must pass either api_key and api_secret or oauth_credentials"

    def _check_oauth_expired(self):
        """
        Internal function to check if the oauth2 credentials are expired
        """

        #Check if they are expired
        if self.oauth2_credentials.access_token_expired == True:

            #Print an notification message if they are
            print 'oAuth2 Token Expired'

            #Raise the appropriate error
            raise AccessTokenCredentialsError

    def refresh_oauth(self):
        """
        Refresh our oauth2 token
        :return: JSON representation of oauth token
        :raise: AccessTokenRefreshError if there was an error refreshing the token
        """

        #See if we can refresh the token
        try:
            #Ask to refresh the token
            self.oauth2_credentials.refresh(http=self.http)

            #We were successful
            #print 'Your token was refreshed with the following response...'

            #Return the token for storage
            return self.oauth2_credentials

        #If the refresh token was invalid
        except AccessTokenRefreshError:

            #Print a warning
            print 'Your refresh token is invalid'

            #Raise the appropriate error
            raise AccessTokenRefreshError

    def _prepare_request(self):
        """
        Prepare our request in various ways
        """

        #Check if the oauth token is expired and refresh it if necessary
        self._check_oauth_expired()

    _get    = lambda self, url, data=None, params=None: self.make_request(self.session.get   , url, data, params)
    _post   = lambda self, url, data=None, params=None: self.make_request(self.session.post  , url, data, params)
    _put    = lambda self, url, data=None, params=None: self.make_request(self.session.put   , url, data, params)
    _delete = lambda self, url, data=None, params=None: self.make_request(self.session.delete, url, data, params)

    def make_request(self, request_func, url, data=None, params=None):
        # We need body as a string to compute the hmac signature
        body = json.dumps(data) if data else ''
        # We also need the full url, so we urlencode the params here
        url = COINBASE_ENDPOINT + url + ('?' + urlencode(params) if params else '')

        if hasattr(self, 'api_key'):
            nonce = str(int(time.time() * 1e6))

            message = nonce + url + body
            signature = hmac.new(self.api_secret, message, hashlib.sha256).hexdigest()
            self.session.headers.update({
                'ACCESS_KEY': self.api_key,
                'ACCESS_SIGNATURE': signature,
                'ACCESS_NONCE': nonce
            })

        response = request_func(url, data=body)
        response_parsed = response.json()

        if response.status_code != 200:
            if 'error' in response_parsed:
                raise CoinbaseError(response_parsed['error'])
            else:
                raise CoinbaseError('Response code not 200, was {}'.format(response.status_code))

        if 'success' in response_parsed and not response_parsed['success']:
            if 'error' in response_parsed:
                raise CoinbaseError(response_parsed['error'])
            elif 'errors' in response_parsed:
                raise CoinbaseError(response_parsed['errors'])
            else:
                raise CoinbaseError('Success was false in response, unknown error')

        return response_parsed


    @property
    def balance(self):
        """
        Retrieve coinbase's account balance

        :return: CoinbaseAmount with currency attribute
        """
        response_parsed = self._get('/account/balance')
        return CoinbaseAmount(response_parsed['amount'], response_parsed['currency'])

    @property
    def receive_address(self):
        """
        Get the account's current receive address

        :return: String address of account
        """
        response_parsed = self._get('/account/receive_address')
        return response_parsed['address']

    @property
    def contacts(self):
        """
        Get the account's contacts

        :return: List of contacts in the account
        """
        response_parsed = self._get('/contacts')
        return [contact['contact'] for contact in response_parsed['contacts']]

    def buy_price(self, qty=1):
        """
        Return the buy price of BitCoin in USD
        :param qty: Quantity of BitCoin to price
        :return: CoinbaseAmount with currency attribute
        """
        response_parsed = self._get('/prices/buy', params={"qty": qty})
        return CoinbaseAmount(response_parsed['amount'], response_parsed['currency'])

    def sell_price(self, qty=1):
        """
        Return the sell price of BitCoin in USD
        :param qty: Quantity of BitCoin to price
        :return: CoinbaseAmount with currency attribute
        """
        response_parsed = self._get('/prices/sell', params={"qty": qty})
        return CoinbaseAmount(response_parsed['amount'], response_parsed['currency'])

    def buy_btc(self, qty, pricevaries=False):
        """
        Buy BitCoin from Coinbase for USD
        :param qty: BitCoin quantity to be bought
        :param pricevaries: Boolean value that indicates whether or not the transaction should
                be processed if Coinbase cannot guarantee the current price.
        :return: CoinbaseTransfer with all transfer details on success or 
                 CoinbaseError with the error list received from Coinbase on failure
        """
        request_data = {
            "qty": qty,
            "agree_btc_amount_varies": pricevaries
        }
        response_parsed = self._post('/buys', data=json.dumps(request_data))
        return CoinbaseTransfer(response_parsed['transfer'])


    def sell_btc(self, qty):
        """
        Sell BitCoin to Coinbase for USD
        :param qty: BitCoin quantity to be sold
        :return: CoinbaseTransfer with all transfer details on success or 
                 CoinbaseError with the error list received from Coinbase on failure
        """
        response_parsed = self._post('/sells', data=json.dumps({"qty": qty}))
        return CoinbaseTransfer(response_parsed['transfer'])       


    def request(self, from_email, amount, notes='', currency='BTC'):
        """
        Request BitCoin from an email address to be delivered to this account
        :param from_email: Email from which to request BTC
        :param amount: Amount to request in assigned currency
        :param notes: Notes to include with the request
        :param currency: Currency of the request
        :return: CoinbaseTransaction with status and details
        """

        if currency == 'BTC':
            request_data = {
                "transaction": {
                    "from": from_email,
                    "amount": amount,
                    "notes": notes
                }
            }
        else:
            request_data = {
                "transaction": {
                    "from": from_email,
                    "amount_string": str(amount),
                    "amount_currency_iso": currency,
                    "notes": notes
                }
            }

        response_parsed = self._post('/transactions/request_money', data=json.dumps(request_data))
        return CoinbaseTransaction(response_parsed['transaction'])

    def send(self, to_address, amount, notes='', currency='BTC'):
        """
        Send BitCoin from this account to either an email address or a BTC address
        :param to_address: Email or BTC address to where coin should be sent
        :param amount: Amount of currency to send
        :param notes: Notes to be included with transaction
        :param currency: Currency to send
        :return: CoinbaseTransaction with status and details
        """

        if currency == 'BTC':
            request_data = {
                "transaction": {
                    "to": to_address,
                    "amount": amount,
                    "notes": notes
                }
            }
        else:

            request_data = {
                "transaction": {
                    "to": to_address,
                    "amount_string": str(amount),
                    "amount_currency_iso": currency,
                    "notes": notes
                }
            }

        response_parsed = self._post('/transactions/send_money', data=json.dumps(request_data))
        return CoinbaseTransaction(response_parsed['transaction'])


    def transactions(self, count=30):
        """
        Retrieve the list of transactions for the current account
        :param count: How many transactions to retrieve
        :return: List of CoinbaseTransaction objects
        """
        pages = count / 30 + 1
        transactions = []

        reached_final_page = False

        for page in xrange(1, pages + 1):

            if not reached_final_page:
                response_parsed = self._get('/transactions', params={'page': page})

                if response_parsed['num_pages'] == page:
                    reached_final_page = True

                for transaction in response_parsed['transactions']:
                    transactions.append(CoinbaseTransaction(transaction['transaction']))

        return transactions
    
    def transfers(self, count=30):
        """
        Retrieve the list of transfers for the current account
        :param count: How many transfers to retrieve
        :return: List of CoinbaseTransfer objects
        """
        pages = count / 30 + 1
        transfers = []

        reached_final_page = False

        for page in xrange(1, pages + 1):

            if not reached_final_page:
                response_parsed = self._get('/transfers', params={'page': page})

                if response_parsed['num_pages'] == page:
                    reached_final_page = True

                for transfer in response_parsed['transfers']:
                    transfers.append(CoinbaseTransfer(transfer['transfer']))

        return transfers

    def get_transaction(self, transaction_id):
        """
        Retrieve a transaction's details
        :param transaction_id: Unique transaction identifier
        :return: CoinbaseTransaction object with transaction details
        """
        response_parsed = self._get('/transactions/{id}'.format(id=transaction_id))
        return CoinbaseTransaction(response_parsed['transaction'])

    def get_user_details(self):
        """
        Retrieve the current user's details

        :return: CoinbaseUser object with user details
        """
        response_parsed = self._get('/users')

        user_details = response_parsed['users'][0]['user']

        #Convert our balance and limits to proper amounts
        balance = CoinbaseAmount(user_details['balance']['amount'], user_details['balance']['currency'])
        buy_limit = CoinbaseAmount(user_details['buy_limit']['amount'], user_details['buy_limit']['currency'])
        sell_limit = CoinbaseAmount(user_details['sell_limit']['amount'], user_details['sell_limit']['currency'])

        user = CoinbaseUser(user_id=user_details['id'],
                            name=user_details['name'],
                            email=user_details['email'],
                            time_zone=user_details['time_zone'],
                            native_currency=user_details['native_currency'],
                            balance=balance,
                            buy_level=user_details['buy_level'],
                            sell_level=user_details['sell_level'],
                            buy_limit=buy_limit,
                            sell_limit=sell_limit)

        return user

    def generate_receive_address(self, callback_url=None):
        """
        Generate a new receive address
        :param callback_url: The URL to receive instant payment notifications
        :return: The new string address
        """
        request_data = {
            "address": {
                "callback_url": callback_url
            }
        }
        response_parsed = self._post('/account/generate_receive_address', data=json.dumps(request_data))
        return response_parsed['address']

    def create_button(self, name,
                            price,
                            currency='BTC',
                            type=None,
                            style=None,
                            text=None,
                            description=None,
                            custom=None,
                            callback_url=None,
                            success_url=None,
                            cancel_url=None,
                            info_url=None,
                            variable_price=None,
                            choose_price=None,
                            include_address=None,
                            include_email=None,
                            price1=None, price2=None, price3=None, price4=None, price5=None):
        """
        Create a new button
        :param name: The name of the item for which you are collecting bitcoin.
        :param price: The price of the item
        :param currency: The currency to charge
        :param type: One of buy_now, donation, and subscription. Default is buy_now.
        :param style: One of buy_now_large, buy_now_small, donation_large, donation_small, subscription_large, subscription_small, custom_large, custom_small, and none. Default is buy_now_large. none is used if you plan on triggering the payment modal yourself using your own button or link.
        :param text: Allows you to customize the button text on custom_large and custom_small styles. Default is Pay With Bitcoin.
        :param description: Longer description of the item in case you want it added to the user's transaction notes.
        :param custom: An optional custom parameter. Usually an Order, User, or Product ID corresponding to a record in your database.
        :param callback_url: A custom callback URL specific to this button.
        :param success_url: A custom success URL specific to this button. The user will be redirected to this URL after a successful payment.
        :param cancel_url: A custom cancel URL specific to this button. The user will be redirected to this URL after a canceled order.
        :param info_url: A custom info URL specific to this button. Displayed to the user after a successful purchase for sharing.
        :param variable_price: Allow users to change the price on the generated button.
        :param choose_price: Show some suggested prices
        :param include_address: Collect shipping address from customer (not for use with inline iframes).
        :param include_email: Collect email address from customer (not for use with inline iframes).
        :param price1: Suggested price 1
        :param price2: Suggested price 2
        :param price3: Suggested price 3
        :param price4: Suggested price 4
        :param price5: Suggested price 5
        :return: A CoinbaseButton object
        """
        request_data = {
            "button": {
                "name": name,
                "price": str(price),
                "price_string": str(price),
                "currency": currency,
                "price_currency_iso": currency,
                "type": type,
                "style": style,
                "text": text,
                "description": description,
                "custom": custom,
                "callback_url": callback_url,
                "success_url": success_url,
                "cancel_url": cancel_url,
                "info_url": info_url,
                "variable_price": variable_price,
                "choose_price": choose_price,
                "include_address": include_address,
                "include_email": include_email,
                "price1": price1,
                "price2": price2,
                "price3": price3,
                "price4": price4,
                "price5": price5
            }
        }
        none_keys = [key for key in request_data['button'].keys() if request_data['button'][key] is None]
        for key in none_keys:
            del request_data['button'][key]

        response_parsed = self._post('/buttons', data=json.dumps(request_data))
        return CoinbaseButton(response_parsed['button'])

    def create_order(self, code):
        """
        Generate a new order from a button
        :param code: The code of the button for which you wish to create an order
        :return: A CoinbaseOrder object
        """
        response_parsed = self._post('/buttons/{code}/create_order'.format(code=code))
        return CoinbaseOrder(response_parsed['order'])

    def get_order(self, order_id):
        """
        Get an order by id
        :param order_id: The order id to be retrieved
        :return: A CoinbaseOrder object
        """
        response_parsed = self._get('/orders/{id}'.format(id=order_id))
        return CoinbaseOrder(response_parsed['order'])

    def orders(self, count=30):
        """
        Retrieve the list of orders for the current account
        :param count: How many orders to retrieve
        :return: List of CoinbaseOrder objects
        """
        pages = count / 30 + 1
        orders = []

        reached_final_page = False

        for page in xrange(1, pages + 1):

            if not reached_final_page:
                response_parsed = self._get('/orders', params={'page': page})

                if response_parsed['num_pages'] == page:
                    reached_final_page = True

                for order in response_parsed['orders']:
                    orders.append(CoinbaseOrder(order['order']))

        return orders
