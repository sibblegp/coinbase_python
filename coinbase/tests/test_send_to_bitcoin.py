from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount
from . import account_setup
from .http_mocking import *


@with_http_mocking
class SendToBitcoinTest(TestCase):

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/transactions/send_money',
                  response_body)

    def test_send_bitcoin_to_btc_address_with_key(self):
        account = account_setup.with_key()
        tx = account.send(to_address='7nregFERfhn8f34FERf8yn8fEGgfe274nv',
                          amount=CoinbaseAmount('0.1', 'BTC'))
        this(tx.amount).should.equal(CoinbaseAmount('-0.1', 'BTC'))
        this(tx.request).should.equal(False)
        this(tx.sender.email).should.equal('alice@example.com')
        this(tx.recipient).should.equal(None)
        this(tx.recipient_address).should.equal(
            '7nregFERfhn8f34FERf8yn8fEGgfe274nv')


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
