import math

from src.crypto.SymmetricEncryptor import SymmetricEncryptor
from src.oram.OramStash import OramStash
from src.oram.OramTree import OramTree
from src.oram.OramTreeBlock import OramTreeBlock
from src.oram.PositionMap import PositionMap
from src.storage.IStorageClient import IStorageClient
from src.storage.LocalFsClient import LocalFsClient


class Oram:
    def __init__(self, number_of_files: int, file_size: int, storage_client: IStorageClient = LocalFsClient()):
        self.__validate_input(file_size, number_of_files)

        self._number_of_files = number_of_files
        self._file_size = file_size
        self._position_map: PositionMap = PositionMap()

        number_of_levels = int(math.log2(number_of_files))
        self._tree = OramTree(number_of_levels, file_size, storage_client)
        self._stash = OramStash()

    @staticmethod
    def __validate_input(file_size: int, number_of_files: int):
        assert (math.log2(number_of_files) % 2) == 0, "Number of files must be a power of 2"
        assert (math.log2(number_of_files) % 2) == 0, "File size must be a power of 2"

    def read(self, file_path: str) -> bytes:
        return self.__access("read", file_path, None)

    def write(self, output_file_path: str, data: bytes) -> None:
        returned_value_from_access = self.__access("write", output_file_path, data)
        if returned_value_from_access is not None:
            raise Exception(f"File {output_file_path} already exists")

        return None

    def __access(self, operation: str, file_path: str, data: bytes) -> bytes:
        self._stash.clear()  # TODO I think that I should clean the stash before every operation

        # If the file is not exist then we just want to iterate over random path
        leaf_of_file = self._position_map.get(file_path) if self._position_map.contains(file_path) else self.__get_random_leaf()

        # Read all path into stash
        buckets = self._tree.read_path(leaf_of_file)
        self._stash.add_buckets(buckets)

        # remove block from the bucket and the position map
        old_block: OramTreeBlock = self._stash.get_block_and_remove_from_bucket(file_path)
        self._position_map.remove(file_path)

        if operation == "write":
            # Update root bucket and position map
            self._stash.get_root_bucket().add(file_path, data)
            new_position = self.__get_random_leaf()
            self._position_map.set(file_path, new_position)

        elif operation == "read":
            # Add old block to the root
            self._stash.get_root_bucket().add(old_block.get_file_name(), old_block.get_plain_text())
            new_position = self.__get_random_leaf()
            self._position_map.set(old_block.get_file_name(), new_position)

        # Write all path into storage
        self._tree.write_path(self._stash.get_buckets())

        # TODO evict

        return old_block.get_plain_text() if operation == "read" else None

    def __get_random_leaf(self):
        return self._tree.get_random_leaf()
