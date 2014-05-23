from sure import this
from unittest import TestCase

from . import account_setup
from .http_mocking import *


@with_http_mocking
class TransactionListTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/transactions',
                  response_body)

    def test_transaction_list_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.transactions()).should.be.an(list)


response_body = """
{
    "balance": {
        "amount": "0.00000000",
        "currency": "BTC"
    },
    "current_page": 1,
    "current_user": {
        "email": "gsibble@gmail.com",
        "id": "509e01ca12838e0200000212",
        "name": "gsibble@gmail.com"
    },
    "num_pages": 1,
    "total_count": 4,
    "transactions": [
        {
            "transaction": {
                "amount": {
                    "amount": "1.00000000",
                    "currency": "BTC"
                },
                "created_at": "2013-03-23T17:43:35-07:00",
                "hsh": null,
                "id": "514e4c37802e1bf69100000e",
                "notes": "Testing",
                "recipient": {
                    "email": "gsibble@gmail.com",
                    "id": "509e01ca12838e0200000212",
                    "name": "gsibble@gmail.com"
                },
                "request": true,
                "sender": {
                    "email": "george@atlasr.com",
                    "id": "514e4c1c802e1bef9800001e",
                    "name": "george@atlasr.com"
                },
                "status": "pending"
            }
        },
        {
            "transaction": {
                "amount": {
                    "amount": "1.00000000",
                    "currency": "BTC"
                },
                "created_at": "2013-03-23T17:43:08-07:00",
                "hsh": null,
                "id": "514e4c1c802e1bef98000020",
                "notes": "Testing",
                "recipient": {
                    "email": "gsibble@gmail.com",
                    "id": "509e01ca12838e0200000212",
                    "name": "gsibble@gmail.com"
                },
                "request": true,
                "sender": {
                    "email": "george@atlasr.com",
                    "id": "514e4c1c802e1bef9800001e",
                    "name": "george@atlasr.com"
                },
                "status": "pending"
            }
        },
        {
            "transaction": {
                "amount": {
                    "amount": "-1.00000000",
                    "currency": "BTC"
                },
                "created_at": "2013-03-21T17:02:57-07:00",
                "hsh":
"42dd65a18dbea0779f32021663e60b1fab8ee0f859db7172a078d4528e01c6c8",
                "id": "514b9fb1b8377ee36500000d",
                "notes": "You gave me this a while ago.",
                "recipient": {
                    "email": "brian@coinbase.com",
                    "id": "4efec8d7bedd320001000003",
                    "name": "Brian Armstrong"
                },
                "recipient_address": "brian@coinbase.com",
                "request": false,
                "sender": {
                    "email": "gsibble@gmail.com",
                    "id": "509e01ca12838e0200000212",
                    "name": "gsibble@gmail.com"
                },
                "status": "complete"
            }
        },
        {
            "transaction": {
                "amount": {
                    "amount": "1.00000000",
                    "currency": "BTC"
                },
                "created_at": "2012-11-09T23:27:07-08:00",
                "hsh":
"ac9b0ffbe36dbe12c5ca047a5bdf9cadca3c9b89b74751dff83b3ac863ccc0b3",
                "id": "509e01cb12838e0200000224",
                "notes": "",
                "recipient": {
                    "email": "gsibble@gmail.com",
                    "id": "509e01ca12838e0200000212",
                    "name": "gsibble@gmail.com"
                },
                "recipient_address": "gsibble@gmail.com",
                "request": false,
                "sender": {
                    "email": "brian@coinbase.com",
                    "id": "4efec8d7bedd320001000003",
                    "name": "Brian Armstrong"
                },
                "status": "complete"
            }
        }
    ]
}
"""
