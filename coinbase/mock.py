from collections import namedtuple
import datetime
from decimal import Decimal
import random
import string

from coinbase.models import *


class CoinbaseAccountMock(object):
    """
    This class has the same attributes as CoinbaseAccount and mimics its
    behavior of Coinbase without actually using Coinbase. Use it to test
    an application without requiring real money.
    """

    def __init__(self):

        self._buy_price = Decimal('510')
        self._sell_price = Decimal('490')

        self._me = CoinbaseContact(id='2346178248353',
                                   name='Me', email='me@example.com')

        self._transactions = {}  # transaction id -> CoinbaseTransaction
        self._transaction_ids = []  # transaction ids in creation order
        self._transfers = {}  # transaction id -> CoinbaseTransfer
        self._transfer_ids = []  # transaction ids in creation order
        self._buttons = {}  # button id -> CoinbasePaymentButton
        self._orders = {}  # order id -> CoinbaseOrder
        self._order_ids = []  # order ids in creation order
        self._orders_by_address = {}  # receive address -> CoinbaseOrder.id
        self._orders_by_custom = {}  # button custom string -> CoinbaseOrder.id

        self.authenticated = True
        self.auth = None
        self.allow_transfers = True

        self.balance = CoinbaseAmount('0', 'BTC')
        self.receive_address = random_bitcoin_address()
        self.exchange_rates = {
            'usd_to_btc': Decimal('0.002'),
            'btc_to_usd': Decimal('500'),
        }

        self.mock = MockControl(account=self)

    def get_exchange_rate(self, from_currency, to_currency):
        return self.exchange_rates['{}_to_{}'.format(
            from_currency.lower(),
            to_currency.lower()
        )]

    def contacts(self, page=None, limit=None, query=None):
        raise NotImplementedError  # todo

    def buy_price(self, qty=1):
        return CoinbaseAmount(qty * self._buy_price, 'USD')

    def sell_price(self, qty=1):
        return CoinbaseAmount(qty * self._sell_price, 'USD')

    def buy_btc(self, qty, pricevaries=False):
        now = get_now()

        transaction = CoinbaseTransaction(
            id=random_transaction_id(),
            created_at=now,
            amount=CoinbaseAmount(qty, 'BTC'),
            status=CoinbaseTransaction.Status.pending,
        )
        transfer = CoinbaseTransfer(
            transaction_id=transaction.id,
            created_at=now,
        )

        self.mock.add_transaction(transaction)
        self.mock.add_transfer(transfer)

        return transfer

    def sell_btc(self, qty):
        return self.buy_btc(qty=-Decimal(qty))

    def request(self, from_email, amount, notes=''):
        raise NotImplementedError  # todo

    def send(self, to_address, amount, notes='', user_fee=None, idem=None):
        transaction = CoinbaseTransaction(
            id=random_transaction_id(),
            created_at=get_now(),
            notes=notes,
            amount=amount,
            status=CoinbaseTransaction.Status.pending,
            request=False,
            sender=self._me,
            recipient=None,  # todo
            recipient_address=to_address,
            recipient_type='coinbase' if '@' in to_address else 'bitcoin',
        )
        self.mock.add_transaction(transaction)
        return transaction

    def transactions(self, count=30):
        return [self._transactions[i] for i in
                list(reversed(self._transaction_ids))[:count]]

    def transfers(self, count=30):
        raise [self._transfers[i] for i in
               list(reversed(self._transfer_ids))[:count]]

    def get_transaction(self, transaction_id):
        return self._transactions[transaction_id]

    def get_user_details(self):
        raise NotImplementedError  # todo

    def generate_receive_address(self, callback_url=None):
        raise NotImplementedError  # todo

    def create_button(self, button, account_id=None):
        id = random_button_id()
        button = button._replace(
            id=id,
            type=button.type or 'buy_now',
            style=button.style or 'buy_now_large',
            text=button.text or 'Pay With Bitcoin',
            custom_secure=bool(button.custom_secure),
        )
        self._buttons[id] = button
        return button

    def orders(self, account_id=None, page=None):
        # todo - paging
        return [self._orders[i] for i in
                list(reversed(self._order_ids))]

    def get_order(self, id_or_custom_field, account_id=None):
        order = self._orders.get(id_or_custom_field)
        if order:
            return order
        order_id = self._orders_by_custom.get(id_or_custom_field)
        if order_id:
            return self._orders.get(order_id)

    def create_button_and_order(self, button):
        button_id = self.create_button(button).id
        return self.create_order_from_button(button_id)

    def create_order_from_button(self, button_id):
        button = self.mock.get_button(button_id)
        order = CoinbaseOrder(
            id=random_order_id(),
            created_at=get_now(),
            status=CoinbaseOrder.Status.pending,
            receive_address=random_bitcoin_address(),
            button=CoinbaseOrder.Button.from_coinbase_payment_button(button),
            custom=button.custom,
            total=self.mock.btc_and_native(button.price),
        )
        self.mock.add_order(order)
        return order


