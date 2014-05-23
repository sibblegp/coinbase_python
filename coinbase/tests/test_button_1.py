from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount, CoinbasePaymentButton
from . import account_setup
from .http_mocking import *


@with_http_mocking
class ButtonTest1(TestCase):
    """
    Create a button using all of the default values.
    """

    def setUp(self):
        mock_http('POST https://coinbase.com/api/v1/buttons',
                  response_body)

    def test_creating_a_button_with_key(self):
        account = account_setup.with_key()
        button = account.create_button(button_spec)
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })
        this(button).should.equal(expected_button)

    def test_creating_a_button_with_oauth(self):
        account = account_setup.with_oauth()
        button = account.create_button(button_spec)
        this(last_request_json()).should.equal(expected_request_json)
        this(last_request_params()).should.equal({})
        this(button).should.equal(expected_button)


button_spec = CoinbasePaymentButton(
    name='a',
    price=CoinbaseAmount('5', 'USD'),
)


expected_request_json = {
    'button': {
        'name': 'a',
        'price_string': '5',
        'price_currency_iso': 'USD',
    }
}


response_body = """
{
    "button": {
        "auto_redirect": false,
        "callback_url": null,
        "cancel_url": null,
        "choose_price": false,
        "code": "f68a5c68d0a68679a6c6f569e651d695",
        "custom": "",
        "description": "",
        "include_address": false,
        "include_email": false,
        "info_url": null,
        "name": "a",
        "price": {
            "cents": 500,
            "currency_iso": "USD"
        },
        "style": "buy_now_large",
        "success_url": null,
        "text": "Pay With Bitcoin",
        "type": "buy_now",
        "variable_price": false
    },
    "success": true
}
"""


expected_button = CoinbasePaymentButton(
    id='f68a5c68d0a68679a6c6f569e651d695',
    name='a',
    price=CoinbaseAmount('5', 'USD'),
    auto_redirect=False,
    custom='',
    description='',
    include_address=False,
    include_email=False,
    style='buy_now_large',
    text='Pay With Bitcoin',
    type='buy_now',
    variable_price=False,
)
