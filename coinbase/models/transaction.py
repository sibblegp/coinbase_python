__author__ = 'gsibble'

import dateutil.parser

from amount import CoinbaseAmount
from contact import CoinbaseContact


class CoinbaseTransaction(object):

    def __init__(self, transaction_id, created_at, notes, amount,
                 status, request, sender=None, recipient=None,
                 recipient_address=None, recipient_type=None):
        """
        :param request: bool
        :param sender: CoinbaseContact
        :param recipient: CoinbaseContact
        :param recipient_type: 'coinbase' or 'bitcoin'
        """
        self.transaction_id = transaction_id
        self.created_at = created_at
        self.notes = notes
        self.amount = amount
        self.status = status
        self.request = request
        self.sender = sender
        self.recipient = recipient
        self.recipient_address = recipient_address
        self.recipient_type = recipient_type

    @classmethod
    def from_coinbase_dict(cls, transaction):

        kwargs = {}

        kwargs['transaction_id'] = transaction['id']
        kwargs['created_at'] = dateutil.parser.parse(transaction['created_at'])
        kwargs['notes'] = transaction['notes']

        kwargs['amount'] = \
            CoinbaseAmount.from_coinbase_dict(transaction['amount'])

        kwargs['status'] = transaction['status']
        kwargs['request'] = transaction['request']

        #Sender Information
        if 'sender' in transaction:
            sender_id = transaction['sender'].get('id', None)
            sender_name = transaction['sender'].get('name', None)
            sender_email = transaction['sender'].get('email', None)

            kwargs['sender'] = CoinbaseContact(contact_id=sender_id,
                                               name=sender_name,
                                               email=sender_email)

        else:
            #TODO:  Not sure what key would go here
            pass

        #Recipient Info
        if 'recipient' in transaction:
            recipient_id = transaction['recipient'].get('id', None)
            recipient_name = transaction['recipient'].get('name', None)
            recipient_email = transaction['recipient'].get('email', None)

            kwargs['recipient'] = CoinbaseContact(contact_id=recipient_id,
                                                  name=recipient_name,
                                                  email=recipient_email)
            kwargs['recipient_address'] = None
            kwargs['recipient_type'] = 'coinbase'

        elif 'recipient_address' in transaction:
            kwargs['recipient'] = None
            kwargs['recipient_address'] = transaction['recipient_address']
            kwargs['recipient_type'] = 'bitcoin'

        return CoinbaseTransaction(**kwargs)

    def refresh(self):
        pass
        #TODO:  Refresh the transaction

    def cancel(self):
        pass
        #TODO:  Cancel the transaction if possible

    def complete(self):
        pass
        #TODO:  Approve the transaction if possible

    def resend(self):
        pass
        #TODO:  Resend the transaction email if possible
