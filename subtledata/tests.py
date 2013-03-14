__author__ = 'gsibble'

import sure
from sure import it, this, those, these
import unittest
from subtledata import SubtleData
from api import swagger

from subtledata import sd_collections_general, sd_collections_tickets, sd_collections_locations, sd_collections_users

from subtledata import sd_location, sd_menu, sd_table, sd_ticket, sd_user

class SDTestCase(unittest.TestCase):
    
    def setUp(self):
        self.SD = SubtleData('abcd', use_cache=False)

class SubtleDataObjectTests(SDTestCase):

    def test_SD_object(self):
        this(self.SD.api_key).should.equal('abcd')
        this(self.SD._use_cache).should.equal(False)

        self.SD = SubtleData('1234', use_cache=True)
        this(self.SD.api_key).should.equal('1234')
        this(self.SD._use_cache).should.equal(True)

        this(self.SD._api_client).should.be.an(swagger.ApiClient)
        this(self.SD.Locations).should.be.an(sd_collections_locations.SDLocationCollection)
        this(self.SD.General).should.be.an(sd_collections_general.SDGeneralInterface)
        this(self.SD.Tickets).should.be.an(sd_collections_tickets.SDTicketCollection)
        this(self.SD.Users).should.be.an(sd_collections_users.SDUserCollection)

class GeneralInterfaceTests(SDTestCase):

    def test_states(self):
        this(self.SD.General.states).should.be.an(list)

    def test_countries(self):
        this(self.SD.General.countries).should.be.an(list)

    def test_languages(self):
        this(self.SD.General.languages).should.be.an(list)

class LocationCollectionTests(SDTestCase):

    def test_get_location(self):
        this(self.SD.Locations.get(123)).should.be.an(sd_location.SDLocation)

    def test_filter_location(self):
        this(self.SD.Locations.filter(name='Test')).should.be.an(list)

    def test_all_locations(self):
        this(self.SD.Locations.all).should.be.an(list)

    def test_create_location(self):
        this(self.SD.Locations.create()).should.be.an(sd_location.SDLocation)

class TicketCollectionTests(SDTestCase):

    def test_get_ticket(self):
        this(self.SD.Tickets.get(1234)).should.be.an(sd_ticket.SDTicket)

class UserCollectionTests(SDTestCase):

    def test_all_users(self):
        this(self.SD.Users.all).should.be.an(list)

    def test_get_user(self):
        this(self.SD.Users.get(1234)).should.be.an(sd_user.SDUser)

    def test_create_user(self):
        this(self.SD.Users.create(first_name='Test')).should.be.an(sd_user.SDUser)

    def test_filter_users(self):
        this(self.SD.Users.filter(first_name='Test')).should.be.an(list)

class SDLocationTests(SDTestCase):

    def setUp(self):
        super(SDLocationTests, self).__init__()
        self.Location = self.SD.Locations.get(1234)

    def test_initial_location_attributes(self):
        this(self.Location.id).should.equal(1234)
        this(self.Location.revenue_centers).should.be.an(list)
        this(self.Location.tip_values).should.be.an(list)
        this(self.Location.discount_types).should.be.an(list)
        this(self.Location.terminals).should.be.an(list)
        #TODO:  More attribs

    def test_location_tables(self):
        this(self.Location.tables).should.be.an(list)
        this(self.Location.open_tables).should.be.an(list)

    def test_location_menu(self):
        this(self.Location.menu).should.be.an(sd_menu.SDMenu)

    def test_check_update_menu(self):
        this(self.Location).should.have.property('update_menu')
        #TODO:  Check for updating the menu somehow

    def test_delete(self):
        this(self.Location.delete()).should.equal(None)

    def test_open_tickets(self):
        this(self.Location.tickets.open).should.be.an(list)
        this(self.Location.tickets.filter()).should.be.an(list)

    def test_fetching_ticket(self):
        this(self.Location.tickets.get_with_pos_id(9876)).should.be.an(sd_ticket.SDTicket)

    def test_create_tickets9