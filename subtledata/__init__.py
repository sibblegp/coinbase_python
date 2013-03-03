__author__ = 'gsibble'

import config

from api import swagger

from api.LocationsApi import LocationsApi
from api.models import Location as SwaggerLocation

class SDFirstClassObject(object):

    def __init__(self, api_client):
        self._api_key = api_client.apiKey
        self._api_client = api_client
        self._swagger_location_api = LocationsApi(self._api_client)


class SDLocation(SDFirstClassObject):

    def __init__(self, location_id, api_client):
        super(SDLocation, self).__init__(api_client)
        self._location_id = location_id

        #Get the location via swagger
        self._swagger_location = self._swagger_location_api.getLocation(location_id, self._api_key)

        #Set attributes of first class Location to match Swagger Location object
        for attribute in self._swagger_location.swaggerTypes:
            self.__setattr__(attribute, getattr(self._swagger_location, attribute))

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

        @property
        def get_category(self, category_id=None, category_name=None):

            category_object = None

            if category_id:
                category_object = self._category_id_dict[str(category_id)]
            elif category_name:
                category_object = self._category_name_dict[category_name]

            return category_object

        @property
        def get_item(self, item_id=None, item_name=None):
            item_object = None

            if item_id:
                item_object = self._item_id_dict[str(item_id)]
            elif item_name:
                item_object = self._category_name_dict[item_name]

            return item_object

    @property
    def menu(self):
        self._swagger_menu = self._swagger_location_api.getLocationMenu(self._location_id, self._api_key)

        return self.SDMenu(self._swagger_menu)

class SubtleData(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.api_client = swagger.ApiClient(api_key, config.SD_ENDPOINT)

    def Location(self, location_id):
        return SDLocation(location_id, self.api_client)