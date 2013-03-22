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

from oauth2client.client import OAuth2Credentials

import requests
import httplib2

#TODO: Switch to decimals
#from decimal import Decimal

from config import COINBASE_ENDPOINT
from models import CoinBaseAmount

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-03-22T09:31:19Z", "access_token": "7a12be33375feca0833a1a7195c974679e531938c84e52bd37fff4d816c0209c", "token_uri": "https://www.coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "7a12be33375feca0833a1a7195c974679e531938c84e52bd37fff4d816c0209c", "token_type": "bearer", "expires_in": 7200, "refresh_token": "0674ba503282d7c4992b72d9e2fc34e7405509f20d8a332d8560daeeb5a95955", "scope": "all"}, "client_id": "2df06cb383f4ffffac20e257244708c78a1150d128f37d420f11fdc069a914fc", "id_token": null, "client_secret": "7caedd79052d7e29aa0f2700980247e499ce85381e70e4a44de0c08f25bded8a", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "0674ba503282d7c4992b72d9e2fc34e7405509f20d8a332d8560daeeb5a95955", "user_agent": null}'''

class CoinBaseAccount(object):
    def __init__(self, oauth_credentials_json):

        self.oauth_credentials = OAuth2Credentials.from_json(oauth_credentials_json)
        self.http = httplib2.Http(disable_ssl_certificate_validation=True)

        if self.oauth_credentials.access_token_expired == True:
            print "Access_token expired"
            self.oauth_credentials.refresh(http=self.http)

        self.session = requests.session()
        self.oauth_credentials.apply(headers=self.session.headers)

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

#Models to create
###Transaction
###Sale
###User
###Contact
###Receive address?
###Amount with currency