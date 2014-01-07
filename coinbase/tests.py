__author__ = 'gsibble'

import sure
from sure import it, this, those, these
import unittest
from httpretty import HTTPretty, httprettified

from coinbase import CoinbaseAccount, CoinbaseError
from coinbase.models import CoinbaseAmount
from decimal import Decimal

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2014-03-31T23:27:40Z", "access_token": "c15a9f84e471db9b0b8fb94f3cb83f08867b4e00cb823f49ead771e928af5c79", "token_uri": "https://www.coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "c15a9f84e471db9b0b8fb94f3cb83f08867b4e00cb823f49ead771e928af5c79", "token_type": "bearer", "expires_in": 7200, "refresh_token": "90cb2424ddc39f6668da41a7b46dfd5a729ac9030e19e05fd95bb1880ad07e65", "scope": "all"}, "client_id": "2df06cb383f4ffffac20e257244708c78a1150d128f37d420f11fdc069a914fc", "id_token": null, "client_secret": "7caedd79052d7e29aa0f2700980247e499ce85381e70e4a44de0c08f25bded8a", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "90cb2424ddc39f6668da41a7b46dfd5a729ac9030e19e05fd95bb1880ad07e65", "user_agent": null}'''

class CoinBaseAmountTests(unittest.TestCase):

    def setUp(self):
        self.cb_amount = CoinbaseAmount(1, 'BTC')

    def test_cb_amount_class(self):
        this(self.cb_amount).should.be.a(Decimal)
        this(Decimal(self.cb_amount)).should.equal(Decimal('1'))
        this(self.cb_amount.currency).should.equal('BTC')

    def test_cb_amount_equality(self):
        this(CoinbaseAmount(1, 'BTC')).should.equal(CoinbaseAmount(1, 'BTC'))
        this(CoinbaseAmount(1, 'BTC')).doesnt.equal(CoinbaseAmount(1, 'USD'))
        assert CoinbaseAmount(1, 'BTC') == 1

class CoinBaseAPIKeyTests(unittest.TestCase):

    def setUp(self):
        self.account = CoinbaseAccount(api_key='f64223978e5fd99d07cded069db2189a38c17142fee35625f6ab3635585f61ab')

    @httprettified
    def test_api_key_balance(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/account/balance",
                           body='''{"amount":"1.00000000","currency":"BTC"}''',
                           content_type='text/json')

        this(float(self.account.balance)).should.equal(1)

