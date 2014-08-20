from decimal import Decimal

from .util import namedtuple, optional

from . import CoinbaseAmount


class CoinbasePaymentButton(namedtuple(
    'CoinbasePaymentButton',
    optional='id type repeat style text name description custom custom_secure '
             'callback_url success_url cancel_url info_url '
             'price auto_redirect suggested_prices include_address '
             'include_email variable_price'
)):
    """
    name
            The name of the item for which you are collecting bitcoin.
            For example, "Acme Order #123" or "Annual Pledge Drive"
    price
            Price as CoinbaseAmount
    type
            One of "buy_now", "donation", and "subscription". Default is
            "buy_now"
    repeat
            Required if `type` is subscription. Must be one of: never,
            daily, weekly, every_two_weeks, monthly, quarterly, yearly
    style
            One of: buy_now_large, buy_now_small, donation_large,
            donation_small, subscription_large, subscription_small,
            custom_large, custom_small, none. Default is buy_now_large
    text
            Allows you to customize the button text on custom_large and
            custom_small styles. Default is "Pay With Bitcoin"
    description
            Longer description of the item in case you want it added to the
            user's transaction notes
    custom
            An optional custom parameter. Usually an Order, User, or Product
            ID corresponding to a record in your database
    custom_secure
            Set this to true to prevent the custom parameter from being
            viewed or  modified after the button has been created. Defaults
            to false
    callback_url
            A custom callback URL specific to this button
    success_url
            A custom success URL specific to this button. The user will
            be redirected to this URL after a successful payment
    cancel_url
            A custom cancel URL specific to this button. The user will be
            redirected to this URL after a canceled order
    info_url
            A custom info URL specific to this button. Displayed to the
            user after a successful purchase for sharing
    auto_redirect
            Auto-redirect users to success or cancel url after payment
            (cancel url if the user pays the wrong amount)
    variable_price
            Allow users to change the price on the generated button
    include_address
            Collect shipping address from customer (not for use with inline
            iframes)
    include_email
            Collect email address from customer (not for use with inline
            iframes)
    suggested_prices
            Some suggested prices to show (Decimal, at most 5)
    """

    @classmethod
    def from_coinbase_dict(cls, x):

        kwargs = {
            'id': x.get('code'),
        }

        for key in ['auto_redirect', 'callback_url', 'cancel_url', 'custom',
                    'custom_secure', 'description', 'info_url', 'name', 'style',
                    'success_url', 'text', 'type', 'repeat', 'variable_price',
                    'include_email', 'include_address']:
            kwargs[key] = x.get(key)

        if x.get('choose_price'):
            prices = []
            for i in range(1, 6):
                s = x.get('price' + str(i))
                if s is not None:
                    prices.append(Decimal(s))
            kwargs['suggested_prices'] = prices

        kwargs['price'] = optional(CoinbaseAmount.from_coinbase_dict)(
            x.get('price'))

        return CoinbasePaymentButton(**kwargs)

    def to_coinbase_dict(self):

        x = {}

        if self.id is not None:
            x['code'] = str(self.id)

        for key in ['type', 'style', 'text', 'name', 'description', 'custom',
                    'callback_url', 'success_url', 'cancel_url', 'info_url',
                    'repeat']:
            value = getattr(self, key)
            if value is not None:
                x[key] = str(value)

        for key in ['auto_redirect', 'include_email', 'include_address',
                    'variable_price', 'custom_secure']:
            value = getattr(self, key)
            if value is not None:
                x[key] = bool(value)

        if self.price is not None:
            x['price_string'] = str(self.price.amount)
            x['price_currency_iso'] = str(self.price.currency)

        if self.suggested_prices is not None:
            x['choose_price'] = True
            for i, price in zip(range(1, 6), self.suggested_prices):
                x['price{}'.format(i)] = str(price)

        return x
