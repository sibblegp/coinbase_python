from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseOrder, CoinbasePaymentButton
from . import account_setup
from .http_mocking import *


@with_http_mocking
class CreateButtonAndOrderTest(TestCase):
    """
    The example from https://coinbase.com/api/doc/1.0/orders/create.html
    """

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/orders',
                  response_body)

    def test_create_button_and_order_with_key(self):
        account = account_setup.with_key()
        order = account.create_button_and_order(button_spec)
        this(last_request_json()).should.equal(expected_button_json)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })
        this(order).should.equal(expected_order)

    def test_create_button_and_order_with_oauth(self):
        account = account_setup.with_oauth()
        order = account.create_button_and_order(button_spec)
        this(last_request_json()).should.equal(expected_button_json)
        this(last_request_params()).should.equal({})
        this(order).should.equal(expected_order)


@with_http_mocking
class CreateOrderFromButtonTest(TestCase):
    """
    The example from
    https://coinbase.com/api/doc/1.0/buttons/create_order.html
    """

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/buttons/'
                  '93865b9cae83706ae59220c013bc0afd/create_order',
                  response_body)

    def test_create_order_from_button_with_key(self):
        account = account_setup.with_key()
        order = account.create_order_from_button(
            button_id='93865b9cae83706ae59220c013bc0afd')
        this(last_request_body()).should.equal(b'')
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })
        this(order).should.equal(expected_order)

    def test_create_order_from_button_with_oauth(self):
        account = account_setup.with_oauth()
        order = account.create_order_from_button(
            button_id='93865b9cae83706ae59220c013bc0afd')
        this(last_request_body()).should.equal(b'')
        this(last_request_params()).should.equal({})
        this(order).should.equal(expected_order)


button_spec = CoinbasePaymentButton(
    name='test',
    type='buy_now',
    price=CoinbaseAmount('1.23', 'USD'),
)


expected_button_json = {
    'button': {
        'name': 'test',
        'type': 'buy_now',
        'price_string': '1.23',
        'price_currency_iso': 'USD',
    }
}


response_body = """
{
  "success": true,
  "order": {
    "id": "8QNULQFE",
    "created_at": "2014-02-04T23:36:30-08:00",
    "status": "new",
    "total_btc": {
      "cents": 12300000,
      "currency_iso": "BTC"
    },
    "total_native": {
      "cents": 123,
      "currency_iso": "USD"
    },
    "custom": null,
    "receive_address": "mnskjZs57dBAmeU2n4csiRKoQcGRF4tpxH",
    "button": {
      "type": "buy_now",
      "name": "test",
      "description": null,
      "id": "1741b3be1eb5dc50625c48851a94ae13"
    },
    "transaction": null
  }
}
"""


expected_order = CoinbaseOrder(
    id='8QNULQFE',
    created_at=datetime(2014, 2, 4, 23, 36, 30,
                        tzinfo=tzoffset(None, -28800)),
    status=CoinbaseOrder.Status.pending,
    total=CoinbaseAmount.BtcAndNative(
        btc=CoinbaseAmount('.12300000', 'BTC'),
        native=CoinbaseAmount('1.23', 'USD'),
    ),
    receive_address='mnskjZs57dBAmeU2n4csiRKoQcGRF4tpxH',
    button=CoinbaseOrder.Button(
        type='buy_now',
        name='test',
        id='1741b3be1eb5dc50625c48851a94ae13',
    ),
)