class CoinBaseLibraryTests(unittest.TestCase):

    def setUp(self):
        self.account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)

    @httprettified
    def test_status_error(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/account/balance",
                               body='''{"error": "Invalid api_key"}''',
                               content_type='text/json',
                               status=401)

        try:
            self.account.balance
        except CoinbaseError as e:
            e.error.should.equal("Invalid api_key")
        except Exception:
            assert False

    @httprettified
    def test_success_false(self):
        # Success is added when posting, putting or deleting
        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/account/balance",
                               body='''{"success": false, "errors":["Error 1","Error 2"]}''',
                               content_type='text/json')

        try:
            self.account.balance
        except CoinbaseError as e:
            e.error.should.equal(["Error 1", "Error 2"])
        except Exception:
            assert False

    @httprettified
    def test_retrieve_balance(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/account/balance",
                               body='''{"amount":"0.00000000","currency":"BTC"}''',
                               content_type='text/json')

        this(float(self.account.balance)).should.equal(0.0)
        this(self.account.balance.currency).should.equal('BTC')

    @httprettified
    def test_receive_addresses(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/account/receive_address",
                               body='''{"address" : "1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt"}''',
                               content_type='text/json')

        this(self.account.receive_address).should.equal(u'1DX9ECEF3FbGUtzzoQhDT8CG3nLUEA2FJt')

    @httprettified
    def test_contacts(self):
        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/contacts",
                               body='''{"contacts":[{"contact":{"email":"brian@coinbase.com"}}],"total_count":1,"num_pages":1,"current_page":1}''',
                               content_type='text/json')

        this(self.account.contacts).should.equal([{u'email': u'brian@coinbase.com'}])

    @httprettified
    def test_buy_price_1(self):
        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/prices/buy?qty=1",
                               body='''{"amount":"63.31","currency":"USD"}''',
                               content_type='text/json')

        buy_price_1 = self.account.buy_price(1)
        this(buy_price_1).should.be.a(Decimal)
        this(buy_price_1).should.be.lower_than(100)
        this(buy_price_1.currency).should.equal('USD')

    @httprettified
    def test_buy_price_2(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/prices/buy?qty=10",
                               body='''{"amount":"633.25","currency":"USD"}''',
                               content_type='text/json')

        buy_price_10 = self.account.buy_price(10)
        this(buy_price_10).should.be.greater_than(100)

    @httprettified
    def test_sell_price(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/prices/sell?qty=1",
                               body='''{"amount":"63.31","currency":"USD"}''',
                               content_type='text/json')

        sell_price_1 = self.account.sell_price(1)
        this(sell_price_1).should.be.a(Decimal)
        this(sell_price_1).should.be.lower_than(100)
        this(sell_price_1.currency).should.equal('USD')

    @httprettified
    def test_sell_price_10(self):
        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/prices/sell?qty=1",
                               body='''{"amount":"630.31","currency":"USD"}''',
                               content_type='text/json')

        sell_price_10 = self.account.sell_price(10)
        this(sell_price_10).should.be.greater_than(100)

    @httprettified
    def test_request_bitcoin(self):

        HTTPretty.register_uri(HTTPretty.POST, "https://coinbase.com/api/v1/transactions/request_money",
                               body='''{"success":true,"transaction":{"id":"514e4c37802e1bf69100000e","created_at":"2013-03-23T17:43:35-07:00","hsh":null,"notes":"Testing","amount":{"amount":"1.00000000","currency":"BTC"},"request":true,"status":"pending","sender":{"id":"514e4c1c802e1bef9800001e","email":"george@atlasr.com","name":"george@atlasr.com"},"recipient":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"}}}''',
                               content_type='text/json')

        new_request = self.account.request('george@atlasr.com', 1, 'Testing')

        this(new_request.amount).should.equal(CoinbaseAmount(Decimal(1), 'BTC'))
        this(new_request.request).should.equal(True)
        this(new_request.sender.email).should.equal('george@atlasr.com')
        this(new_request.recipient.email).should.equal('gsibble@gmail.com')
        this(new_request.notes).should.equal('Testing')

    @httprettified
    def test_send_bitcoin(self):

        HTTPretty.register_uri(HTTPretty.POST, "https://coinbase.com/api/v1/transactions/send_money",
                               body='''{"success":true,"transaction":{"id":"5158b227802669269c000009","created_at":"2013-03-31T15:01:11-07:00","hsh":null,"notes":"","amount":{"amount":"-0.10000000","currency":"BTC"},"request":false,"status":"pending","sender":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"},"recipient_address":"15yHmnB5vY68sXpAU9pR71rnyPAGLLWeRP"}}    ''',
                               content_type='text/json')

        new_transaction_with_btc_address = self.account.send('15yHmnB5vY68sXpAU9pR71rnyPAGLLWeRP', amount=0.1)

        this(new_transaction_with_btc_address.amount).should.equal(CoinbaseAmount(Decimal('-0.1'), 'BTC'))
        this(new_transaction_with_btc_address.request).should.equal(False)
        this(new_transaction_with_btc_address.sender.email).should.equal('gsibble@gmail.com')
        this(new_transaction_with_btc_address.recipient).should.equal(None)
        this(new_transaction_with_btc_address.recipient_address).should.equal('15yHmnB5vY68sXpAU9pR71rnyPAGLLWeRP')

        HTTPretty.register_uri(HTTPretty.POST, "https://coinbase.com/api/v1/transactions/send_money",
                               body='''{"success":true,"transaction":{"id":"5158b2920b974ea4cb000003","created_at":"2013-03-31T15:02:58-07:00","hsh":null,"notes":"","amount":{"amount":"-0.10000000","currency":"BTC"},"request":false,"status":"pending","sender":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"},"recipient":{"id":"4efec8d7bedd320001000003","email":"brian@coinbase.com","name":"Brian Armstrong"},"recipient_address":"brian@coinbase.com"}}''',
                               content_type='text/json')

        new_transaction_with_email = self.account.send('brian@coinbase.com', amount=0.1)

        this(new_transaction_with_email.recipient.email).should.equal('brian@coinbase.com')

    @httprettified
    def test_transaction_list(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/transactions",
                               body='''{"current_user":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"},"balance":{"amount":"0.00000000","currency":"BTC"},"total_count":4,"num_pages":1,"current_page":1,"transactions":[{"transaction":{"id":"514e4c37802e1bf69100000e","created_at":"2013-03-23T17:43:35-07:00","hsh":null,"notes":"Testing","amount":{"amount":"1.00000000","currency":"BTC"},"request":true,"status":"pending","sender":{"id":"514e4c1c802e1bef9800001e","email":"george@atlasr.com","name":"george@atlasr.com"},"recipient":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"}}},{"transaction":{"id":"514e4c1c802e1bef98000020","created_at":"2013-03-23T17:43:08-07:00","hsh":null,"notes":"Testing","amount":{"amount":"1.00000000","currency":"BTC"},"request":true,"status":"pending","sender":{"id":"514e4c1c802e1bef9800001e","email":"george@atlasr.com","name":"george@atlasr.com"},"recipient":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"}}},{"transaction":{"id":"514b9fb1b8377ee36500000d","created_at":"2013-03-21T17:02:57-07:00","hsh":"42dd65a18dbea0779f32021663e60b1fab8ee0f859db7172a078d4528e01c6c8","notes":"You gave me this a while ago. It's turning into a fair amount of cash and thought you might want it back :) Building something on your API this weekend. Take care!","amount":{"amount":"-1.00000000","currency":"BTC"},"request":false,"status":"complete","sender":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"},"recipient":{"id":"4efec8d7bedd320001000003","email":"brian@coinbase.com","name":"Brian Armstrong"},"recipient_address":"brian@coinbase.com"}},{"transaction":{"id":"509e01cb12838e0200000224","created_at":"2012-11-09T23:27:07-08:00","hsh":"ac9b0ffbe36dbe12c5ca047a5bdf9cadca3c9b89b74751dff83b3ac863ccc0b3","notes":"","amount":{"amount":"1.00000000","currency":"BTC"},"request":false,"status":"complete","sender":{"id":"4efec8d7bedd320001000003","email":"brian@coinbase.com","name":"Brian Armstrong"},"recipient":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"},"recipient_address":"gsibble@gmail.com"}}]}''',
                               content_type='text/json')

        transaction_list = self.account.transactions()

        this(transaction_list).should.be.a(list)

    @httprettified
    def test_getting_transaction(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/transactions/5158b227802669269c000009",
                               body='''{"transaction":{"id":"5158b227802669269c000009","created_at":"2013-03-31T15:01:11-07:00","hsh":"223a404485c39173ab41f343439e59b53a5d6cba94a02501fc6c67eeca0d9d9e","notes":"","amount":{"amount":"-0.10000000","currency":"BTC"},"request":false,"status":"pending","sender":{"id":"509e01ca12838e0200000212","email":"gsibble@gmail.com","name":"gsibble@gmail.com"},"recipient_address":"15yHmnB5vY68sXpAU9pR71rnyPAGLLWeRP"}}''',
                               content_type='text/json')

        transaction = self.account.get_transaction('5158b227802669269c000009')

        this(transaction.status).should.equal('pending')
        this(transaction.amount).should.equal(CoinbaseAmount(Decimal("-0.1"), "BTC"))

    @httprettified
    def test_getting_user_details(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/users",
                               body='''{"users":[{"user":{"id":"509f01da12837e0201100212","name":"New User","email":"gsibble@gmail.com","time_zone":"Pacific Time (US & Canada)","native_currency":"USD","buy_level":1,"sell_level":1,"balance":{"amount":"1225.86084181","currency":"BTC"},"buy_limit":{"amount":"10.00000000","currency":"BTC"},"sell_limit":{"amount":"50.00000000","currency":"BTC"}}}]}''',
                               content_type='text/json')

        user = self.account.get_user_details()

        this(user.id).should.equal("509f01da12837e0201100212")
        this(user.balance).should.equal(CoinbaseAmount(Decimal("1225.86084181"), "BTC"))

    # The following tests use the example request/responses from the coinbase API docs:
    # test_creating_button, test_creating_order, test_getting_order
    @httprettified
    def test_creating_button(self):
        HTTPretty.register_uri(HTTPretty.POST, "https://coinbase.com/api/v1/buttons",
                               body='''{"success":true,"button":{"code":"93865b9cae83706ae59220c013bc0afd","type":"buy_now","style":"custom_large","text":"Pay With Bitcoin","name":"test","description":"Sample description","custom":"Order123","callback_url":"http://www.example.com/my_custom_button_callback","price":{"cents":123,"currency_iso":"USD"}}}''',
                               content_type='text/json')

        button = self.account.create_button(
            name="test",
            type="buy_now",
            price=1.23,
            currency="USD",
            custom="Order123",
            callback_url="http://www.example.com/my_custom_button_callback",
            description="Sample description",
            style="custom_large",
            include_email=True
        )
        this(button.code).should.equal("93865b9cae83706ae59220c013bc0afd")
        this(button.name).should.equal("test")
        this(button.price).should.equal(CoinbaseAmount(Decimal('1.23'), "USD"))
        this(button.include_address).should.equal(None)

    @httprettified
    def test_creating_order(self):

        HTTPretty.register_uri(HTTPretty.POST, "https://coinbase.com/api/v1/buttons/93865b9cae83706ae59220c013bc0afd/create_order",
                               body='''{"success":true,"order":{"id":"7RTTRDVP","created_at":"2013-11-09T22:47:10-08:00","status":"new","total_btc":{"cents":100000000,"currency_iso":"BTC"},"total_native":{"cents":100000000,"currency_iso":"BTC"},"custom":"Order123","receive_address":"mgrmKftH5CeuFBU3THLWuTNKaZoCGJU5jQ","button":{"type":"buy_now","name":"test","description":"Sample description","id":"93865b9cae83706ae59220c013bc0afd"},"transaction":null}}''',
                               content_type='text/json')

        order = self.account.create_order("93865b9cae83706ae59220c013bc0afd")

        this(order.order_id).should.equal("7RTTRDVP")
        this(order.total_btc).should.equal(CoinbaseAmount(1, 'BTC'))

        this(order.button.button_id).should.equal("93865b9cae83706ae59220c013bc0afd")
        this(order.transaction).should.equal(None)

    @httprettified
    def test_order_list(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/orders",
                               body='''{"orders":[{"order":{"id":"A7C52JQT","created_at":"2013-03-11T22:04:37-07:00","status":"completed","total_btc":{"cents":100000000,"currency_iso":"BTC"},"total_native":{"cents":3000,"currency_iso":"USD"},"custom":"","button":{"type":"buy_now","name":"Order #1234","description":"order description","id":"eec6d08e9e215195a471eae432a49fc7"},"transaction":{"id":"513eb768f12a9cf27400000b","hash":"4cc5eec20cd692f3cdb7fc264a0e1d78b9a7e3d7b862dec1e39cf7e37ababc14","confirmations":0}}}],"total_count":1,"num_pages":1,"current_page":1}''',
                               content_type='text/json')

        orders = self.account.orders()
        this(orders).should.be.a(list)
        this(orders[0].order_id).should.equal("A7C52JQT")

    @httprettified
    def test_getting_order(self):

        HTTPretty.register_uri(HTTPretty.GET, "https://coinbase.com/api/v1/orders/A7C52JQT",
                               body='''{"order":{"id":"A7C52JQT","created_at":"2013-03-11T22:04:37-07:00","status":"completed","total_btc":{"cents":10000000,"currency_iso":"BTC"},"total_native":{"cents":10000000,"currency_iso":"BTC"},"custom":"","button":{"type":"buy_now","name":"test","description":"","id":"eec6d08e9e215195a471eae432a49fc7"},"transaction":{"id":"513eb768f12a9cf27400000b","hash":"4cc5eec20cd692f3cdb7fc264a0e1d78b9a7e3d7b862dec1e39cf7e37ababc14","confirmations":0}}}''',
                               content_type='text/json')

        order = self.account.get_order("A7C52JQT")

        this(order.order_id).should.equal("A7C52JQT")
        this(order.status).should.equal("completed")
        this(order.total_btc).should.equal(CoinbaseAmount(Decimal(".1"), "BTC"))
        this(order.button.name).should.equal("test")
        this(order.transaction.transaction_id).should.equal("513eb768f12a9cf27400000b")

if __name__ == '__main__':
    unittest.main()
