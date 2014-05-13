__author__ = 'mhluongo'

from .util import namedtuple

from . import CoinbaseAmount


class CoinbasePaymentButton(namedtuple(
    'CoinbasePaymentButton',
    optional='id type style text name description custom '
             'callback_url success_url cancel_url info_url '
             'price auto_redirect choose_price include_address '
             'include_email variable_price'
)):

    @classmethod
    def from_coinbase_dict(cls, x):
        return CoinbasePaymentButton(
            id=x['code'],
            auto_redirect=x['auto_redirect'],
            callback_url=x['callback_url'],
            cancel_url=x['cancel_url'],
            choose_price=x['choose_price'],
            custom=x['custom'],
            description=x['description'],
            info_url=x['info_url'],
            name=x['name'],
            price=CoinbaseAmount.from_coinbase_dict(x['price']),
            style=x['style'],
            success_url=x['success_url'],
            text=x['text'],
            type=x['type'],
            variable_price=x['variable_price'],
        )
