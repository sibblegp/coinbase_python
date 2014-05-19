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

from oauth2client.client import AccessTokenRefreshError, OAuth2Credentials, \
    AccessTokenCredentialsError

import requests
import httplib2
import json
import os
import re

from decimal import Decimal

from coinbase.config import COINBASE_ENDPOINT
from coinbase.models import *
from coinbase.errors import *


url_path_component_regex = re.compile('^[0-9a-z_\-]+$', re.I)


def coinbase_url(*args):

    args = map(str, args)

    # make sure we don't concatenate anything too weird into the url
    for c in args:
        if not url_path_component_regex.match(c):
            raise UrlValueError(c)

    return '/'.join([COINBASE_ENDPOINT] + args)


class CoinbaseAccount(object):
    """
    Primary object for interacting with a Coinbase account

    You may use oauth credentials, a classic API key, or
    no auth (for unauthenticated resources only)
    """

    def __init__(self, oauth2_credentials=None, api_key=None,
                 allow_transfers=True):
        """
        :param oauth2_credentials: JSON representation of Coinbase oauth2
                credentials
        :param api_key:  Coinbase API key
        :param allow_transfers: Whether to allow sending money.
                You can set this to False for safety while in a development
                environment if you want to more sure you don't actually send
                any money around.
        """

        self.allow_transfers = allow_transfers

        #Set up our requests session
        self.session = requests.session()

        #Set our Content-Type
        self.session.headers.update({'content-type': 'application/json'})

        self.authenticated = bool(oauth2_credentials or api_key)

        if oauth2_credentials:

            #CA Cert Path
            ca_directory = os.path.abspath(__file__).split('/')[0:-1]

            ca_path = '/'.join(ca_directory) + '/ca_certs.txt'

            #Set CA certificates (breaks without them)
            self.http = httplib2.Http(ca_certs=ca_path)

            #Create our credentials from the JSON sent
            self.oauth2_credentials = \
                OAuth2Credentials.from_json(oauth2_credentials)

            #Check our token
            self.token_expired = False
            try:
                self._check_oauth_expired()
            except AccessTokenCredentialsError:
                self.token_expired = True

            #Apply our oAuth credentials to the session
            self.oauth2_credentials.apply(headers=self.session.headers)

            #Set our request parameters to be empty
            self.auth_params = {}

        elif api_key:
            #Set our API Key
            self.api_key = api_key

            #Set our auth_params
            self.auth_params = {'api_key': api_key}

    def _require_allow_transfers(self):
        if not self.allow_transfers:
            raise Exception('Transfers are not enabled')

    def _require_authentication(self):
        if not self.authenticated:
            raise Exception('Authentication credentials required')

    def _check_oauth_expired(self):
        """
        Internal function to check if the oauth2 credentials are expired
        """

        #Check if they are expired
        if self.oauth2_credentials.access_token_expired:

            #Print an notification message if they are
            print 'oAuth2 Token Expired'

            #Raise the appropriate error
            raise AccessTokenCredentialsError

    def refresh_oauth(self):
        """
        Refresh our oauth2 token
        :return: JSON representation of oauth token
        :raise: AccessTokenRefreshError if there was an error refreshing the
                token
        """

        #See if we can refresh the token
        try:
            #Ask to refresh the token
            self.oauth2_credentials.refresh(http=self.http)

            #We were successful

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

    @property
    def balance(self):
        """
        Retrieve coinbase's account balance

        :return: CoinbaseAmount with currency attribute
        """
        self._require_authentication()

        url = coinbase_url('account', 'balance')
        response = self.session.get(url, params=self.auth_params)
        return CoinbaseAmount.from_coinbase_dict(response.json())

    @property
    def receive_address(self):
        """
        Get the account's current receive address

        :return: String address of account
        """
        self._require_authentication()

        url = coinbase_url('account', 'receive_address')
        response = self.session.get(url, params=self.auth_params)
        return response.json()['address']

    def contacts(self, page=None, limit=None, query=None):
        """
        Contacts the user has previously sent to or received from.

        :param page: Can be used to page through results. Default value is 1.
        :param limit: Number of records to return. Maximum is 1000. Default
                      value is 25.
        :param query: Optional partial string match to filter contacts.

        :return: list of CoinbaseContact
        """
        self._require_authentication()

        url = coinbase_url('contacts')

        params = {}
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if query is not None:
            params['query'] = query
        params.update(self.auth_params)

        response = self.session.get(url, params=params)
        return [CoinbaseContact.from_coinbase_dict(x['contact'])
                for x in response.json()['contacts']]

    def buy_price(self, qty=1):
        """
        Return the buy price of BitCoin in USD
        :param qty: Quantity of BitCoin to price
        :return: CoinbaseAmount with currency attribute
        """
        url = coinbase_url('prices', 'buy')
        params = {'qty': qty}
        response = self.session.get(url, params=params)
        results = response.json()
        return CoinbaseAmount.from_coinbase_dict(results)

    def sell_price(self, qty=1):
        """
        Return the sell price of BitCoin in USD
        :param qty: Quantity of BitCoin to price
        :return: CoinbaseAmount with currency attribute
        """
        url = coinbase_url('prices', 'sell')
        params = {'qty': qty}
        response = self.session.get(url, params=params)
        results = response.json()
        return CoinbaseAmount.from_coinbase_dict(results)

    def buy_btc(self, qty, pricevaries=False):
        """
        Buy BitCoin from Coinbase for USD
        :param qty: BitCoin quantity to be bought
        :param pricevaries: Boolean value that indicates whether or not the
                transaction should be processed if Coinbase cannot guarantee
                the current price.
        :return: CoinbaseTransfer with all transfer details on success
        :raise: CoinbaseError with the error list received from Coinbase on
                 failure
        """
        self._require_allow_transfers()
        self._require_authentication()

        url = coinbase_url('buys')
        request_data = {
            "qty": qty,
            "agree_btc_amount_varies": pricevaries
        }
        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        response_parsed = response.json()
        if not response_parsed.get('success'):
            raise CoinbaseError('Failed to buy btc.',
                                response_parsed.get('errors'))

        return CoinbaseTransfer.from_coinbase_dict(response_parsed['transfer'])

    def sell_btc(self, qty):
        """
        Sell BitCoin to Coinbase for USD
        :param qty: BitCoin quantity to be sold
        :return: CoinbaseTransfer with all transfer details on success
        :raise: CoinbaseError with the error list received from Coinbase on
                 failure
        """
        self._require_allow_transfers()
        self._require_authentication()

        url = coinbase_url('sells')
        request_data = {
            "qty": qty,
        }
        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        response_parsed = response.json()
        if not response_parsed.get('success'):
            raise CoinbaseError('Failed to sell btc.',
                                response_parsed.get('errors'))

        return CoinbaseTransfer.from_coinbase_dict(response_parsed['transfer'])

    def request(self, from_email, amount, notes=''):
        """
        Request BitCoin from an email address to be delivered to this account
        :param from_email: Email from which to request BTC
        :param amount: Amount to request (CoinbaseAmount)
        :param notes: Notes to include with the request
        :return: CoinbaseTransaction with status and details
        :raise: CoinbaseError with the error list received from Coinbase on
                 failure
        """
        self._require_allow_transfers()
        self._require_authentication()

        url = coinbase_url('transactions', 'request_money')

        request_data = {
            'transaction': {
                'from': from_email,
                'notes': notes,
            },
        }

        if amount.currency == 'BTC':
            request_data['transaction']['amount'] = str(amount.amount)
        else:
            request_data['transaction']['amount_string'] = str(amount.amount)
            request_data['transaction']['amount_currency_iso'] = amount.currency

        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        response_parsed = response.json()
        if not response_parsed.get('success'):
            raise CoinbaseError('Failed to request btc.',
                                response_parsed.get('errors'))

        return CoinbaseTransaction \
            .from_coinbase_dict(response_parsed['transaction'])

    def send(self, to_address, amount, notes=''):
        """
        Send BitCoin from this account to either an email address or a BTC
        address
        :param to_address: Email or BTC address to where coin should be sent
        :param amount: Amount of currency to send (CoinbaseAmount)
        :param notes: Notes to be included with transaction
        :return: CoinbaseTransaction with status and details
        :raise: CoinbaseError with the error list received from Coinbase on
                 failure
        """
        self._require_allow_transfers()
        self._require_authentication()

        url = coinbase_url('transactions', 'send_money')

        request_data = {
            'transaction': {
                'to': to_address,
                'amount': amount,
                'notes': notes,
            },
        }

        if amount.currency == 'BTC':
            request_data['transaction']['amount'] =  str(amount.amount)
        else:
            request_data['transaction']['amount_string'] = str(amount.amount)
            request_data['transaction']['amount_currency_iso'] = amount.currency

        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        response_parsed = response.json()

        if not response_parsed.get('success'):
            raise CoinbaseError('Failed to send btc.',
                                response_parsed.get('errors'))

        return CoinbaseTransaction \
            .from_coinbase_dict(response_parsed['transaction'])

    def transactions(self, count=30):
        """
        Retrieve the list of transactions for the current account
        :param count: How many transactions to retrieve
        :return: List of CoinbaseTransaction objects
        """
        self._require_authentication()

        url = coinbase_url('transactions')
        pages = count / 30 + 1
        transactions = []

        reached_final_page = False

        for page in xrange(1, pages + 1):

            if not reached_final_page:
                params = {'page': page}
                params.update(self.auth_params)
                response = self.session.get(url=url, params=params)
                parsed_transactions = response.json()

                if parsed_transactions['num_pages'] == page:
                    reached_final_page = True

                for transaction in parsed_transactions['transactions']:
                    tx = CoinbaseTransaction \
                        .from_coinbase_dict(transaction['transaction'])
                    transactions.append(tx)

        return transactions

    def transfers(self, count=30):
        """
        Retrieve the list of transfers for the current account
        :param count: How many transfers to retrieve
        :return: List of CoinbaseTransfer objects
        """
        self._require_authentication()

        url = coinbase_url('transfers')
        pages = count / 30 + 1
        transfers = []

        reached_final_page = False

        for page in xrange(1, pages + 1):

            if not reached_final_page:
                params = {'page': page}
                params.update(self.auth_params)
                response = self.session.get(url=url, params=params)
                parsed_transfers = response.json()

                if parsed_transfers['num_pages'] == page:
                    reached_final_page = True

                for transfer in parsed_transfers['transfers']:
                    transfers.append(CoinbaseTransfer
                                     .from_coinbase_dict(transfer['transfer']))

        return transfers

    def get_transaction(self, transaction_id):
        """
        Retrieve a transaction's details
        :param transaction_id: Unique transaction identifier
        :return: CoinbaseTransaction object with transaction details
        """
        self._require_authentication()

        url = coinbase_url('transactions', transaction_id)
        response = self.session.get(url, params=self.auth_params)
        results = response.json()

        if not results.get('success', True):
            pass
            #TODO:  Add error handling

        return CoinbaseTransaction.from_coinbase_dict(results['transaction'])

    def get_user_details(self):
        """
        Retrieve the current user's details

        :return: CoinbaseUser object with user details
        """
        self._require_authentication()

        url = coinbase_url('users')
        response = self.session.get(url, params=self.auth_params)
        results = response.json()

        return CoinbaseUser.from_coinbase_dict(results['users'][0]['user'])

    def generate_receive_address(self, callback_url=None):
        """
        Generate a new receive address
        :param callback_url: The URL to receive instant payment notifications
        :return: The new string address
        """
        self._require_authentication()

        url = coinbase_url('account', 'generate_receive_address')
        request_data = {
            'address': {
                'callback_url': callback_url
            }
        }
        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        return response.json()['address']

    def create_button(self, button, account_id=None):
        """
        Create a new payment button, page, or iframe.

        See https://coinbase.com/api/doc/1.0/buttons/create.html for details.

        :param button: CoinbasePaymentButton
        :param account_id: Specify for which account is the button created.
                           The default is your primary account.
        :return: CoinbasePaymentButton (which should have the same attributes
                 as the one given, except now it has an ID generated by
                 Coinbase)
        """
        self._require_authentication()

        url = coinbase_url('buttons')

        request_data = {
            'button': button.to_coinbase_dict()
        }

        if account_id is not None:
            request_data['account_id'] = account_id

        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        resp_data = response.json()
        if not resp_data.get('success') or 'button' not in resp_data:
            error_msg = 'Error creating button'
            if 'errors' in resp_data:
                error_msg += ':' + u'\n'.join(resp_data)
            else:
                error_msg += '.'
            raise RuntimeError(error_msg)

        return CoinbasePaymentButton.from_coinbase_dict(resp_data['button'])

    @property
    def exchange_rates(self):
        """
        Retrieve BTC to fiat (and vice versus) exchange rates in various
        currencies. It has keys for both btc_to_xxx and xxx_to_btc.
        :return: Dict with str keys and Decimal values
        """
        url = coinbase_url('currencies', 'exchange_rates')
        rates = json.loads(requests.get(url).content)
        return dict(((k, Decimal(v)) for k, v in rates.iteritems()))

    def orders(self, account_id=None, page=None):
        """
        Returns a merchant's orders that they have received.
        Sorted by created_at in descending order.

        :param account_id: Specify which account is used for fetching data.
        The default is your primary account.
        :param page: Can be used to page through results. Default is 1.
        :return: List of CoinbaseOrder
        """
        self._require_authentication()

        url = coinbase_url('orders')

        params = {}
        if account_id is not None:
            params['account_id'] = account_id
        if page is not None:
            params['page'] = page
        params.update(self.auth_params)

        response = self.session.get(url=url, params=params)
        return map(CoinbaseOrder.from_coinbase_dict, response.json()['orders'])

    def get_order(self, id_or_custom_field, account_id=None):
        self._require_authentication()

        url = coinbase_url('orders', id_or_custom_field)

        params = {}
        if account_id is not None:
            params['account_id'] = account_id
        params.update(self.auth_params)

        response = self.session.get(url=url, params=params)
        return CoinbaseOrder.from_coinbase_dict(response.json())

    def create_button_and_order(self, button):
        self._require_authentication()

        url = coinbase_url('orders')

        request_data = {
            'button': button.to_coinbase_dict()
        }

        response = self.session.post(url=url, data=json.dumps(request_data),
                                     params=self.auth_params)
        return CoinbaseOrder.from_coinbase_dict(response.json())

    def create_order_from_button(self, button_id):
        self._require_authentication()

        url = coinbase_url('buttons', button_id, 'create_order')

        response = self.session.post(url=url, params=self.auth_params)
        return CoinbaseOrder.from_coinbase_dict(response.json())
