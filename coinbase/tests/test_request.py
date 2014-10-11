from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseTransaction, CoinbaseContact
from . import account_setup
from .http_mocking import *


@with_http_mocking
class RequestTest(TestCase):

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/transactions/request_money',
                  response_body)

    def test_request_bitcoin_with_key(self):
        account = account_setup.with_key()
        transaction = account.request(**request_args)
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })
        this(transaction).should.equal(expected_transaction)

    def test_request_bitcoin_with_oauth(self):
        account = account_setup.with_oauth()
        transaction = account.request(**request_args)
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({})
        this(transaction).should.equal(expected_transaction)


request_args = {
    'from_email': 'alice@example.com',
    'amount': CoinbaseAmount('1', 'BTC'),
    'notes': 'Testing',
}


expected_request_json = {
    'transaction': {
        'from': 'alice@example.com',
        'amount': '1',
        'notes': 'Testing',
    }
}


response_body = """
{
    "success": true,
    "transaction": {
        "amount": {
            "amount": "1.00000000",
            "currency": "BTC"
        },
        "created_at": "2013-03-23T17:43:35-07:00",
        "hsh": null,
        "id": "96ab6e96f69a69c6d6960173",
        "notes": "Testing",
        "recipient": {
            "email": "bob@example.com",
            "id": "65ab697e5d67a58675675d31",
            "name": "bob@example.com"
        },
        "request": true,
        "sender": {
            "email": "alice@example.com",
            "id": "956df569c9ae67598a6c56e9",
            "name": "alice@example.com"
        },
        "status": "pending"
    }
}
"""


expected_transaction = CoinbaseTransaction(
    amount=CoinbaseAmount('1', 'BTC'),
    created_at=datetime(2013, 3, 23, 17, 43, 35,
                        tzinfo=tzoffset(None, -25200)),
    id='96ab6e96f69a69c6d6960173',
    notes='Testing',
    recipient=CoinbaseContact(
        id='65ab697e5d67a58675675d31',
        name='bob@example.com',
        email='bob@example.com',
    ),
    request=True,
    sender=CoinbaseContact(
        id='956df569c9ae67598a6c56e9',
        name='alice@example.com',
        email='alice@example.com',
    ),
    status=CoinbaseTransaction.Status.pending,
    recipient_type='coinbase',
)
