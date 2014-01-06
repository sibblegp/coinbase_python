__author__ = 'vkhougaz'

from amount import CoinbaseAmount

class CoinbaseButton(object):

    def __init__(self, button):
        self.data = button
        # Sometimes it's called code (create button) and sometimes id (sub item of create button)
        # so we map them together
        if 'id' in button:
            self.button_id = button['id']
        if 'code' in button:
            self.button_id = button['code']
        self.code = self.button_id

        self.name = button['name']
        if 'price' in button:
            price_cents = button['price']['cents']
            price_currency_iso = button['price']['currency_iso']
            self.price = CoinbaseAmount.from_cents(price_cents, price_currency_iso)
        else:
            self.price = None
        self.type = button.get('type', None)
        self.style = button.get('style', None)
        self.text = button.get('text', None)
        self.description = button.get('description', None)
        self.custom = button.get('custom', None)
        self.callback_url = button.get('callback_url', None)
        self.success_url = button.get('success_url', None)
        self.cancel_url = button.get('cancel_url', None)
        self.info_url = button.get('info_url', None)
        self.variable_price = button.get('variable_price', None)
        self.choose_price = button.get('choose_price', None)
        self.include_address = button.get('include_address', None)
        self.include_email = button.get('include_email', None)
        self.price1 = button.get('price1', None)
        self.price2 = button.get('price2', None)
        self.price3 = button.get('price3', None)
        self.price4 = button.get('price4', None)
        self.price5 = button.get('price4', None)
