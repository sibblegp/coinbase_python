__author__ = 'gsibble'

from base_types import  SDFirstClassObject
from sd_menu import SDMenu
from sd_table import SDTable

class SDLocation(SDFirstClassObject):

    def __init__(self, parent, location_id, include_menu, use_cache, *args, **kwargs):
        super(SDLocation, self).__init__(parent, use_cache)
        self._location_id = location_id

        #Get the location via swagger
        self._swagger_location = self._swagger_locations_api.getLocation(location_id, self._api_key,
                                                                         use_cache=self._use_cache)

        #Set attributes of first class Location to match Swagger Location object
        for attribute in self._swagger_location.swaggerTypes:
            self.__setattr__(attribute, getattr(self._swagger_location, attribute))

        #Set the tables to be our type
        self.tables = [SDTable(self, table) for table in self.tables]

        if include_menu:
            self.update_menu(use_cache)

    def update_menu(self, use_cache=True):

        if not self._use_cache:
            use_cache = False

        self._swagger_menu = self._swagger_locations_api.getLocationMenu(self._location_id, self._api_key,
                                                                         use_cache=use_cache)

    @property
    def menu(self):

        if not hasattr(self, '_swagger_menu'):
            self.update_menu()

        return SDMenu(self, self._swagger_menu)

    @property
    def open_tables(self):
        return []

    def open_ticket_for_dine_in(self, user_id, device_id, table_id, business_expense=False):
        new_ticket_body = {

        }

        #TODO:  Implement Later
        #Return a SDTicket
        pass

    def open_ticket_for_take_out(self, user_id):

        #Return a SDTicket
        pass

    def open_ticket_for_delivery(self, user_id):

        #Return a SDTicket
        pass