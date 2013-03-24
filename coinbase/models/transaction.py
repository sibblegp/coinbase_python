__author__ = 'gsibble'

EXAMPLE_RESOINSE = '''{
  "success": true,
  "transaction": {
    "id": "501a3554f8182b2754000003",
    "created_at": "2012-08-02T01:07:48-07:00",
    "notes": "Sample request for you!",
    "amount": {
      "amount": "1.23400000",
      "currency": "BTC"
    },
    "request": true,
    "status": "pending",
    "sender": {
      "id": "5011f33df8182b142400000a",
      "name": "User One",
      "email": "user1@example.com"
    },
    "recipient": {
      "id": "5011f33df8182b142400000e",
      "name": "User Two",
      "email": "user2@example.com"
    }
  }
}'''

from amount import CoinBaseAmount
from contact import CoinBaseContact

class CoinBaseTransaction(object):

    def __init__(self, transaction):

        self.transaction_id = transaction['id']
        self.created_at = transaction['created_at']
        self.notes = transaction['notes']

        transaction_amount = transaction['amount']['amount']
        transaction_currency = transaction['amount']['currency']

        self.amount = CoinBaseAmount(transaction_amount, transaction_currency)

        self.status = transaction['status']
        self.request = transaction['request']


        #Sender Information

        if 'sender' in transaction:
            sender_id = transaction['sender']['id']
            sender_name = transaction['sender']['name']
            sender_email = transaction['sender']['email']

            self.sender = CoinBaseContact(contact_id=sender_id,
                                          name=sender_name,
                                          email=sender_email)

        else:
            #TODO:  Not sure what key would go here
            pass

        #Recipient Info

        if 'recipient' in transaction:
            recipient_id = transaction['recipient']['id']
            recipient_name = transaction['recipient']['name']
            recipient_email = transaction['recipient']['email']

            self.recipient = CoinBaseContact(contact_id=recipient_id,
                                          name=recipient_name,
                                          email=recipient_email)
            self.recipient_address = None
            self.recipient_type = 'CoinBase'

        elif 'recipient_address' in transaction:
            self.recipient = None
            self.recipient_address = transaction['recipient_address']
            self.recipient_type = 'Bitcoin'

    def refresh(self):
        pass
        #TODO:  Refresh the transaction

    def cancel(self):
        pass
        #TODO:  Cancel the transaction if possible

    def complete(self):
        pass
        #TODO:  Approve the transaction if possible

    def resent(self):
        pass
        #TODO:  Resent the transaction email if possible

