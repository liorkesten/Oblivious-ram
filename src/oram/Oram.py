import math

from src.crypto.SymmetricEncryptor import SymmetricEncryptor
from src.oram.OramStash import OramStash
from src.oram.OramTree import OramTree
from src.oram.PositionMap import PositionMap
from src.storage.IStorageClient import IStorageClient


class Oram:
    def __init__(self, number_of_files: int, file_size: int, storage_client: IStorageClient):
        self.__validate_input(file_size, number_of_files)

        self._number_of_files = number_of_files
        self._file_size = file_size
        self._position_map: PositionMap = PositionMap()

        number_of_levels = int(math.log2(number_of_files))
        self._tree = OramTree(number_of_levels, storage_client)
        self._stash = OramStash()

    @staticmethod
    def __validate_input(file_size: int, number_of_files: int):
        assert math.log2(number_of_files) == 0, "Number of files must be a power of 2"
        assert math.log2(file_size) == 0, "File size must be a power of 2"

    def read(self, file_path: str):
        return self.__access("read", file_path, None)

    def write(self, output_file_path: str, data: str):
        return self.__access("write", output_file_path, data)

    def __access(self, operation: str, file_path: str, data: str) -> bytes:
        self._stash.clear()  # TODO I think that I should clean the stash before every operation

        leaf_of_file = self._position_map.get(file_path)
        new_position = self.__get_random_leaf()

        # Read all path into stash
        buckets = self._tree.read_path(leaf_of_file)
        self._stash.add_buckets(buckets)

        old_data = self._stash.get(file_path)

        if operation == "write":
            # remove from stash and then add new data
            self._stash.remove(file_path)
            self._stash.add(file_path, data)

        levels = self._tree.get_number_of_levels()
        for level in reversed(range(levels)):  # TODO levels -1 or levels?
            pass

        return old_data.get_plain_text()

    def __get_random_leaf(self):
        return self._tree.get_random_leaf()
