import dateutil.parser

from .util import namedtuple

from amount import CoinbaseAmount
from contact import CoinbaseContact


class CoinbaseTransaction(namedtuple(
    'CoinbaseTransaction',
    optional='id created_at notes amount status request '
             'sender recipient recipient_address recipient_type'
)):
    """
    request - bool
    sender - CoinbaseContact
    recipient - CoinbaseContact
    recipient_type - 'coinbase' or 'bitcoin'
    """

    @classmethod
    def from_coinbase_dict(cls, x):

        t = CoinbaseTransaction(
            id=x['id'],
            created_at=dateutil.parser.parse(x['created_at']),
            notes=x['notes'],
            amount=CoinbaseAmount.from_coinbase_dict(x['amount']),
            status=x['status'],
            request=x['request'],
        )

        if 'sender' in x:
            t = t._replace(sender=CoinbaseContact.from_coinbase_dict(
                x['sender']))

        if 'recipient' in x:
            t = t._replace(
                recipient_type='coinbase',
                recipient=CoinbaseContact.from_coinbase_dict(x['recipient']),
            )
        elif 'recipient_address' in x:
            t = t._replace(
                recipient_type='bitcoin',
                recipient_address=x['recipient_address'],
            )

        return t
