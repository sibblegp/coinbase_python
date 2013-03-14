"""
Subtledata Python Client Library

AUTHOR

George Sibble
Chief Software Architect
Subtledata, Inc.
george.sibble@subtledata.com
Github:  sibblegp


************TO USE************

LICENSE (The MIT License)

Copyright (c) 2013 Subtledata, Inc. "code@subtledata.com"

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

__author__ = 'gsibble'

import config

from api import swagger

from base_types import SDFirstClassObject

from sd_collections_locations import SDLocationCollection
from sd_collections_users import SDUserCollection
from sd_collections_general import SDGeneralInterface
from sd_collections_tickets import SDTicketCollection


class SubtleData(object):

    def __init__(self, api_key, use_cache=True, testing=False, internal_debug=True):
        self.api_key = api_key
        self._use_cache = use_cache
        self._internal_debug = internal_debug

        if not testing:
            self._api_client = swagger.ApiClient(api_key, config.SD_ENDPOINT)
        else:
            self._api_client = swagger.ApiClient(api_key, config.SD_TESTING_ENDPOINT)

        self.Locations = SDLocationCollection(self)
        self.Users = SDUserCollection(self)
        self.Tickets = SDTicketCollection(self)
        self.General = SDGeneralInterface(self)