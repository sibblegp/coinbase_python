__author__ = 'kroberts'

class CoinbaseError(BaseException):

    def __init__(self, errorList):
        self.error = errorList

    def __unicode__(self):
        return 'CoinbaseError: {}'.format(unicode(self.error))

    def __str__(self):
        return 'CoinbaseError: {}'.format(str(self.error))