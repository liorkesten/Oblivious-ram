class OramTreeBlock:
    NUMBER_OF_EXTRA_BYTES = 12

    def __init__(self, is_dummy: bool = True, plain_text: bytes = "", block_size: int = 0):
        assert block_size > 0
        self._block_size = block_size

        if is_dummy or plain_text == "":
            self._is_dummy = is_dummy
            self._plain_text = b"dummy plain text"
        else:
            self._plain_text = plain_text
            self._is_dummy = False

        # TODO I need to pad the plain_text to size of block
        self._padded_plain_text = self._plain_text.ljust(self._block_size, b'\0')

    def __str__(self):
        return "\ncipher text: " + str(self._plain_text)

    def __repr__(self):
        return "\ncipher text: " + str(self._plain_text)

    def get_plain_text(self) -> bytes:
        return self._plain_text

    def get_padded_plain_text(self) -> bytes:
        return self._padded_plain_text

    def is_dummy(self) -> bool:
        return self._is_dummy

    @staticmethod
    def read_block_from_bytes(data: bytes) -> "OramTreeBlock":
        is_dummy = bool(int.from_bytes(data[0:4], "little"))
        block_size = int.from_bytes(data[4:8], "little")
        plain_text_length = int.from_bytes(data[8:12], "little")
        plain_text = data[12:12 + plain_text_length]
        return OramTreeBlock(is_dummy, plain_text, block_size)

    def write_block_to_bytes(self) -> bytes:
        bytes_as_str = b""
        bytes_as_str += self._is_dummy.to_bytes(4, "little")
        bytes_as_str += self._block_size.to_bytes(4, "little")
        bytes_as_str += len(self._plain_text).to_bytes(4, "little")
        bytes_as_str += self._padded_plain_text
        return bytes_as_str
