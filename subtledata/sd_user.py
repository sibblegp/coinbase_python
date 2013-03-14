__author__ = 'gsibble'

from base_types import SDFirstClassObject

class SDUser(SDFirstClassObject):
    def __init__(self, parent, user_id=False, user_name=None, use_cache=True, *args, **kwargs):
        super(SDUser, self).__init__(parent, use_cache)

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