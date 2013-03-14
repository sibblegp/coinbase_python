__author__ = 'gsibble'

from base_types import SDFirstClassCollection
from sd_ticket import SDTicket

class SDTicketCollection(SDFirstClassCollection):

    def __init__(self, parent):
        super(SDTicketCollection, self).__init__(parent)

    def get(self, ticket_id, user_id=None):
        return SDTicket(self._api_client, ticket_id=ticket_id, user_id=user_id)