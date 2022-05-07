class OramTreeBlock:
    MAX_LEN_OF_FILE_NAME = 30
    NUMBER_OF_EXTRA_BYTES = 13 + MAX_LEN_OF_FILE_NAME

    def __init__(self, is_dummy: bool = True, file_name: str = "", plain_text: bytes = "", block_size: int = 0):
        assert block_size > 0, "block size must be greater than 0"
        assert 0 <= len(file_name) <= OramTreeBlock.MAX_LEN_OF_FILE_NAME, f"file name must be between 0 and {OramTreeBlock.MAX_LEN_OF_FILE_NAME} characters"

        self._block_size = block_size

        if is_dummy or plain_text == "":
            self._is_dummy = is_dummy
            self._file_name = "dummy_file".encode("utf-8")
            self._plain_text = b"dummy plain text"
        else:
            self._file_name = file_name.encode("utf-8")
            self._plain_text = plain_text
            self._is_dummy = False

        # TODO I need to pad the plain_text to size of block
        self._padded_file_name = self._file_name.ljust(OramTreeBlock.MAX_LEN_OF_FILE_NAME, b'\0')
        self._padded_plain_text = self._plain_text.ljust(self._block_size, b'\0')

    def __str__(self):
        return "\nplain text: " + str(self._plain_text)

    def __repr__(self):
        return "\nplain text: " + str(self._plain_text)

    def get_file_name(self) -> str:
        return self._file_name.decode("utf-8")

    def get_padded_file_name(self) -> str:
        return self._padded_file_name.decode("utf-8")

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

        # Filename
        file_name_length = int.from_bytes(data[8:9], "little")
        file_name_as_bytes = data[9:9 + file_name_length]
        file_name = file_name_as_bytes.decode("utf-8")

        # Data
        data_length = int.from_bytes(data[9 + OramTreeBlock.MAX_LEN_OF_FILE_NAME:13 + OramTreeBlock.MAX_LEN_OF_FILE_NAME], "little")
        data_as_bytes = data[13 + OramTreeBlock.MAX_LEN_OF_FILE_NAME:13 + OramTreeBlock.MAX_LEN_OF_FILE_NAME + data_length]
        plain_text = data_as_bytes
        return OramTreeBlock(is_dummy, file_name, plain_text, block_size)

    def write_block_to_bytes(self) -> bytes:
        bytes_as_str = b""
        bytes_as_str += self._is_dummy.to_bytes(4, "little")  # TODO maybe change to 1 byte
        bytes_as_str += self._block_size.to_bytes(4, "little")  # TODO maybe I can remove it
        # Filename
        bytes_as_str += len(self._file_name).to_bytes(1, "little")
        bytes_as_str += self._padded_file_name
        # Data
        bytes_as_str += len(self._plain_text).to_bytes(4, "little")
        bytes_as_str += self._padded_plain_text
        return bytes_as_str
