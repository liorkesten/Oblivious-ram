import math
import random
from typing import List

from src.crypto.SymmetricEncryptionObject import SymmetricEncryptionObject
from src.crypto.SymmetricEncryptor import SymmetricEncryptor
from src.oram.OramTreeBucket import OramTreeBucket
from src.storage.IStorageClient import IStorageClient


class OramTree:
    def __init__(self, number_of_levels: int, storage_client: IStorageClient):
        self._number_of_buckets = 2 ** number_of_levels
        self._levels = number_of_levels
        self._storage_client = storage_client
        self._block_size = number_of_levels  # Block size is log2(number_of_buckets) -> number_of_levels
        self._buckets = [OramTreeBucket(i, number_of_levels, self._block_size) for i in range(self._number_of_buckets)]
        self._encryptor = SymmetricEncryptor()
        self._bucket_index_to_iv: List[int, str] = dict()

    def get_number_of_levels(self) -> int:
        return self._levels

    def read_path(self, leaf_index) -> List[OramTreeBucket]:
        path_indexes = self.get_path_index(leaf_index)
        # buckets = [self._buckets[i] for i in path]
        ciphered_buckets_content = [self._storage_client.read(index) for index in path_indexes]
        # Create array of symmetric encryption objects
        symmetric_objects: List[SymmetricEncryptionObject] = []
        for i, ciphered_bucket_content in enumerate(ciphered_buckets_content):
            iv = self._bucket_index_to_iv[path_indexes[i]]
            symmetric_object = SymmetricEncryptionObject(iv, ciphered_bucket_content, 0)  # we pass 0 because we assume that the size of block will be multiple of 16 as well as the num of buckets.
            symmetric_objects.append(symmetric_object)

        # Decrypt the buckets
        plain_buckets_content: List[bytes] = [self._encryptor.decrypt(symmetric_object) for symmetric_object in symmetric_objects]
        buckets: List[OramTreeBucket] = [OramTreeBucket.read_bucket_from_bytes(i, plain_bucket_content, self._block_size) for i, plain_bucket_content in enumerate(plain_buckets_content)]
        return buckets

    def read_bucket_at_path_and_level(self, leaf_index, level) -> OramTreeBucket:
        path = self.get_path_index(leaf_index)
        return self._buckets[path[level]]

    def get_path_index(self, leaf_index) -> List[int]:
        assert self._number_of_buckets > leaf_index >= 0
        path = []
        cur = 0
        leaf_index_as_binary = format(leaf_index, 'b').zfill(self._levels)

        for i in range(len(leaf_index_as_binary)):
            path.append(cur)
            match leaf_index_as_binary[i]:
                case '0':
                    cur = (2 * cur) + 1
                case '1':
                    cur = (2 * cur) + 2

        path.append(cur)  # Add the last bucket
        return path

    def get_random_leaf(self) -> int:
        return random.randint(0, self._levels + 1)  # TODO verify randint second parameter
