__author__ = 'kroberts'



class CoinbaseError(object):

    def __init__(self, errorList):
        self.error = errorList

class TransactionError(Exception):
    def __init__(self, message, error_list=[]):
        Exception.__init__(self, message)
        self.error_list = error_list
