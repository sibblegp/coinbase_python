from coinbase.models import CoinbaseError


def test_coinbase_error_instantiation():
    CoinbaseError("message")
    CoinbaseError("message", ["abc", "def"])
