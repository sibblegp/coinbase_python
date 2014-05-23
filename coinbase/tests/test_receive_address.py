from sure import this
from unittest import TestCase

from . import account_setup
from .http_mocking import *


@with_http_mocking
class ReceiveAddressTest(TestCase):

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/account/receive_address',
                  response_body)

    def test_receive_addresses_with_key(self):
        account = account_setup.with_key()
        this(account.receive_address).should.equal(expected_receive_address)
        this(last_request_params()).should.equal({
            'api_key': [account_setup.api_key],
        })

    def test_receive_addresses_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.receive_address).should.equal(expected_receive_address)
        this(last_request_params()).should.equal({})


response_body = """
{
    "address":"1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt"
}
"""


expected_receive_address = '1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt'
