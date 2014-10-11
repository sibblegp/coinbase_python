from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseOrder
from . import account_setup
from .http_mocking import *


@with_http_mocking
class OrdersTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/orders',
                  response_body)

    def test_orders_with_key(self):
        account = account_setup.with_key()
        this(account.orders()).should.equal(expected_orders)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })

    def test_orders_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.orders()).should.equal(expected_orders)
        this(last_request_params()).should.equal({})


response_body = """
{
    "current_page": 1,
    "num_pages": 131,
    "orders": [
        {
            "customer": {
                "email": null
            },
            "order": {
                "button": {
                    "description": "warm and fuzzy",
                    "id": "0fde6d456181be1279fef6879d6897a3",
                    "name": "Alpaca socks",
                    "type": "buy_now"
                },
                "created_at": "2014-04-21T10:25:50-07:00",
                "custom": "abcdef",
                "id": "8DJ2Z9AQ",
                "receive_address": "8uREGg34ji4gn43M93cuibhbkfi6FbyF1g",
                "status": "expired",
                "total_btc": {
                    "cents": 1818000,
                    "currency_iso": "BTC"
                },
                "total_native": {
                    "cents": 900,
                    "currency_iso": "USD"
                },
                "transaction": null
            }
        },
        {
            "customer": {
                "email": "alice@example.com"
            },
            "order": {
                "button": {
                    "description": "20% off",
                    "id": "69adb65c95af59ed5b9ab5de55a579db",
                    "name": "Pineapple",
                    "type": "buy_now"
                },
                "created_at": "2014-04-21T09:56:57-07:00",
                "custom": "ghijkl",
                "id": "J3KAD35D",
                "receive_address": "b87nihewshngyuFUbu6fy5vbtdtryfhhj1",
                "status": "completed",
                "total_btc": {
                    "cents": 799600,
                    "currency_iso": "BTC"
                },
                "total_native": {
                    "cents": 400,
                    "currency_iso": "USD"
                },
                "transaction": {
                    "confirmations": 11,
                    "hash":
"67b6a75d56cd5675868d5695c695865ab9568ef5895653a2f23454d45e4a357a",
                    "id": "658bc586df6ef56740ac6de5"
                }
            }
        },
        {
            "customer": {
                "email": "bob@example.com"
            },
            "order": {
                "button": {
                    "description": null,
                    "id": "586df68e5a665c6975d569e569a768c5",
                    "name": "Things",
                    "type": "buy_now"
                },
                "created_at": "2014-04-19T17:07:37-07:00",
                "custom": "xyzzy",
                "id": "7DAF5310",
                "mispaid_btc": {
                    "cents": 2034753,
                    "currency_iso": "BTC"
                },
                "mispaid_native": {
                    "cents": 1007,
                    "currency_iso": "USD"
                },
                "receive_address": "8Wmgg87fgu6777ihgbFTYugyjfFT686fFf",
                "status": "mispaid",
                "total_btc": {
                    "cents": 1980000,
                    "currency_iso": "BTC"
                },
                "total_native": {
                    "cents": 1000,
                    "currency_iso": "USD"
                },
                "transaction": {
                    "confirmations": 314,
                    "hash":
"56949ae6498b66f9865e67a6c4d759578ad5986e65965f5965a695696ec59c5d",
                    "id": "16a64b43fe6c435a45c07a0d"
                }
            }
        }
    ],
    "total_count": 3262
}
"""


expected_orders = [
    CoinbaseOrder(
        id='8DJ2Z9AQ',
        created_at=datetime(2014, 4, 21, 10, 25, 50,
                            tzinfo=tzoffset(None, -25200)),
        status=CoinbaseOrder.Status.expired,
        receive_address='8uREGg34ji4gn43M93cuibhbkfi6FbyF1g',
        button=CoinbaseOrder.Button(
            id='0fde6d456181be1279fef6879d6897a3',
            description='warm and fuzzy',
            name='Alpaca socks',
            type='buy_now',
        ),
        custom='abcdef',
        total=CoinbaseAmount.BtcAndNative(
            btc=CoinbaseAmount('.01818000', 'BTC'),
            native=CoinbaseAmount('9', 'USD'),
        ),
        customer=CoinbaseOrder.Customer(),
    ),
    CoinbaseOrder(
        id='J3KAD35D',
        created_at=datetime(2014, 4, 21, 9, 56, 57,
                            tzinfo=tzoffset(None, -25200)),
        status=CoinbaseOrder.Status.complete,
        receive_address='b87nihewshngyuFUbu6fy5vbtdtryfhhj1',
        button=CoinbaseOrder.Button(
            id='69adb65c95af59ed5b9ab5de55a579db',
            description='20% off',
            name='Pineapple',
            type='buy_now',
        ),
        custom='ghijkl',
        total=CoinbaseAmount.BtcAndNative(
            btc=CoinbaseAmount('.00799600', 'BTC'),
            native=CoinbaseAmount('4', 'USD'),
        ),
        transaction=CoinbaseOrder.Transaction(
            id='658bc586df6ef56740ac6de5',
            hash='67b6a75d56cd5675868d5695c695865a'
                 'b9568ef5895653a2f23454d45e4a357a',
            confirmations=11
        ),
        customer=CoinbaseOrder.Customer(
            email='alice@example.com',
        ),
    ),
    CoinbaseOrder(
        id='7DAF5310',
        created_at=datetime(2014, 4, 19, 17, 7, 37,
                            tzinfo=tzoffset(None, -25200)),
        status=CoinbaseOrder.Status.mispaid,
        receive_address='8Wmgg87fgu6777ihgbFTYugyjfFT686fFf',
        button=CoinbaseOrder.Button(
            id='586df68e5a665c6975d569e569a768c5',
            name='Things',
            type='buy_now',
        ),
        custom='xyzzy',
        mispaid=CoinbaseAmount.BtcAndNative(
            btc=CoinbaseAmount('.02034753', 'BTC'),
            native=CoinbaseAmount('10.07', 'USD'),
        ),
        total=CoinbaseAmount.BtcAndNative(
            btc=CoinbaseAmount('.0198', 'BTC'),
            native=CoinbaseAmount('10', 'USD'),
        ),
        customer=CoinbaseOrder.Customer(
            email='bob@example.com',
        ),
        transaction=CoinbaseOrder.Transaction(
            id='16a64b43fe6c435a45c07a0d',
            hash='56949ae6498b66f9865e67a6c4d75957'
                 '8ad5986e65965f5965a695696ec59c5d',
            confirmations=314,
        ),
    ),
]
