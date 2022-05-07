class SymmetricEncryptionObject:
    def __init__(self, iv, ciphertext, num_of_padding_bytes):
        self.iv = iv
        self.num_of_padding_bytes = num_of_padding_bytes
        self.cipher_text = ciphertext

    def __str__(self):
        return "iv: {}, ciphertext: {}".format(self.iv, self.cipher_text)

    def __repr__(self):
        return self.__str__()
