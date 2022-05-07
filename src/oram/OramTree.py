import math
import random
from typing import List, Dict

from src.crypto.SymmetricEncryptionObject import SymmetricEncryptionObject
from src.crypto.SymmetricEncryptor import SymmetricEncryptor
from src.oram.OramTreeBucket import OramTreeBucket
from src.storage.IStorageClient import IStorageClient


class OramTree:
    def __init__(self, number_of_levels: int, block_size: int, storage_client: IStorageClient):
        self._number_of_buckets = 2 ** number_of_levels
        self._levels = number_of_levels
        self._storage_client = storage_client
        self._block_size = block_size
        self._buckets = [OramTreeBucket(i, number_of_levels, self._block_size) for i in range(self._number_of_buckets)]
        self._encryptor = SymmetricEncryptor()
        self._bucket_index_to_cypher_object: Dict[int, SymmetricEncryptionObject] = dict()

        # Write all buckets to storage
        self.__write_array_of_buckets(self._buckets)

    def get_number_of_levels(self) -> int:
        return self._levels

    def read_path(self, leaf_index) -> List[OramTreeBucket]:
        path_indexes = self.get_path_index(leaf_index)
        # buckets = [self._buckets[i] for i in path]
        ciphered_buckets_content = [self._storage_client.read(str(index)) for index in path_indexes]
        # Create array of symmetric encryption objects
        symmetric_objects: List[SymmetricEncryptionObject] = []
        for i, ciphered_bucket_content in enumerate(ciphered_buckets_content):
            symmetric_object = self._bucket_index_to_cypher_object[path_indexes[i]]
            symmetric_object.set_cipher_text(ciphered_bucket_content)
            symmetric_objects.append(symmetric_object)

        # Decrypt the buckets
        plain_buckets_content: List[bytes] = [self._encryptor.decrypt(symmetric_object) for symmetric_object in symmetric_objects]
        buckets: List[OramTreeBucket] = \
            [OramTreeBucket.read_bucket_from_bytes(i, plain_bucket_content, self._block_size, self._number_of_buckets) for i, plain_bucket_content in zip(path_indexes, plain_buckets_content)]
        return buckets

    #

    def get_path_index(self, leaf_index) -> List[int]:
        assert self._number_of_buckets > leaf_index >= 0
        path = []
        cur = 0
        leaf_index_as_binary = format(leaf_index, 'b').zfill(self._levels - 1)

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

    def write_path(self, buckets: List[OramTreeBucket]) -> None:
        self.__write_array_of_buckets(buckets)

    def __write_array_of_buckets(self, buckets: List[OramTreeBucket]) -> None:
        for bucket in buckets:
            bucket_index: int = bucket.get_index()
            bucket_as_bytes = bucket.write_bucket_to_bytes()
            symmetric_object: SymmetricEncryptionObject = self._encryptor.encrypt(bucket_as_bytes)
            cypher_text = symmetric_object.get_cipher_text()
            symmetric_object.reset_cipher_text()  # Reset in order to prevent memory leak!!

            self._bucket_index_to_cypher_object[bucket_index] = symmetric_object
            self._storage_client.write(str(bucket_index), cypher_text)

    # def read_bucket_at_path_and_level(self, leaf_index, level) -> OramTreeBucket:
    #     path = self.get_path_index(leaf_index)
    #     return self._buckets[path[level]]
