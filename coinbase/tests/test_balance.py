from sure import this
from unittest import TestCase

from coinbase.models import CoinbaseAmount
from coinbase.errors import UrlValueError

from . import account_setup
from .http_mocking import *


@with_http_mocking
class BalanceTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/account/balance',
                  response_body)

    def test_balance_with_key(self):
        account = account_setup.with_key()
        this(account.balance).should.equal(expected_balance)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key]
        })

    def test_balance_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.balance).should.equal(expected_balance)
        this(last_request_params()).should.equal({})


response_body = """
{
    "amount": "1.00000000",
    "currency": "BTC"
}
"""


expected_balance = CoinbaseAmount('1.0', 'BTC')


def test_url_injection_attempt():
    account = account_setup.with_oauth()
    this(lambda: account.get_order('../account/balance')) \
        .should.throw(UrlValueError)
