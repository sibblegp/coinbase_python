from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount
from . import account_setup
from .http_mocking import *


@with_http_mocking
class SendToEmailTest(TestCase):

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/transactions/send_money',
                  response_body)

    def test_send_bitcoin_to_email_address_with_key(self):
        account = account_setup.with_key()
        tx = account.send(to_address='bob@example.com',
                          amount=CoinbaseAmount('0.1', 'BTC'))
        this(tx.recipient.email).should.equal('bob@example.com')


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
