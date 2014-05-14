import dateutil.parser
import json

from .util import namedtuple, optional
from . import CoinbaseAmount


class CoinbaseOrder(namedtuple(
    'CoinbaseOrder',
    optional='id created_at status receive_address button '
             'transaction custom total mispaid customer refund_address'
)):
    """
    status
            These rules are inferred from experimentation.
            - An order's status is one of:
              "pending", "complete", "mispaid", "expired"
            - Orders are be created through the API, or by a user clicking a
              payment button. In the latter case, the order is only behind
              the scenes; it is hidden from the API until a payment is made.
            - All orders have an initial status of "pending".
            - When a "pending" order receives a payment in the correct amount,
              its status permanently becomes "complete".
            - When a "pending" order receives a payment in an incorrect amount,
              its status permanently becomes "mispaid".
            - When a "pending" order's time runs out, its status permanently
              becomes "expired".
    total
            CoinbaseAmount.BtcAndNative. This is the order's price; in other
            words, the amount that Coinbase expects to receive for the order's
            status to become "complete".
    mispaid
            CoinbaseAmount.BtcAndNative. This field is present if the order's
            status is "mispaid" or "expired". Its value is the amount of the
            most recent payment made on this order.
    refund_address
            A refund address on off-blockchain order payments.
            "This is an experimental feature."
    button
            CoinbaseOrder.Button
    transaction
            CoinbaseOrder.Transaction
    customer
            CoinbaseOrder.Customer
    """

    @classmethod
    def parse_callback(cls, s):
        return CoinbaseOrder.from_coinbase_dict(json.loads(s))

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
            customer=optional(CoinbaseOrder.Customer.from_coinbase_dict)(
                x.get('customer')),
            refund_address=x['order'].get('refund_address'),
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

    class Customer(namedtuple(
        'CoinbaseOrder_Customer',
        optional='email shipping_address'
    )):

        @classmethod
        def from_coinbase_dict(cls, x):
            return CoinbaseOrder.Customer(
                email=x.get('email'),
                shipping_address=x.get('shipping_address'),
            )
