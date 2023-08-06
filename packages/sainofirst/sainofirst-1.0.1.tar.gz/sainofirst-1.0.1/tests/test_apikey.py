import unittest
from sainofirst import Sainofirst


class TestApiKey(unittest.TestCase):

    def test_apiKeyNotExist(self):
        self.assertRaises(Exception, Sainofirst, None)

    def test_apiKeyEmpty(self):
        self.assertRaises(Exception, Sainofirst, "")

    def test_apiKeyExist(self):
        sf = Sainofirst("uewyr932yr9gqeu")
        self.assertIsInstance(sf, Sainofirst)

    

if __name__ == '__main__':
    unittest.main()