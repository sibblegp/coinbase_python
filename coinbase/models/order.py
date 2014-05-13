from .util import namedtuple, optional

import dateutil.parser

from . import CoinbaseAmount


class CoinbaseOrder(namedtuple(
    'CoinbaseOrder',
    optional='id created_at status receive_address button '
             'transaction custom total mispaid customer_email'
)):

    @classmethod
    def from_coinbase_dict(cls, x):

        return CoinbaseOrder(
            id=x['order']['id'],
            created_at=dateutil.parser.parse(
                x['order']['created_at']),
            status=x['order']['status'],
            receive_address=x['order']['receive_address'],
            button=CoinbaseOrder.Button.from_coinbase_dict(
                x['order']['button']),
            transaction=optional(CoinbaseOrder.Transaction.from_coinbase_dict)(
                x['order']['transaction']),
            custom=x['order'].get('custom'),
            total=CoinbaseAmount.BtcAndNative.from_coinbase_dict(
                x['order'], prefix='total'),
            mispaid=CoinbaseAmount.BtcAndNative.from_coinbase_dict(
                x['order'], prefix='mispaid'),
            customer_email=x['customer'].get('email'),
        )

    class Button(namedtuple(
        'CoinbaseOrder_Button',
        'id type',
        optional='name description'
    )):

        @classmethod
        def from_coinbase_dict(cls, x):
            return CoinbaseOrder.Button(
                id=x['id'],
                type=x['type'],
                name=x['name'],
                description=x['description'],
            )

    class Transaction(namedtuple(
        'CoinbaseOrder_Transaction',
        'id hash confirmations'
    )):

        @classmethod
        def from_coinbase_dict(cls, x):
            return CoinbaseOrder.Transaction(
                id=x['id'],
                hash=x['hash'],
                confirmations=x['confirmations'],
            )
