import dateutil.parser
from enum import Enum

from .util import namedtuple
from .amount import CoinbaseAmount


class CoinbaseTransfer(namedtuple(
    'CoinbaseTransfer',
    optional='type code created_at fees_coinbase fees_bank '
             'payout_date transaction_id status btc_amount '
             'subtotal_amount total_amount description'
)):
    """
    status - CoinbaseTransfer.Status
    """

    class Status(Enum):
        """
        Enumeration of values for `CoinbaseTransfer.status`.
        """

        pending = 'Pending'

        complete = 'Complete'

        canceled = 'Canceled'

        reversed = 'Reversed'

    @classmethod
    def from_coinbase_dict(cls, transfer):
        return CoinbaseTransfer(
            type=transfer['type'],
            code=transfer['code'],
            created_at=dateutil.parser.parse(
                transfer['created_at']),
            fees_coinbase=CoinbaseAmount.from_coinbase_dict(
                transfer['fees']['coinbase']),
            fees_bank=CoinbaseAmount.from_coinbase_dict(
                transfer['fees']['bank']),
            payout_date=dateutil.parser.parse(
                transfer['payout_date']),
            transaction_id=transfer.get('transaction_id', ''),
            status=CoinbaseTransfer.Status(transfer['status']),
            btc_amount=CoinbaseAmount.from_coinbase_dict(
                transfer['btc']),
            subtotal_amount=CoinbaseAmount.from_coinbase_dict(
                transfer['subtotal']),
            total_amount=CoinbaseAmount.from_coinbase_dict(
                transfer['total']),
            description=transfer.get('description', ''),
        )
