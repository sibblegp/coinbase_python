from sure import this
from unittest import TestCase

from coinbase import CoinbaseContact
from . import account_setup
from .http_mocking import *


@with_http_mocking
class ContactsTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/contacts',
                  response_body)

    def test_contacts_with_key(self):
        account = account_setup.with_key()
        this(account.contacts()).should.equal(expected_contacts)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })

    def test_contacts_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.contacts()).should.equal(expected_contacts)
        this(last_request_params()).should.equal({})


response_body = """
{
    "contacts": [
        {
            "contact": {
                "email": "alice@example.com"
            }
        },
        {
            "contact": {
                "email": "bob@example.com"
            }
        },
        {
            "contact": {
                "email": "eve@example.com"
            }
        }
    ],
    "current_page": 1,
    "num_pages": 1,
    "total_count": 3
}
"""


expected_contacts = [
    CoinbaseContact(email='alice@example.com'),
    CoinbaseContact(email='bob@example.com'),
    CoinbaseContact(email='eve@example.com'),
]
