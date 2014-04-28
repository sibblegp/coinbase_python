__author__ = 'pmb6tz'

import dateutil.parser

from amount import CoinbaseAmount


class CoinbaseTransfer(object):

    def __init__(self, type, code, created_at, fees_coinbase, fees_bank,
                 payout_date, transaction_id, status, btc_amount,
                 subtotal_amount, total_amount, description):
        self.type = type
        self.code = code
        self.created_at = created_at
        self.fees_coinbase = fees_coinbase
        self.fees_bank = fees_bank
        self.payout_date = payout_date
        self.transaction_id = transaction_id
        self.status = status
        self.btc_amouint = btc_amount
        self.subtotal_amount = subtotal_amount
        self.total_amount = total_amount
        self.description = description

    @classmethod
    def from_coinbase_dict(cls, transfer):

        kwargs = {}

        kwargs['type'] = transfer['type']
        kwargs['code'] = transfer['code']
        kwargs['created_at'] = dateutil.parser.parse(transfer['created_at'])

        kwargs['fees_coinbase'] = \
            CoinbaseAmount.from_coinbase_dict(transfer['fees']['coinbase'])

        kwargs['fees_bank'] = \
            CoinbaseAmount.from_coinbase_dict(transfer['fees']['bank'])

        kwargs['payout_date'] = transfer['payout_date']
        kwargs['transaction_id'] = transfer.get('transaction_id','')
        kwargs['status'] = transfer['status']

        kwargs['btc_amount'] = \
            CoinbaseAmount.from_coinbase_dict(transfer['btc'])

        kwargs['subtotal_amount'] = \
            CoinbaseAmount.from_coinbase_dict(transfer['subtotal'])

        kwargs['total_amount'] = \
            CoinbaseAmount.from_coinbase_dict(transfer['total'])

        kwargs['description'] = transfer.get('description', '')

        return CoinbaseTransfer(**kwargs)

    def refresh(self):
        pass
        #TODO:  Refresh the transfer

    def cancel(self):
        pass
        #TODO:  Cancel the transfer if possible

    def complete(self):
        pass
        #TODO:  Approve the transfer if possible

    def resend(self):
        pass
        #TODO:  Resend the transfer email if possible
