class CoinbaseOrder(object):

    def __init__(self, order_id, created_at, status, receive_address,
                 button, transaction=None, custom=None,
                 total_btc=None, total_native=None,
                 mispaid_btc=None, mispaid_native=None):

        self.order_id = order_id
        self.created_at = created_at
        self.status = status
        self.receive_address = receive_address
        self.button = button,
        self.transaction = transaction
        self.custom = custom
        self.total_btc = total_btc
        self.total_native = total_native
        self.mispaid_btc = mispaid_btc
        self.mispaid_native = mispaid_native
