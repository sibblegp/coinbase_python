__author__ = 'gsibble'

from base_types import SDFirstClassCollection

from sd_user import SDUser

class SDUserCollection(SDFirstClassCollection):

    def __init__(self, parent):
        super(SDUserCollection, self).__init__(parent)

    def create(self):
        pass

    def get(self, user_id, use_cache=True):
        if not self._use_cache:
            use_cache = False

        return SDUser(self, user_id=user_id, use_cache=use_cache)

    def get_with_name(self, user_name, use_cache=True):
        if not self._use_cache:
            use_cache = False

        return SDUser(self, user_name=user_name, use_cache=use_cache)