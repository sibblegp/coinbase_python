__author__ = 'gsibble'

import sure
from sure import it, this, those, these
import unittest
from coinbase import CoinBase
    
    def setUp(self):
        self.coinbase = CoinBase()