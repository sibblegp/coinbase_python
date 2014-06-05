from sure import this
from unittest import TestCase

from datetime import datetime
from dateutil.tz import tzoffset

from coinbase import CoinbaseAmount, CoinbaseTransfer
from . import account_setup
from .http_mocking import *


@with_http_mocking
class TransferTest(TestCase):
    """
    The example from the API doc
    https://coinbase.com/api/doc/1.0/transfers/index.html
    """

    def setUp(self):
        mock_http('GET https://coinbase.com/api/v1/transfers',
                  response_body)

    def test_transfers_with_oauth(self):
        account = account_setup.with_oauth()
        this(account.transfers()).should.equal([expected_transfer])


response_body = """
{
  "transfers": [
    {
      "transfer": {
        "type": "Buy",
        "code": "QPCUCZHR",
        "created_at": "2013-02-27T23:28:18-08:00",
        "fees": {
          "coinbase": {
            "cents": 14,
            "currency_iso": "USD"
          },
          "bank": {
            "cents": 15,
            "currency_iso": "USD"
          }
        },
        "payout_date": "2013-03-05T18:00:00-08:00",
        "transaction_id": "5011f33df8182b142400000e",
        "status": "Pending",
        "btc": {
          "amount": "1.00000000",
          "currency": "BTC"
        },
        "subtotal": {
          "amount": "13.55",
          "currency": "USD"
        },
        "total": {
          "amount": "13.84",
          "currency": "USD"
        },
        "description": "Paid for with $13.84 from Test xxxxx3111."
      }
    }
  ],
  "total_count": 1,
  "num_pages": 1,
  "current_page": 1
}
"""


expected_transfer = CoinbaseTransfer(
    type='Buy',
    code='QPCUCZHR',
    created_at=datetime(2013, 2, 27, 23, 28, 18,
                        tzinfo=tzoffset(None, -28800)),
    fees_coinbase=CoinbaseAmount('.14', 'USD'),
    fees_bank=CoinbaseAmount('.15', 'USD'),
    payout_date=datetime(2013, 3, 5, 18, 0, 0,
                         tzinfo=tzoffset(None, -28800)),
    transaction_id='5011f33df8182b142400000e',
    status=CoinbaseTransfer.Status.pending,
    btc_amount=CoinbaseAmount('1', 'BTC'),
    subtotal_amount=CoinbaseAmount('13.55', 'USD'),
    total_amount=CoinbaseAmount('13.84', 'USD'),
    description='Paid for with $13.84 from Test xxxxx3111.',
)
