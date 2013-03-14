__author__ = 'gsibble'

from base_types import SDFirstClassCollection

from sd_location import SDLocation

class SDLocationCollection(SDFirstClassCollection):

    def __init__(self, parent):
        super(SDLocationCollection, self).__init__(parent)

    def create(self):
        pass

    def get(self, location_id, use_cache=True, include_menu=False):
        if not self._use_cache:
            use_cache = False

        return SDLocation(self, location_id, include_menu, use_cache)