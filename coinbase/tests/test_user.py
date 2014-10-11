from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount
from . import account_setup
from .http_mocking import *


@with_http_mocking
class UserTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/users', response_body)

    def test_getting_user_details_with_oauth(self):
        account = account_setup.with_oauth()
        user = account.get_user_details()
        this(user.id).should.equal("509f01da12837e0201100212")
        this(user.balance).should.equal(CoinbaseAmount('1225.86084181', 'BTC'))


response_body = """
{
    "users": [
        {
            "user": {
                "balance": {
                    "amount": "1225.86084181",
                    "currency": "BTC"
                },
                "buy_level": 1,
                "buy_limit": {
                    "amount": "10.00000000",
                    "currency": "BTC"
                },
                "email": "gsibble@gmail.com",
                "id": "509f01da12837e0201100212",
                "name": "New User",
                "native_currency": "USD",
                "sell_level": 1,
                "sell_limit": {
                    "amount": "50.00000000",
                    "currency": "BTC"
                },
                "time_zone": "Pacific Time (US & Canada)"
            }
        }
    ]
}
"""
