__author__ = 'gsibble'

from api.LocationsApi import LocationsApi
from api.UsersApi import UsersApi
from api.TicketsApi import TicketsApi
from api.GeneralApi import GeneralApi

class SDInterface(object):

    def __init__(self, parent, *args, **kwargs):
        if hasattr(parent, 'api_key'):
            self._api_key = parent.api_key
        else:
            self._api_key = parent._api_key
        self._use_cache = parent._use_cache
        self._api_client = parent._api_client
        self._swagger_locations_api = LocationsApi(self._api_client)
        self._swagger_users_api = UsersApi(self._api_client)
        self._swagger_tickets_api = TicketsApi(self._api_client)
        self._swagger_general_api = GeneralApi(self._api_client)

class SDFirstClassCollection(SDInterface):

    def __init__(self, parent, *args, **kwargs):
        super(SDFirstClassCollection, self).__init__(parent)



class SDFirstClassObject(SDInterface):
    def __init__(self, parent, use_cache=True, *args, **kwargs):
        super(SDFirstClassObject, self).__init__(parent)

        #Override use cache if not already set to False
        if self._use_cache:
            self._use_cache = use_cache