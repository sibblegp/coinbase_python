__author__ = 'gsibble'

from base_types import SDFirstClassCollection

from sd_user import SDUser

class SDUserCollection(SDFirstClassCollection):

    def __init__(self, parent):
        super(SDUserCollection, self).__init__(parent)

    @property
    def all(self):

        return []


    def get(self, user_id, use_cache=True):
        if not self._use_cache:
            use_cache = False

        return SDUser(self, user_id=user_id, use_cache=use_cache)

    def filter(self, first_name=None):

        return []

    def create(self, first_name):
        pass