__author__ = 'gsibble'

import config

from api import swagger

from api.LocationsApi import LocationsApi
from api.models import Location as SwaggerLocation

class SDFirstClassObject(object):

    def __init__(self, api_client, use_cache=True, *args, **kwargs):
        self._api_key = api_client.apiKey
        self._api_client = api_client
        self._use_cache = use_cache
        self._swagger_location_api = LocationsApi(self._api_client)

class SDLocation(SDFirstClassObject):

    class SDMenu(object):

        def __init__(self, swagger_menu):

            #Set up the public lists
            self.items = []
            self.categories = swagger_menu

            #Set up the private item dictionaries
            self._item_name_dict = {}
            self._item_id_dict = {}

            #Set up private category dictionaries
            self._category_name_dict = {}
            self._category_id_dict = {}

            for category in swagger_menu:
                self._category_name_dict[category.category_name] = category
                self._category_id_dict[category.category_id] = category

                #Store the items
                for item in category.items:
                    setattr(item, 'category', category.category_name)
                    self.items.append(item)
                    self._item_name_dict[item.name] = item
                    self._item_id_dict[item.item_id] = item

        def get_category(self, category_id=None, category_name=None):

            category_object = None

            if category_id is not None:
                category_object = self._category_id_dict[category_id]
            elif category_name is not None:
                category_object = self._category_name_dict[category_name]

            return category_object

        def get_item(self, item_id=None, item_name=None):

            item_object = None

            if item_id is not None:
                item_object = self._item_id_dict[item_id]
            elif item_name is not None:
                item_object = self._category_name_dict[item_name]

            return item_object

    def __init__(self, location_id, api_client, include_menu, use_cache, *args, **kwargs):
        super(SDLocation, self).__init__(api_client, use_cache)
        self._location_id = location_id

        #Get the location via swagger
        self._swagger_location = self._swagger_location_api.getLocation(location_id, self._api_key, use_cache=self._use_cache)

        #Set attributes of first class Location to match Swagger Location object
        for attribute in self._swagger_location.swaggerTypes:
            self.__setattr__(attribute, getattr(self._swagger_location, attribute))

        if include_menu:
            self.update_menu(use_cache)

    def update_menu(self, use_cache=True):

        if not self._use_cache:
            use_cache = False

        self._swagger_menu = self._swagger_location_api.getLocationMenu(self._location_id, self._api_key, use_cache=use_cache)

    @property
    def menu(self):

        if not hasattr(self, '_swagger_menu'):
            self.update_menu()

        return self.SDMenu(self._swagger_menu)

class SubtleData(object):

    def __init__(self, api_key, use_cache=True):
        """

        :param api_key: Subtledata API Key
        :param use_cache: Use Subtledata's Redis Caching layer to accelerate delivery of results.  This specific setting is global to all calls for this API object.
        """
        self.api_key = api_key
        self.use_cache = use_cache
        self.api_client = swagger.ApiClient(api_key, config.SD_ENDPOINT)

    def Location(self, location_id, use_cache=True, include_menu=False):

        if not self.use_cache:
            use_cache = False

        return SDLocation(location_id, self.api_client, include_menu, use_cache)