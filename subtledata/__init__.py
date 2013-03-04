__author__ = 'gsibble'

import config

from api import swagger

from api.LocationsApi import LocationsApi
from api.UsersApi import UsersApi
from api.TicketsApi import TicketsApi

import exceptions as E


class SDFirstClassObject(object):
    def __init__(self, api_client, use_cache=True, *args, **kwargs):
        self._api_key = api_client.apiKey
        self._api_client = api_client
        self._use_cache = use_cache
        self._swagger_location_api = LocationsApi(self._api_client)
        self._swagger_users_api = UsersApi(self._api_client)
        self._swagger_tickets_api = TicketsApi(self._api_client)


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
        self._swagger_location = self._swagger_location_api.getLocation(location_id, self._api_key,
                                                                        use_cache=self._use_cache)

        #Set attributes of first class Location to match Swagger Location object
        for attribute in self._swagger_location.swaggerTypes:
            self.__setattr__(attribute, getattr(self._swagger_location, attribute))

        if include_menu:
            self.update_menu(use_cache)

    def update_menu(self, use_cache=True):

        if not self._use_cache:
            use_cache = False

        self._swagger_menu = self._swagger_location_api.getLocationMenu(self._location_id, self._api_key,
                                                                        use_cache=use_cache)

    @property
    def menu(self):

        if not hasattr(self, '_swagger_menu'):
            self.update_menu()

        return self.SDMenu(self._swagger_menu)

    def open_ticket_for_dine_in(self, user_id):

        #Return a SDTicket
        pass

    def open_ticket_for_take_out(self, user_id):

        #Return a SDTicket
        pass

    def open_ticket_for_delivery(self, user_id):

        #Return a SDTicket
        pass


class SDUser(SDFirstClassObject):
    def __init__(self, api_client, user_id=False, user_name=None, use_cache=True, *args, **kwargs):
        super(SDUser, self).__init__(api_client, use_cache)

        if user_id is not None:
            self._swagger_user = self._swagger_users_api.getUser(user_id, self._api_key, use_cache=self._use_cache)
        elif user_name is not None:
            self._swagger_user = self._swagger_users_api.searchUsersByName(user_name, self._api_key,
                                                                           use_cache=self._use_cache)
        else:
            self._swagger_user = None

        if self._swagger_user is not None:
            for attribute in self._swagger_user.swaggerTypes:
                self.__setattr__(attribute, getattr(self._swagger_user, attribute))

    def update_info(self):
        pass


class SDTicket(SDFirstClassObject):
    def __init__(self, api_client, ticket_id, user_id=None, *args, **kwargs):
        super(SDTicket, self).__init__(api_client, False)

        self._swagger_ticket = self._swagger_tickets_api.getTicket(ticket_id, user_id)

        if self._swagger_ticket is not None:
            for attribute in self._swagger_ticket.swaggerTypes:
                self.__setattr__(attribute, getattr(self._swagger_ticket, attribute))

    def add_items_to_order(self, item_id, quantity, instructions=None, modifiers=None):

        if hasattr(self, 'user_id') and hasattr(self, 'ticket_id'):
            if self.user_id is not None and self.ticket_id is not None:
                post_body = {
                    'item_id': item_id,
                    'quantity': quantity,

                }

                if instructions is not None:
                    post_body['instructions'] = instructions

                if modifiers is not None:
                    post_body['modifiers'] = modifiers

                returned_status = self._swagger_tickets_api.addItemsToOrder(self.ticket_id, self.user_id, self._api_key,
                                                                            post_body)

                return returned_status

            else:
                raise E.NoUserSetOnTicket
        else:
            raise E.NoUserSetOnTicket

    def submit_order(self):

        if hasattr(self, 'user_id') and hasattr(self, 'ticket_id'):
            if self.user_id is not None and self.ticket_id is not None:

                returned_status = self._swagger_tickets_api.submitOrder(self.ticket_id, self.user_id, self._api_key,
                                                                        body={})

                return returned_status
            else:
                raise E.NoUserSetOnTicket
        else:
            raise E.NoUserSetOnTicket


class SubtleData(object):
    class _SDFirstClassCollection(object):

        def __init__(self, parent, *args, **kwargs):
            self._api_key = parent.api_key
            self._use_cache = parent._use_cache
            self._api_client = parent._api_client

    class _SDLocationCollection(_SDFirstClassCollection):

        def __init__(self, parent):
            super(SubtleData._SDLocationCollection, self).__init__(parent)

        def create(self):
            pass

        def get(self, location_id, use_cache=True, include_menu=False):
            if not self._use_cache:
                use_cache = False

            return SDLocation(location_id, self._api_client, include_menu, use_cache)

    class _SDUserCollection(_SDFirstClassCollection):

        def __init__(self, parent):
            super(SubtleData._SDUserCollection, self).__init__(parent)

        def create(self):
            pass

        def get(self, user_id, use_cache=True):
            if not self._use_cache:
                use_cache = False

            return SDUser(self._api_client, user_id=user_id, use_cache=use_cache)

        def get_with_name(self, user_name, use_cache=True):
            if not self._use_cache:
                use_cache = False

            return SDUser(self._api_client, user_name=user_name, use_cache=use_cache)

    class _SDTicketCollection(_SDFirstClassCollection):

        def __init__(self, parent):
            super(SubtleData._SDTicketCollection, self).__init__(parent)

        def get(self, ticket_id, user_id=None):
            return SDTicket(self._api_client, ticket_id=ticket_id, user_id=user_id)

        def get_with_pos_id(self, pos_id):
            pass

    def __init__(self, api_key, use_cache=True):
        """

        :param api_key: Subtledata API Key
        :param use_cache: Use Subtledata's Redis Caching layer to accelerate delivery of results.  This specific setting is global to all calls for this API object.
        """
        self.api_key = api_key
        self._use_cache = use_cache
        self._api_client = swagger.ApiClient(api_key, config.SD_ENDPOINT)
        self.Locations = SubtleData._SDLocationCollection(self)
        self.Users = SubtleData._SDTicketCollection(self)
        self.Tickets = SubtleData._SDTicketCollection(self)
