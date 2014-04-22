__author__ = 'mhluongo'

from . import CoinbaseAmount


class CoinbasePaymentButton(object):

    def __init__(self, code=None, type=None, style=None, text=None, name=None,
                 description=None, custom=None, callback_url=None,
                 success_url=None, cancel_url=None, info_url=None, price=None,
                 auto_redirect=None, choose_price=None, include_address=None,
                 include_email=None, variable_price=None):

        self.code = code
        self.type = type
        self.style = style
        self.text = text
        self.name = name
        self.description = description
        self.custom = custom
        self.callback_url = callback_url
        self.success_url = success_url
        self.cancel_url = cancel_url
        self.info_url = info_url
        self.price = price
        self.auto_redirect = auto_redirect
        self.choose_price = choose_price
        self.include_address = include_address
        self.include_email = include_email
        self.variable_price = variable_price

    @classmethod
    def from_coinbase_dict(cls, button):
        return CoinbasePaymentButton(
            auto_redirect=button['auto_redirect'],
            callback_url=button['callback_url'],
            cancel_url=button['cancel_url'],
            choose_price=button['choose_price'],
            code=button['code'],
            custom=button['custom'],
            description=button['description'],
            info_url=button['info_url'],
            name=button['name'],
            price=CoinbaseAmount.from_coinbase_dict(button['price']),
            style=button['style'],
            success_url=button['success_url'],
            text=button['text'],
            type=button['type'],
            variable_price=button['variable_price'],
        )
