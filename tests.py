import unittest
from totp import get_totp_token

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        secret_key = "HA2GKZBRGM2GINRQGM3TGYRUGNQTMYZYGZSDKMJWMZQTEZRYGU2DSZJTMZQWCMBQGY2GCZBZMZRDOMTDGM3TKMRXHA4TAZBSGMZGCZQ="
        get_totp_token(secret_key, "0000")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()