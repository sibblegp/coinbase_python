from sure import this
from unittest import TestCase

from coinbase import CoinbaseAmount, CoinbasePaymentButton
from . import account_setup
from .http_mocking import *


@with_http_mocking
class ButtonTest2(TestCase):
    """
    Create a subscription button with suggested prices.
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
    name='abc def',
    description='ghi jkl',
    text='lol',
    custom='12345x',
    custom_secure=True,
    price=CoinbaseAmount('102.76', 'USD'),
    type='subscription',
    repeat='monthly',
    style='subscription_small',
    callback_url='https://example.com/callback',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
    info_url='https://example.com/info',
    auto_redirect=True,
    suggested_prices=['5', '20.25', '250'],
    include_address=True,
    include_email=True,
    variable_price=True,
)


expected_request_json = {
    'button': {
        'name': 'abc def',
        'description': 'ghi jkl',
        'text': 'lol',
        'custom': '12345x',
        'custom_secure': True,
        'price_string': '102.76',
        'price_currency_iso': 'USD',
        'type': 'subscription',
        'repeat': 'monthly',
        'style': 'subscription_small',
        'callback_url': 'https://example.com/callback',
        'success_url': 'https://example.com/success',
        'cancel_url': 'https://example.com/cancel',
        'info_url': 'https://example.com/info',
        'auto_redirect': True,
        'choose_price': True,
        'price1': '5',
        'price2': '20.25',
        'price3': '250',
        'include_address': True,
        'include_email': True,
        'variable_price': True,
    }
}


response_body = """
{
    "button": {
        "auto_redirect": true,
        "callback_url": "https://example.com/callback",
        "cancel_url": "https://example.com/cancel",
        "choose_price": true,
        "code": "089e75679117f0a59524fa0c2c2aae59",
        "custom": "12345x",
        "description": "ghi jkl",
        "include_address": true,
        "include_email": true,
        "info_url": "https://example.com/info",
        "name": "abc def",
        "price": {
            "cents": 10276,
            "currency_iso": "USD"
        },
        "style": "subscription_small",
        "success_url": "https://example.com/success",
        "text": "lol",
        "type": "subscription",
        "variable_price": true
    },
    "success": true
}
"""


expected_button = button_spec._replace(
    id='089e75679117f0a59524fa0c2c2aae59',
    # Coinbase's response doesn't include "price1", "price2", "price3",
    # "repeat", "custom_secure". It's unclear if that's intentional.
    suggested_prices=[],
    custom_secure=None,
    repeat=None,
)
