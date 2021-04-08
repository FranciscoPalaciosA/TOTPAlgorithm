import unittest
from totp import (generate_seed, generate_secret_key, 
                    get_totp_token)

EMAIL="frankpa97@hotmail.com"
SECRET_KEY = "MQ2TGZLEME3WCNRTG5RTSOLDMM3WMYRVGY3GIOJWMU4WMYJRGA4WEZRRGVRTINZYGQYTAYJTMY2WKYRUMQ2GGNDFGI3GGZBQHAYWMNQ="
RANDOM_SEQUENCE = ['3', '2', 'A', 'C']
class TestTOTPalgorithm(unittest.TestCase):

    def test_generate_seed(self):
        seed = generate_seed()
        # All seeds will be random
        self.assertEqual(len(seed), 64)

    def test_generate_secret_key(self):
        seed = ''.join(['A'] * 64)
        sk = generate_secret_key(seed)
        self.assertEqual(sk, SECRET_KEY)

    def test_totp_dif_time_interval(self):
        original_time = 240
        totp = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, original_time)
        totp2 = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, original_time + 120)
        self.assertNotEqual(totp, totp2)

    def test_totp_dif_random_sequence(self):
        totp = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, 240)
        totp2 = get_totp_token(SECRET_KEY, '1234', 240)
        self.assertNotEqual(totp, totp2)
    
    def test_totp_dif_secret_ket(self):
        totp = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, 240)
        totp2 = get_totp_token(SECRET_KEY.replace('M', 'N'), RANDOM_SEQUENCE, 240)
        self.assertNotEqual(totp, totp2)

    def test_totp_same_time_interval(self):
        original_time = 240
        totp = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, original_time)
        totp2 = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, original_time + 119)
        self.assertEqual(totp, totp2)
    
    def test_totp_same_random_sequence(self):
        totp = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, 240)
        totp2 = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, 240)
        self.assertEqual(totp, totp2)
    
    def test_totp_same_secret_ket(self):
        totp = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, 240)
        totp2 = get_totp_token(SECRET_KEY, RANDOM_SEQUENCE, 240)
        self.assertEqual(totp, totp2)

if __name__ == '__main__':
    unittest.main()