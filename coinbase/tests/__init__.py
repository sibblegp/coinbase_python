__author__ = 'gsibble'

from sure import it, this, those, these
import unittest
from httpretty import HTTPretty, httprettified
from decimal import Decimal
import os.path

from coinbase import CoinbaseAccount, CoinbaseAmount


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


class CoinBaseAmountTests(unittest.TestCase):

    def setUp(self):
        self.cb_amount = CoinbaseAmount('1.063', 'BTC')

    def test_cb_amount_class(self):
        this(Decimal(self.cb_amount)).should.equal(Decimal('1.063'))
        this(self.cb_amount.currency).should.equal('BTC')


class CoinBaseAPIKeyTests(unittest.TestCase):

    def setUp(self):
        self.account = CoinbaseAccount(
            api_key='f64223978e5fd99d07cded069db2189a'
                    '38c17142fee35625f6ab3635585f61ab')

    @httprettified
    def test_api_key_balance(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/account/balance',
            body='{"amount":"1.00000000","currency":"BTC"}',
            content_type='text/json')

        this(self.account.balance).should.equal(CoinbaseAmount('1.0', 'BTC'))


class CoinBaseLibraryTests(unittest.TestCase):

    def setUp(self):
        self.account = CoinbaseAccount(
            oauth2_credentials=read('oauth2_credentials.json'))

    @httprettified
    def test_retrieve_balance(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/account/balance',
            body='{"amount":"0.00000000","currency":"BTC"}',
            content_type='text/json')

        this(self.account.balance).should.equal(
            CoinbaseAmount('0.00000000', 'BTC'))

    @httprettified
    def test_receive_addresses(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/account/receive_address',
            body='{"address":"1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt"}',
            content_type='text/json')

        this(self.account.receive_address).should.equal(
            u'1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt')

    @httprettified
    def test_contacts(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/contacts',
            body=read('contacts.json'),
            content_type='text/json')

        this(self.account.contacts).should.equal([
            {u'email': u'alice@example.com'},
            {u'email': u'bob@example.com'},
            {u'email': u'eve@example.com'},
        ])

    @httprettified
    def test_buy_price_1(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/prices/buy?qty=1',
            body='{"amount":"63.31","currency":"USD"}',
            content_type='text/json')

        this(self.account.buy_price(1)).should.equal(
            CoinbaseAmount('63.31', 'USD'))

    @httprettified
    def test_buy_price_2(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/prices/buy?qty=10',
            body='{"amount":"633.25","currency":"USD"}',
            content_type='text/json')

        this(self.account.buy_price(10)).should.equal(
            CoinbaseAmount('633.25', 'USD'))

    @httprettified
    def test_sell_price(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/prices/sell?qty=1',
            body='{"amount":"63.31","currency":"USD"}',
            content_type='text/json')

        this(self.account.sell_price(1)).should.equal(
            CoinbaseAmount('63.31', 'USD'))

    @httprettified
    def test_sell_price_10(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/prices/sell?qty=1',
            body='{"amount":"630.31","currency":"USD"}',
            content_type='text/json')

        this(self.account.sell_price(10)).should.equal(
            CoinbaseAmount('630.31', 'USD'))

    @httprettified
    def test_request_bitcoin(self):

        HTTPretty.register_uri(
            HTTPretty.POST,
            'https://coinbase.com/api/v1/transactions/request_money',
            body=read('request_btc.json'),
            content_type='text/json')

        request = self.account.request(from_email='alice@example.com',
                                       amount=CoinbaseAmount('1', 'BTC'),
                                       notes='Testing')

        this(request.amount).should.equal(CoinbaseAmount('1', 'BTC'))
        this(request.request).should.equal(True)
        this(request.sender.email).should.equal('alice@example.com')
        this(request.recipient.email).should.equal('bob@example.com')
        this(request.notes).should.equal('Testing')

    @httprettified
    def test_send_bitcoin_to_btc_address(self):

        HTTPretty.register_uri(
            HTTPretty.POST,
            'https://coinbase.com/api/v1/transactions/send_money',
            body=read('send_to_bitcoin_address.json'),
            content_type='text/json')

        tx = self.account.send(to_address='7nregFERfhn8f34FERf8yn8fEGgfe274nv',
                               amount=CoinbaseAmount('0.1', 'BTC'))

        this(tx.amount).should.equal(CoinbaseAmount(Decimal('-0.1'), 'BTC'))
        this(tx.request).should.equal(False)
        this(tx.sender.email).should.equal('alice@example.com')
        this(tx.recipient).should.equal(None)
        this(tx.recipient_address).should.equal(
            '7nregFERfhn8f34FERf8yn8fEGgfe274nv')

    @httprettified
    def test_send_bitcoin_to_email_address(self):

        HTTPretty.register_uri(
            HTTPretty.POST,
            'https://coinbase.com/api/v1/transactions/send_money',
            body=read('send_to_email_address.json'),
            content_type='text/json')

        tx = self.account.send(to_address='bob@example.com',
                               amount=CoinbaseAmount('0.1', 'BTC'))

        this(tx.recipient.email).should.equal('bob@example.com')

    @httprettified
    def test_transaction_list(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/transactions',
            body=read('transactions.json'),
            content_type='text/json')

        transaction_list = self.account.transactions()

        this(transaction_list).should.be.an(list)

    @httprettified
    def test_getting_transaction(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/transactions/5158b227802669269c000009',
            body=read('transaction.json'),
            content_type='text/json')

        transaction = self.account.get_transaction('5158b227802669269c000009')

        this(transaction.status).should.equal('pending')
        this(transaction.amount).should.equal(CoinbaseAmount('-0.1', 'BTC'))

    @httprettified
    def test_getting_user_details(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            'https://coinbase.com/api/v1/users',
            body=read('users.json'),
            content_type='text/json')

        user = self.account.get_user_details()

        this(user.id).should.equal("509f01da12837e0201100212")
        this(user.balance).should.equal(CoinbaseAmount('1225.86084181', 'BTC'))

    @httprettified
    def test_creating_a_button(self):

        HTTPretty.register_uri(
            HTTPretty.POST,
            'https://coinbase.com/api/v1/buttons',
            body=read('button.json'),
            content_type='text/json')

        button = self.account.create_button(
            name='Test Button',
            price=CoinbaseAmount('20.00', 'USD'))

        this(button.code).should.equal('f68a5c68d0a68679a6c6f569e651d695')
        this(button.name).should.equal('Test Button')
        this(button.price).should.equal(CoinbaseAmount('20', 'USD'))

    @httprettified
    def test_exchange_rates(self):

        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://coinbase.com/api/v1/currencies/exchange_rates",
            body=read('exchange_rates.json'),
            content_type='text/json')

        rates = self.account.exchange_rates
        this(rates['gbp_to_usd']).should.be.equal(Decimal('1.648093'))
        this(rates['usd_to_btc']).should.be.equal(Decimal('0.002'))
        this(rates['btc_to_usd']).should.be.equal(Decimal('499.998'))
        this(rates['bdt_to_btc']).should.be.equal(Decimal('0.000026'))
