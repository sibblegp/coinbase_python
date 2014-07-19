from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseContact, CoinbaseTransaction
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
        this(transaction).should.equal(expected_transaction)


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
        "idem": "abcdef",
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


expected_transaction = CoinbaseTransaction(
    id='5158b227802669269c000009',
    status=CoinbaseTransaction.Status.pending,
    amount=CoinbaseAmount('-0.1', 'BTC'),
    hash='223a404485c39173ab41f343439e59b53a5d6cba94a02501fc6c67eeca0d9d9e',
    idem='abcdef',
    created_at=datetime(2013, 3, 31, 15, 1, 11,
                        tzinfo=tzoffset(None, -25200)),
    notes='',
    recipient_address='15yHmnB5vY68sXpAU9pR71rnyPAGLLWeRP',
    recipient_type='bitcoin',
    request=False,
    sender=CoinbaseContact(
        id='509e01ca12838e0200000212',
        email='gsibble@gmail.com',
        name='gsibble@gmail.com',
    ),
)
