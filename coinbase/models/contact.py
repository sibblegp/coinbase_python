__author__ = 'gsibble'

from .util import namedtuple


class CoinbaseContact(namedtuple(
    'CoinbaseContact',
    optional='id name email'
)):
    @classmethod
    def from_coinbase_dict(cls, x):
        return CoinbaseContact(
            id=x.get('id'),
            name=x.get('name'),
            email=x.get('email'),
        )
