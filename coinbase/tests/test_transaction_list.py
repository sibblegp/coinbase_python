from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseContact, CoinbaseTransaction
from . import account_setup
from .http_mocking import *


@with_http_mocking
class TransactionListTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/transactions',
                  response_body)

    def test_transaction_list_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.transactions()).should.equal(expected_transactions)


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
                "idem": "",
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
                "idem": "",
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
                "idem": "jkl",
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
                "idem": "xyz",
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


expected_transactions = [
    CoinbaseTransaction(
        amount=CoinbaseAmount('1', 'BTC'),
        created_at=datetime(2013, 3, 23, 17, 43, 35,
                            tzinfo=tzoffset(None, -25200)),
        id='514e4c37802e1bf69100000e',
        notes='Testing',
        recipient=CoinbaseContact(
            id='509e01ca12838e0200000212',
            email='gsibble@gmail.com',
            name='gsibble@gmail.com',
        ),
        recipient_type='coinbase',
        request=True,
        sender=CoinbaseContact(
            id='514e4c1c802e1bef9800001e',
            email='george@atlasr.com',
            name='george@atlasr.com',
        ),
        status=CoinbaseTransaction.Status.pending,
    ),
    CoinbaseTransaction(
        amount=CoinbaseAmount('1', 'BTC'),
        created_at=datetime(2013, 3, 23, 17, 43, 8,
                            tzinfo=tzoffset(None, -25200)),
        id='514e4c1c802e1bef98000020',
        notes='Testing',
        recipient=CoinbaseContact(
            id='509e01ca12838e0200000212',
            email='gsibble@gmail.com',
            name='gsibble@gmail.com',
        ),
        recipient_type='coinbase',
        request=True,
        sender=CoinbaseContact(
            id='514e4c1c802e1bef9800001e',
            email='george@atlasr.com',
            name='george@atlasr.com',
        ),
        status=CoinbaseTransaction.Status.pending,
    ),
    CoinbaseTransaction(
        amount=CoinbaseAmount('-1', 'BTC'),
        created_at=datetime(2013, 3, 21, 17, 2, 57,
                            tzinfo=tzoffset(None, -25200)),
        hash='42dd65a18dbea0779f32021663e60b1fab8ee0f859db7172a078d4528e01c6c8',
        id='514b9fb1b8377ee36500000d',
        notes='You gave me this a while ago.',
        idem='jkl',
        recipient=CoinbaseContact(
            id='4efec8d7bedd320001000003',
            email='brian@coinbase.com',
            name='Brian Armstrong',
        ),
        recipient_type='coinbase',
        recipient_address='brian@coinbase.com',
        request=False,
        sender=CoinbaseContact(
            id='509e01ca12838e0200000212',
            email='gsibble@gmail.com',
            name='gsibble@gmail.com',
        ),
        status=CoinbaseTransaction.Status.complete,
    ),
    CoinbaseTransaction(
        amount=CoinbaseAmount('1', 'BTC'),
        created_at=datetime(2012, 11, 9, 23, 27, 7,
                            tzinfo=tzoffset(None, -28800)),
        hash='ac9b0ffbe36dbe12c5ca047a5bdf9cadca3c9b89b74751dff83b3ac863ccc0b3',
        id='509e01cb12838e0200000224',
        notes='',
        idem='xyz',
        recipient=CoinbaseContact(
            id='509e01ca12838e0200000212',
            email='gsibble@gmail.com',
            name='gsibble@gmail.com',
        ),
        recipient_type='coinbase',
        recipient_address='gsibble@gmail.com',
        request=False,
        sender=CoinbaseContact(
            id='4efec8d7bedd320001000003',
            email='brian@coinbase.com',
            name='Brian Armstrong',
        ),
        status=CoinbaseTransaction.Status.complete,
    ),
]