class MockControl(namedtuple('CoinbaseAccount_MockControl', 'account')):

    def complete_transaction(self, transaction_id):

        transaction = self.modify_transaction(
            transaction_id, status=CoinbaseTransaction.Status.complete)

        if transaction_id in self.account._transfers:
            self.modify_transfer(transaction_id,
                                 status=CoinbaseTransfer.Status.complete)

        send = (transaction.sender is not None and
                transaction.sender.id == self.account._me.id)

        amount_btc = self.convert_amount(transaction.amount, 'BTC').amount
        account_amount = self.account.balance.amount
        self.account.balance = self.account.balance._replace(
                amount=account_amount + amount_btc * (-1 if send else 1))

        return transaction

    def create_order_from_button(self, button_id, customer=None,
                                 refund_address=None):
        """
        customer - CoinbaseOrder.Customer
        refund_address - bitcoin addresss
        """
        order_id = self.account.create_order_from_button(button_id).id
        return self.modify_order(order_id, customer=customer,
                                 refund_address=refund_address)

    def accept_payment(self, receive_address, amount_btc):
        """
        receive_address - bitcoin address
        amount_btc - Decimal

        Returns a list of Callback
        """

        callbacks = []

        now = get_now()

        amount_btc = Decimal(amount_btc)
        amount_usd = amount_btc * self.account.exchange_rates['btc_to_usd']
        amount = CoinbaseAmount.BtcAndNative(
            btc=CoinbaseAmount(amount_btc, 'BTC'),
            native=CoinbaseAmount(amount_usd, 'USD'),
        )

        self.account.balance = self.account.balance._replace(
                amount=self.account.balance.amount + amount_btc)

        transaction = CoinbaseTransaction(
            id=random_transaction_id(),
            created_at=now,
            amount=amount.btc,
            status=CoinbaseTransaction.Status.complete,
        )

        self.account.mock.add_transaction(transaction)

        order_id = self.account._orders_by_address.get(receive_address)
        if order_id is not None:

            order = self.account._orders[order_id]
            button = self.account._buttons[order.button.id]

            # I'm not actually sure when the transaction field gets updated.
            order = self.modify_order(
                order_id,
                transaction=CoinbaseOrder.Transaction(
                    id=transaction.id,
                    hash=None,
                    confirmations=0,
                )
            )

            if order.status == CoinbaseOrder.Status.pending:
                amount_is_correct = amount.btc == order.total.btc
                status = (CoinbaseOrder.Status.complete if amount_is_correct
                          else CoinbaseOrder.Status.mispaid)
                order = self.modify_order(order.id, status=status)

            if order.status in [CoinbaseOrder.Status.mispaid,
                                CoinbaseOrder.Status.expired]:
                order = self.modify_order(order.id, mispaid=amount)

            if button.callback_url is not None:
                callbacks.append(Callback(
                    url=button.callback_url,
                    body=order.render_callback(),
                ))

        return callbacks

    def add_transaction(self, transaction):
        self.account._transactions[transaction.id] = transaction
        self.account._transaction_ids.append(transaction.id)

    def add_transfer(self, transfer):
        self.account._transfers[transfer.transaction_id] = transfer
        self.account._transfer_ids.append(transfer.transaction_id)

    def add_order(self, order):
        self.account._orders[order.id] = order
        self.account._orders_by_address[order.receive_address] = order.id
        if order.custom:
            self.account._orders_by_custom[order.custom] = order.id
        self.account._order_ids.append(order.id)

    def modify_transaction(self, transaction_id, **kwargs):
        transaction = self.account._transactions[transaction_id]
        transaction = transaction._replace(**kwargs)
        self.account._transactions[transaction_id] = transaction
        return transaction

    def modify_transfer(self, transaction_id, **kwargs):
        transfer = self.account._transfers[transaction_id]
        transfer = transfer._replace(**kwargs)
        self.account._transfers[transaction_id] = transfer
        return transfer

    def modify_order(self, order_id, **kwargs):
        order = self.account._orders[order_id]
        order = order._replace(**kwargs)
        self.account._orders[order_id] = order
        return order

    def get_button(self, button_id):
        return self.account._buttons[button_id]

    def convert_amount(self, amount, currency):
        if amount.currency == currency:
            return amount
        return amount.convert(
            currency=currency,
            exchange_rate=self.account.get_exchange_rate(
                from_currency=amount.currency,
                to_currency=currency
            )
        )

    def btc_and_native(self, amount, preferred_native_currency='USD'):
        native_currency = (amount.currency if amount.currency != 'BTC'
                           else preferred_native_currency)
        return CoinbaseAmount.BtcAndNative(
            btc=self.convert_amount(amount, 'BTC'),
            native=self.convert_amount(amount, native_currency),
        )


Callback = namedtuple('Callback', 'url body')


def get_now():
    return floor_second(datetime.datetime.now())


def floor_second(x):
    return x - datetime.timedelta(microseconds=x.microsecond)


def random_string(length, chars):
    return ''.join((random.choice(chars) for _ in range(length)))


def random_transaction_id():
    return random_string(24, string.hexdigits[:16])


def random_button_id():
    return random_string(32, string.hexdigits[:16])


def random_order_id():
    return random_string(8, string.digits + string.ascii_uppercase)


def random_bitcoin_address():
    return random_string(34, string.ascii_letters + string.digits)
