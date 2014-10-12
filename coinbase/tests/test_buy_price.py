from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount
from . import account_setup
from .http_mocking import *


@with_http_mocking
class BuyPriceTest1(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/prices/buy',
                  self.response_body)

    def test_buy_price_without_auth(self):
        self.go(account_setup.without_auth())

    def test_buy_price_with_key(self):
        self.go(account_setup.with_key())

    def test_buy_price_with_oauth(self):
        self.go(account_setup.with_oauth())

    def go(self, account):
        this(account.buy_price()).should.equal(self.expected_price)
        params = last_request_params()
        params.pop('api_key', None)
        this(params).should.equal({'qty': ['1']})

    response_body = """
    {
        "amount": "63.31",
        "currency": "USD"
    }
    """

    expected_price = CoinbaseAmount('63.31', 'USD')


@with_http_mocking
class BuyPriceTest2(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/prices/buy',
                  self.response_body)

    def test_buy_price_without_auth(self):
        self.go(account_setup.without_auth())

    def test_buy_price_with_key(self):
        self.go(account_setup.with_key())

    def test_buy_price_with_oauth(self):
        self.go(account_setup.with_oauth())

    def go(self, account):
        this(account.buy_price('10')).should.equal(self.expected_price)
        params = last_request_params()
        params.pop('api_key', None)
        this(params).should.equal({'qty': ['10']})

    response_body = """
    {
        "amount": "633.25",
        "currency": "USD"
    }
    """

    expected_price = CoinbaseAmount('633.25', 'USD')
