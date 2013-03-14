__author__ = 'gsibble'

from base_types import SDFirstClassObject, SDInterface

class SDGeneralInterface(SDInterface):

    def __init__(self, parent):
        super(SDGeneralInterface, self).__init__(parent)

    @property
    def states(self):
        states = self._swagger_general_api.getAllStates(self._api_key)
        return states

