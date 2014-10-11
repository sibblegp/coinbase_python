from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseContact, CoinbaseTransaction
from . import account_setup
from .http_mocking import *


@with_http_mocking
class SendBtcToEmailTest(TestCase):

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/transactions/send_money',
                  response_body)

    def test_send_btc_to_email_address_with_key(self):
        account = account_setup.with_key()
        tx = account.send(
            to_address='bob@example.com',
            amount=CoinbaseAmount('0.1', 'BTC'),
        )
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })
        this(tx).should.equal(expected_transaction)

    def test_send_btc_to_email_address_with_oauth(self):
        account = account_setup.with_oauth()
        tx = account.send(
            to_address='bob@example.com',
            amount=CoinbaseAmount('0.1', 'BTC'),
        )
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({})
        this(tx).should.equal(expected_transaction)


expected_request_json = {
    'transaction': {
        'to': 'bob@example.com',
        'amount': '0.1',
        'notes': '',
    }
}


response_body = """
{
    "success": true,
    "transaction": {
        "amount": {
            "amount": "-0.10000000",
            "currency": "BTC"
        },
        "created_at": "2013-03-31T15:02:58-07:00",
        "hsh": null,
        "id": "69ab532bde59cfba595c5738",
        "notes": "",
        "idem": "",
        "recipient": {
            "email": "bob@example.com",
            "id": "72370bd60efa506c6596d56e",
            "name": "Bob"
        },
        "recipient_address": "bob@example.com",
        "request": false,
        "sender": {
            "email": "alice@example.com",
            "id": "016bde60ac5603bde5300011",
            "name": "alice@example.com"
        },
        "status": "pending"
    }
}
"""


expected_transaction = CoinbaseTransaction(
    id='69ab532bde59cfba595c5738',
    created_at=datetime(2013, 3, 31, 15, 2, 58,
                        tzinfo=tzoffset(None, -25200)),
    notes='',
    amount=CoinbaseAmount('-0.1', 'BTC'),
    status=CoinbaseTransaction.Status.pending,
    request=False,
    sender=CoinbaseContact(
        id='016bde60ac5603bde5300011',
        email='alice@example.com',
        name='alice@example.com',
    ),
    recipient=CoinbaseContact(
        id='72370bd60efa506c6596d56e',
        email='bob@example.com',
        name='Bob',
    ),
    recipient_address='bob@example.com',
    recipient_type='coinbase',
)
