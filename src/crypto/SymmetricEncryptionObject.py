class SymmetricEncryptionObject:
    def __init__(self, iv: bytes, ciphertext: bytes, num_of_padding_bytes: int):
        self._iv = iv
        self._num_of_padding_bytes = num_of_padding_bytes
        self._cipher_text = ciphertext

    def __str__(self):
        return "iv: {}, ciphertext: {}".format(self._iv, self._cipher_text)

    def __repr__(self):
        return self.__str__()

    def get_iv(self) -> bytes:
        return self._iv

    def get_cipher_text(self) -> bytes:
        return self._cipher_text

    def get_num_of_padding_bytes(self) -> int:
        return self._num_of_padding_bytes

    def reset_cipher_text(self):
        self._cipher_text = None

    def set_cipher_text(self, cipher_text: bytes):
        self._cipher_text = cipher_text
