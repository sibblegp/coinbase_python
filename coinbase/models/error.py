__author__ = 'kroberts'

class CoinbaseError(BaseException):

    def __init__(self, errorList):
        self.error = errorList
