__author__ = 'gsibble'

from base_types import SDFirstClassObject
import constants as C

class SDTicket(SDFirstClassObject):
    def __init__(self, parent, ticket_id, user_id=None, get_values=True, *args, **kwargs):
        super(SDTicket, self).__init__(parent, False)

        self.ticket_id = ticket_id
        self.user_id = user_id

        if get_values == True:
            pass
            #TODO:  Implement this
            # self._swagger_ticket = self._swagger_tickets_api.getTicket(ticket_id, user_id)
            #
            # if self._swagger_ticket is not None:
            #     for attribute in self._swagger_ticket.swaggerTypes:
            #         self.__setattr__(attribute, getattr(self._swagger_ticket, attribute))

    def add_item_to_order(self, item_id, quantity, instructions=None, modifiers=None):

        if hasattr(self, 'user_id') and hasattr(self, 'ticket_id'):
            if self.user_id is not None and self.ticket_id is not None:
                post_body = {
                    'item_id': int(item_id),
                    'quantity': quantity,

                    }

                if instructions is not None:
                    post_body['instructions'] = instructions

                if modifiers is not None:
                    post_body['modifiers'] = modifiers

                print post_body

                returned_status = self._swagger_tickets_api.addItemsToOrder(self.ticket_id, self.user_id, self._api_key,
                                                                            body=post_body)

                return returned_status

            else:

                raise C.NoUserSetOnTicket
        else:
            raise C.NoUserSetOnTicket

    def submit_order(self):

        if hasattr(self, 'user_id') and hasattr(self, 'ticket_id'):
            if self.user_id is not None and self.ticket_id is not None:

                returned_status = self._swagger_tickets_api.submitOrder(self.ticket_id, self.user_id, self._api_key,
                                                                        body={'send': True})

                return returned_status
            else:
                raise C.NoUserSetOnTicket
        else:
            raise C.NoUserSetOnTicket