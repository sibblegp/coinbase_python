from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseContact, CoinbaseTransaction
from . import account_setup
from .http_mocking import *


@with_http_mocking
class SendBtcToBitcoinTest(TestCase):

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/transactions/send_money',
                  response_body)

    def test_send_btc_to_bitcoinaddress_with_key(self):
        account = account_setup.with_key()
        tx = account.send(
            to_address='7nregFERfhn8f34FERf8yn8fEGgfe274nv',
            amount=CoinbaseAmount('0.1', 'BTC'),
            idem='abc',
        )
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })
        this(tx).should.equal(expected_transaction)

    def test_send_btc_to_bitcoin_address_with_oauth(self):
        account = account_setup.with_oauth()
        tx = account.send(
            to_address='7nregFERfhn8f34FERf8yn8fEGgfe274nv',
            amount=CoinbaseAmount('0.1', 'BTC'),
            idem='abc',
        )
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({})
        this(tx).should.equal(expected_transaction)


expected_request_json = {
    'transaction': {
        'to': '7nregFERfhn8f34FERf8yn8fEGgfe274nv',
        'amount': '0.1',
        'notes': '',
        'idem': 'abc',
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
        "created_at": "2013-03-31T15:01:11-07:00",
        "hsh": null,
        "id": "760n6abc6790e6bd67e6ba50",
        "notes": "",
        "idem": "abc",
        "recipient_address": "7nregFERfhn8f34FERf8yn8fEGgfe274nv",
        "request": false,
        "sender": {
            "email": "alice@example.com",
            "id": "701bdfea6f6e1062b6823532",
            "name": "alice@example.com"
        },
        "status": "pending"
    }
}
"""


expected_transaction = CoinbaseTransaction(
    id='760n6abc6790e6bd67e6ba50',
    created_at=datetime(2013, 3, 31, 15, 1, 11,
                        tzinfo=tzoffset(None, -25200)),
    notes='',
    idem='abc',
    amount=CoinbaseAmount('-0.1', 'BTC'),
    status=CoinbaseTransaction.Status.pending,
    request=False,
    sender=CoinbaseContact(
        id='701bdfea6f6e1062b6823532',
        email='alice@example.com',
        name='alice@example.com',
    ),
    recipient_address='7nregFERfhn8f34FERf8yn8fEGgfe274nv',
    recipient_type='bitcoin',
)
