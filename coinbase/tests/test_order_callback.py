from sure import this

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseOrder


def test_order_callback():
    """
    The example from the callbacks doc
    https://coinbase.com/docs/merchant_tools/callbacks
    """
    this(CoinbaseOrder.parse_callback(callback_body)) \
        .should.be.equal(expected_order)


callback_body = """
{
  "customer": {
    "email": "coinbase@example.com",
    "shipping_address": [
      "John Smith",
      "123 Main St.",
      "Springfield, OR 97477",
      "United States"
    ]
  },
  "order": {
    "id": "5RTQNACF",
    "created_at": "2012-12-09T21:23:41-08:00",
    "status": "completed",
    "total_btc": {
      "cents": 100000000,
      "currency_iso": "BTC"
    },
    "total_native": {
      "cents": 1253,
      "currency_iso": "USD"
    },
    "custom": "order1234",
    "receive_address": "1NhwPYPgoPwr5hynRAsto5ZgEcw1LzM3My",
    "button": {
      "type": "buy_now",
      "name": "Alpaca Socks",
      "description": "The ultimate in lightweight footwear",
      "id": "5d37a3b61914d6d0ad15b5135d80c19f"
    },
    "transaction": {
      "id": "514f18b7a5ea3d630a00000f",
      "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
      "confirmations": 0
    },
    "refund_address": "1HcmQZarSgNuGYz4r7ZkjYumiU4PujrNYk"
  }
}
"""


expected_order = CoinbaseOrder(
    id='5RTQNACF',
    created_at=datetime(2012, 12, 9, 21, 23, 41,
                        tzinfo=tzoffset(None, -28800)),
    status=CoinbaseOrder.Status.complete,
    total=CoinbaseAmount.BtcAndNative(
        btc=CoinbaseAmount('1', 'BTC'),
        native=CoinbaseAmount('12.53', 'USD'),
    ),
    custom='order1234',
    receive_address='1NhwPYPgoPwr5hynRAsto5ZgEcw1LzM3My',
    button=CoinbaseOrder.Button(
        type='buy_now',
        name='Alpaca Socks',
        description='The ultimate in lightweight footwear',
        id='5d37a3b61914d6d0ad15b5135d80c19f',
    ),
    transaction=CoinbaseOrder.Transaction(
        id='514f18b7a5ea3d630a00000f',
        hash='4a5e1e4baab89f3a32518a88c31bc87f'
             '618f76673e2cc77ab2127b7afdeda33b',
        confirmations=0,
    ),
    customer=CoinbaseOrder.Customer(
        email='coinbase@example.com',
        shipping_address=[
            'John Smith',
            '123 Main St.',
            'Springfield, OR 97477',
            'United States',
        ]
    ),
    refund_address='1HcmQZarSgNuGYz4r7ZkjYumiU4PujrNYk',
)
