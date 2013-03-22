__author__ = 'gsibble'

import sure
from sure import it, this, those, these
import unittest

from coinbase import CoinBaseAccount
from models import CoinBaseAmount

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-03-22T09:31:19Z", "access_token": "7a12be33375feca0833a1a7195c974679e531938c84e52bd37fff4d816c0209c", "token_uri": "https://www.coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "7a12be33375feca0833a1a7195c974679e531938c84e52bd37fff4d816c0209c", "token_type": "bearer", "expires_in": 7200, "refresh_token": "0674ba503282d7c4992b72d9e2fc34e7405509f20d8a332d8560daeeb5a95955", "scope": "all"}, "client_id": "2df06cb383f4ffffac20e257244708c78a1150d128f37d420f11fdc069a914fc", "id_token": null, "client_secret": "7caedd79052d7e29aa0f2700980247e499ce85381e70e4a44de0c08f25bded8a", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "0674ba503282d7c4992b72d9e2fc34e7405509f20d8a332d8560daeeb5a95955", "user_agent": null}'''

class CoinBaseTests(unittest.TestCase):

    def setUp(self):
        self.account = CoinBaseAccount(TEMP_CREDENTIALS)

    def test_retrieve_balance(self):
        this(self.account.balance).should.equal(0.0)
        this(self.account.balance.currency).should.equal('BTC')

        #TODO:  Switch to decimals
        #this(self.account.balance).should.equal(CoinBaseAmount('0.00000000', 'USD'))
        #this(self.account.balance.currency).should.equal(CoinBaseAmount('0.00000000', 'USD').currency)

    def test_receive_addresses(self):
        this(self.account.receive_address).should.equal(u'1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt')

    def test_contacts(self):
        this(self.account.contacts).should.equal([{u'email': u'brian@coinbase.com'}])

    def test_buy_price(self):
        buy_price_1 = self.account.buy_price(1)
        this(buy_price_1).should.be.an(float)
        this(buy_price_1.currency).should.equal('USD')

        buy_price_10 = self.account.buy_price(10)
        this(buy_price_10).should.be.greater_than(buy_price_1 * 9.8)

    def test_sell_price(self):
        sell_price_1 = self.account.sell_price(1)
        this(sell_price_1).should.be.an(float)
        this(sell_price_1.currency).should.equal('USD')

        buy_price_10 = self.account.sell_price(10)
        this(buy_price_10).should.be.greater_than(sell_price_1 * 9.8)