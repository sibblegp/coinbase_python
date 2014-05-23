from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount
from . import account_setup
from .http_mocking import *


@with_http_mocking
class TransactionTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/transactions/'
                  '5158b227802669269c000009', response_body)

    def test_getting_transaction_with_oauth(self):
        account = account_setup.with_oauth()
        transaction = account.get_transaction('5158b227802669269c000009')
        this(transaction.status).should.equal('pending')
        this(transaction.amount).should.equal(CoinbaseAmount('-0.1', 'BTC'))


response_body = """
{
    "transaction": {
        "amount": {
            "amount": "-0.10000000",
            "currency": "BTC"
        },
        "created_at": "2013-03-31T15:01:11-07:00",
        "hsh":
"223a404485c39173ab41f343439e59b53a5d6cba94a02501fc6c67eeca0d9d9e",
        "id": "5158b227802669269c000009",
        "notes": "",
        "recipient_address": "15yHmnB5vY68sXpAU9pR71rnyPAGLLWeRP",
        "request": false,
        "sender": {
            "email": "gsibble@gmail.com",
            "id": "509e01ca12838e0200000212",
            "name": "gsibble@gmail.com"
        },
        "status": "pending"
    }
}
"""
