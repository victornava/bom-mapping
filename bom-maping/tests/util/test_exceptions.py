import unittest
from util.exceptions import *

class TestWMSBaseError(unittest.TestCase):    
    def test_accepts_empty_constructor(self):
        e = OperationNotSupportedError()
        self.assertEqual("OperationNotSupported", e.data()['code'])
    
    def test_data(self):
        e = OperationNotSupportedError("the message")
        self.assertEqual("OperationNotSupported", e.data()['code'])
        self.assertEqual("the message", e.data()['message'])
                    
if __name__ == '__main__':
    unittest.main()