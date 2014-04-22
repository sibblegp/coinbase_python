__author__ = 'pmb6tz'

from amount import CoinbaseAmount


class CoinbaseTransfer(object):

    def __init__(self, transfer):
        self.type = transfer['type']
        self.code = transfer['code']
        self.created_at = transfer['created_at']

        self.fees_coinbase = \
            CoinbaseAmount.from_coinbase_dict(transfer['fees']['coinbase'])

        self.fees_bank = \
            CoinbaseAmount.from_coinbase_dict(transfer['fees']['bank'])

        self.payout_date = transfer['payout_date']
        self.transaction_id = transfer.get('transaction_id','')
        self.status = transfer['status']

        self.btc_amount = \
            CoinbaseAmount.from_coinbase_dict(transfer['btc'])

        self.subtotal_amount = CoinbaseAmount \
            .from_coinbase_dict(transfer['subtotal'])

        self.total_amount = \
            CoinbaseAmount.from_coinbase_dict(transfer['total'])

        self.description = transfer.get('description','')

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
