"""
Coinbase Python Client Library

AUTHOR

George Sibble
Github:  sibblegp


************TO USE************

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

from oauth2client.client import AccessTokenRefreshError, OAuth2Credentials

import requests
import httplib2
import json

#TODO: Switch to decimals from floats
#from decimal import Decimal

from config import COINBASE_ENDPOINT
from models import CoinBaseAmount, CoinBaseTransaction

class CoinBaseAccount(object):
    def __init__(self, api_key=None, oauth2_credentials=None):

        if oauth2_credentials:

            #Set our credentials
            self.oauth2_credentials = oauth2_credentials

            #Check our token and refresh if necessary
            self._check_oauth_expired()

            #Set up our session
            self.session = requests.session()

            #Apply our oAuth credentials to the session
            self.oauth2_credentials.apply(headers=self.session.headers)

            #Set our Content-Type
            self.session.headers.update({'content-type': 'application/json'})

        elif api_key:
            if api_key is type(str):
                #TODO:  Implement api_key version
                pass
            elif api_key is type(OAuth2Credentials):
                print "Please pass oAuth credentials into the oauth2_credentials parameter, not api_key"
            else:
                print "Your api_key must be a string"
        else:
            print "You must pass either an api_key or oauth_credentials"

    def _check_oauth_expired(self):
        if self.oauth2_credentials.access_token_expired == True:
            print 'oAuth2 Token Expired'
            self._refresh_oauth()

    def _refresh_oauth(self):
        #Set CA certificates (breaks without them)
        self.http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')

        #See if we can refresh the token
        try:
            #Ask to refresh the token
            self.oauth2_credentials.refresh(http=self.http)

            #We were successful
            print 'Your token was refreshed with the following response...'

            #Print the token for copy/paste
            print self.oauth2_credentials.to_json()

        #If the refresh token was invalid
        except AccessTokenRefreshError:

            print 'Your refresh token is invalid'
            raise AccessTokenRefreshError

    @property
    def balance(self):
        url = COINBASE_ENDPOINT + '/account/balance'
        response = self.session.get(url)
        results = response.json()
        return CoinBaseAmount(results['amount'], results['currency'])

    @property
    def receive_address(self):
        url = COINBASE_ENDPOINT + '/account/receive_address'
        response = self.session.get(url)
        return response.json()['address']

    @property
    def contacts(self):
        url = COINBASE_ENDPOINT + '/contacts'
        response = self.session.get(url)
        return [contact['contact'] for contact in response.json()['contacts']]

    def buy_price(self, qty=1):
        url = COINBASE_ENDPOINT + '/prices/buy'
        params = {'qty': qty}
        response = self.session.get(url, params=params)
        results = response.json()
        return CoinBaseAmount(results['amount'], results['currency'])

    def sell_price(self, qty=1):
        url = COINBASE_ENDPOINT + '/prices/sell'
        params = {'qty': qty}
        response = self.session.get(url, params=params)
        results = response.json()
        return CoinBaseAmount(results['amount'], results['currency'])

    @property
    def user(self):
        url = COINBASE_ENDPOINT + '/account/receive_address'
        response = self.session.get(url)
        return response.json()

    def request(self, from_email, amount, notes='', currency='BTC'):
        url = COINBASE_ENDPOINT + '/transactions/request_money'

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

        response = self.session.post(url=url, data=json.dumps(request_data))
        response_parsed = response.json()
        if response_parsed['success'] == False:
            pass
            #DO ERROR HANDLING and raise something

        return CoinBaseTransaction(response_parsed['transaction'])

    def send(self, to_address, amount, notes='', currency='BTC'):
        url = COINBASE_ENDPOINT + '/transactions/send_money'

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

        response = self.session.post(url=url, data=json.dumps(request_data))
        response_parsed = response.json()
        if response_parsed['success'] == False:
            pass
            #DO ERROR HANDLING and raise something

        return CoinBaseTransaction(response_parsed['transaction'])


    def transactions(self, count=30):
        url = COINBASE_ENDPOINT + '/transactions'
        pages = count / 30 + 1
        transactions = []

        reached_final_page = False

        for page in xrange(1, pages + 1):

            if not reached_final_page:
                params = {'page': page}
                response = self.session.get(url=url, params=params)
                parsed_transactions = response.json()

                if parsed_transactions['num_pages'] == page:
                    reached_final_page = True

                for transaction in parsed_transactions['transactions']:
                    transactions.append(CoinBaseTransaction(transaction['transaction']))

        return transactions

    def get_transaction(self, transaction_id):
        url = COINBASE_ENDPOINT + '/transactions/' + str(transaction_id)
        response = self.session.get(url)
        results = response.json()
        return CoinBaseTransaction(results['transaction'])

#Models to create
###Transaction
###Sale
###User
###Contact
###Receive address?
###Amount with currency