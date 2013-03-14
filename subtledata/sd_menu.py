__author__ = 'gsibble'

from base_types import SDFirstClassObject

class SDMenu(SDFirstClassObject):

    def __init__(self, location, swagger_menu, use_cache=True):

        super(SDMenu, self).__init__(location, use_cache)

        #Store parent location
        self._location = location

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