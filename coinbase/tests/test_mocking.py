from decimal import Decimal
import inspect
import unittest
from sure import this

from coinbase import *
from coinbase.mock import *


class CoinbaseAccountMockTests(unittest.TestCase):

    def setUp(self):
        self.account = CoinbaseAccountMock()
        this(len(self.account.transactions())).should.equal(0)

    def test_buy(self):

        # Buy some bitcoin
        transaction_id = self.account.buy_btc('3.5').transaction_id
        this(self.account.get_transaction(transaction_id).status) \
            .should.equal(CoinbaseTransaction.Status.pending)
        this(len(self.account.transactions()),).should.equal(1)
        this(self.account.balance).should.equal(CoinbaseAmount('0', 'BTC'))

        # Complete the transaction
        self.account.mock.complete_transaction(transaction_id)
        this(self.account.get_transaction(transaction_id).status) \
            .should.equal(CoinbaseTransaction.Status.complete)
        this(len(self.account.transactions())).should.equal(1)
        this(self.account.balance).should.equal(CoinbaseAmount('3.5', 'BTC'))

    def test_sell(self):

        self.account.balance = CoinbaseAmount('10', 'BTC')

        # Sell some bitcoin
        transaction_id = self.account.sell_btc('3.5').transaction_id
        this(self.account.get_transaction(transaction_id).status) \
            .should.equal(CoinbaseTransaction.Status.pending)
        this(len(self.account.transactions())).should.equal(1)
        this(self.account.balance).should.equal(CoinbaseAmount('10', 'BTC'))

        # Complete the transaction
        self.account.mock.complete_transaction(transaction_id)
        this(self.account.get_transaction(transaction_id).status) \
            .should.equal(CoinbaseTransaction.Status.complete)
        this(len(self.account.transactions())).should.equal(1)
        this(self.account.balance).should.equal(CoinbaseAmount('6.5', 'BTC'))

    def test_payment_via_button(self):

        self.account.balance = CoinbaseAmount('.02', 'BTC')

        # Set up a button
        button_id = self.account.create_button(CoinbasePaymentButton(
            name='Fuzzy slippers',
            price=CoinbaseAmount('5', 'USD'),
            callback_url='https://example.com/cb',
            custom='pqxrt',
            custom_secure=True,
        )).id

        # Create an order
        order = self.account.mock.create_order_from_button(
            button_id,
            customer=CoinbaseOrder.Customer(email='alice@example.com'),
        )

        # Pay the order, complete the transaction
        callbacks = self.account.mock.accept_payment(
            order.receive_address, '.01')
        order = self.account.get_order(order.id)
        transaction = self.account.get_transaction(order.transaction.id)

        # Verify the resulting state
        this(self.account.balance).should.equal(CoinbaseAmount('.03', 'BTC'))
        this(order.status).should.equal(CoinbaseOrder.Status.complete)
        this(transaction.status).should.equal(
            CoinbaseTransaction.Status.complete)

        # Verify the resulting callback
        this(len(callbacks)).should.equal(1)
        callback_url, callback_body = callbacks[0]
        this(callback_url).should.equal('https://example.com/cb')
        this(CoinbaseOrder.parse_callback(callback_body)).should.equal(order)

    def test_send(self):

        self.account.balance = CoinbaseAmount('.02', 'BTC')

        # Send someone money
        transaction = self.account.send(
            to_address='bob@example.com',
            amount=CoinbaseAmount('5', 'USD'),
            notes='Your refund',
        )
        this(transaction.status).should.equal(
            CoinbaseTransaction.Status.pending)
        this(len(self.account.transactions()),).should.equal(1)
        this(self.account.balance).should.equal(CoinbaseAmount('.02', 'BTC'))

        # Complete the transaction
        transaction = self.account.mock.complete_transaction(transaction.id)
        this(transaction.status).should.equal(
            CoinbaseTransaction.Status.complete)
        this(len(self.account.transactions())).should.equal(1)
        this(self.account.balance).should.equal(CoinbaseAmount('.01', 'BTC'))

    def test_get_exchange_rate(self):
        this(self.account.get_exchange_rate('BTC', 'USD')) \
            .should.equal(Decimal('500'))
        this(self.account.get_exchange_rate('USD', 'BTC')) \
            .should.equal(Decimal('.002'))

    def test_transactions(self):
        self.account.send(amount=CoinbaseAmount('.5', 'BTC'),
                          to_address='alice@example.com')
        self.account.send(amount=CoinbaseAmount('.8', 'BTC'),
                          to_address='bob@example.com')
        this([tx.recipient_address for tx in self.account.transactions()]) \
            .should.equal(['bob@example.com', 'alice@example.com'])


class CoinbaseAccountMockSpecTests(unittest.TestCase):

    def test_account_spec(self):
        a = public_argspecs(CoinbaseAccount)
        b = public_argspecs(CoinbaseAccountMock)
        this(a).should.equal(b)


def public_argspecs(x):
    return dict([(key, inspect.getargspec(value))
                 for key, value in x.__dict__.items()
                 if key[0] != '_' and inspect.isfunction(value)])
