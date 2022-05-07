import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.crypto.SymmetricEncryptionObject import SymmetricEncryptionObject


class SymmetricEncryptor:
    def __init__(self):
        self.key = os.urandom(32)

    def encrypt(self, data: bytes) -> SymmetricEncryptionObject:
        if bytes is None:
            raise ValueError("Data is None")

        # print(f"Starting to encrypt data: {data}")
        num_of_padding_bytes = self.get_num_of_padding_bytes(data)
        if num_of_padding_bytes > 0:
            data += bytes([0] * num_of_padding_bytes)
            print(f"Padding data (len <{len(data)}>): {num_of_padding_bytes}")

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(data) + encryptor.finalize()
        # print(f"Finished to encrypt data with IV {iv}- Cipher Text:{cipher_text}")

        return SymmetricEncryptionObject(iv, cipher_text, num_of_padding_bytes)

    def decrypt(self, symmetric_crypto_object: SymmetricEncryptionObject) -> bytes:
        # print(f"Starting to decrypt data: {symmetric_crypto_object}")

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(symmetric_crypto_object.get_iv()))
        decryptor = cipher.decryptor()
        cypher_text = symmetric_crypto_object.get_cipher_text()
        plain_text = decryptor.update(cypher_text) + decryptor.finalize()
        plain_text = plain_text[:-symmetric_crypto_object.get_num_of_padding_bytes()]

        print(f"Plain Text:{plain_text}. removed padding:{symmetric_crypto_object.get_num_of_padding_bytes()}")
        return plain_text

    @staticmethod
    def get_num_of_padding_bytes(plain_text: bytes) -> int:
        return 16 - (len(plain_text) % 16)
