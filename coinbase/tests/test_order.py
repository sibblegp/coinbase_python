from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseOrder
from .http_mocking import *
from . import account_setup


@with_http_mocking
class OrderTest(TestCase):
    """
    The example from the API doc
    https://coinbase.com/api/doc/1.0/orders/show.html
    """

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/orders/A7C52JQT',
                  response_body)
        mock_http('GET https://coinbase.com/api/v1/orders/custom123',
                  response_body)

    def test_get_order_by_id_with_key(self):
        account = account_setup.with_key()
        this(account.get_order('A7C52JQT')).should.equal(expected_order)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })

    def test_get_order_by_id_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.get_order('A7C52JQT')).should.equal(expected_order)
        this(last_request_params()).should.equal({})

    def test_get_order_by_custom_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.get_order('custom123')).should.equal(expected_order)
        this(last_request_params()).should.equal({})


response_body = """
{
  "order": {
    "id": "A7C52JQT",
    "created_at": "2013-03-11T22:04:37-07:00",
    "status": "completed",
    "total_btc": {
      "cents": 10000000,
      "currency_iso": "BTC"
    },
    "total_native": {
      "cents": 10000000,
      "currency_iso": "BTC"
    },
    "custom": "custom123",
    "receive_address": "mgrmKftH5CeuFBU3THLWuTNKaZoCGJU5jQ",
    "button": {
      "type": "buy_now",
      "name": "test",
      "description": "",
      "id": "eec6d08e9e215195a471eae432a49fc7"
    },
    "transaction": {
      "id": "513eb768f12a9cf27400000b",
      "hash":
"4cc5eec20cd692f3cdb7fc264a0e1d78b9a7e3d7b862dec1e39cf7e37ababc14",
      "confirmations": 0
    }
  }
}
"""


expected_order = CoinbaseOrder(
    id='A7C52JQT',
    created_at=datetime(2013, 3, 11, 22, 4, 37,
                        tzinfo=tzoffset(None, -25200)),
    status=CoinbaseOrder.Status.complete,
    total=CoinbaseAmount.BtcAndNative(
        btc=CoinbaseAmount('.1', 'BTC'),
        native=CoinbaseAmount('.1', 'BTC'),
    ),
    custom='custom123',
    receive_address='mgrmKftH5CeuFBU3THLWuTNKaZoCGJU5jQ',
    button=CoinbaseOrder.Button(
        type='buy_now',
        name='test',
        description='',
        id='eec6d08e9e215195a471eae432a49fc7',
    ),
    transaction=CoinbaseOrder.Transaction(
        id='513eb768f12a9cf27400000b',
        hash='4cc5eec20cd692f3cdb7fc264a0e1d78'
             'b9a7e3d7b862dec1e39cf7e37ababc14',
        confirmations=0,
    ),
)
