import dateutil.parser
from enum import Enum

from .util import namedtuple

from .amount import CoinbaseAmount
from .contact import CoinbaseContact


class CoinbaseTransaction(namedtuple(
    'CoinbaseTransaction',
    optional='id created_at notes amount status request hash idem '
             'sender recipient recipient_address recipient_type'
)):
    """
    status = CoinbaseTransaction.Status
    request - bool
    idem  - str
    sender - CoinbaseContact
    recipient - CoinbaseContact
    recipient_type - 'coinbase' or 'bitcoin'
    """

    class Status(Enum):
        """
        Enumeration of values for `CoinbaseTransaction.status`.
        """

        pending = 'pending'

        complete = 'complete'

    @classmethod
    def from_coinbase_dict(cls, x):

        t = CoinbaseTransaction(
            id=x['id'],
            created_at=dateutil.parser.parse(x['created_at']),
            notes=x['notes'],
            amount=CoinbaseAmount.from_coinbase_dict(x['amount']),
            status=CoinbaseTransaction.Status(x['status']),
            request=x['request'],
            hash=x.get('hsh'),
            recipient_type=('coinbase' if ('recipient' in x) else 'bitcoin'),
            idem=(x.get('idem') or None),
        )

        if 'sender' in x:
            t = t._replace(sender=CoinbaseContact.from_coinbase_dict(
                x['sender']))

        if 'recipient' in x:
            t = t._replace(
                recipient=CoinbaseContact.from_coinbase_dict(x['recipient']),
            )

        if 'recipient_address' in x:
            t = t._replace(
                recipient_address=x['recipient_address'],
            )

        return t
