import unittest

from src.crypto.SymmetricEncryptor import SymmetricEncryptor


class MyTestCase(unittest.TestCase):
    def test_happy_path(self):
        s = "hello world hello world hello world"
        enc = SymmetricEncryptor()
        r = enc.encrypt(bytes(s, 'utf-8'))
        plain_text = enc.decrypt(r).decode('ascii')
        assert s == plain_text

    def test_same_string_diff_iv(self):
        s = "hello world hello world hello world"
        enc = SymmetricEncryptor()
        r1 = enc.encrypt(bytes(s, 'utf-8'))
        r2 = enc.encrypt(bytes(s, 'utf-8'))
        plain_text1 = enc.decrypt(r1).decode('ascii')
        plain_text2 = enc.decrypt(r2).decode('ascii')
        assert s == plain_text1 == plain_text2
        assert not r1._cipher_text == r2._cipher_text


if __name__ == '__main__':
    unittest.main()
