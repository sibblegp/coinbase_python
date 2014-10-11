__author__ = 'kroberts'


class CoinbaseError(Exception):

    def __init__(self, message, errors=None):
        super(CoinbaseError, Exception).__init__(self, ' '.join([message] + (errors or [])))
