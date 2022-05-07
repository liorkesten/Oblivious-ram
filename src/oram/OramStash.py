from typing import List

from src.oram.OramTreeBlock import OramTreeBlock
from src.oram.OramTreeBucket import OramTreeBucket


class OramStash:
    def __init__(self, capacity=0):
        self._capacity = capacity
        self._stash: List[OramTreeBucket] = []

    def get_buckets(self) -> List[OramTreeBucket]:
        return self._stash

    def get_root_bucket(self) -> OramTreeBucket:
        if len(self._stash) == 0:
            raise Exception("Stash is empty")

        return self._stash[0]

    def add_buckets(self, buckets: List[OramTreeBucket]):
        for bucket in buckets:
            self.add_bucket(bucket)

    def add_bucket(self, bucket: OramTreeBucket):
        # TODO should I check the capacity?
        self._stash.append(bucket)

    def get(self, file_path):
        index = self.try_get_index(file_path)
        if index is not None:
            return self._stash[index]

        raise Exception("File not found in stash")

    def get_block_and_remove_from_bucket(self, file_path: str) -> OramTreeBlock:
        index_block_of_file = self.try_get_index(file_path)
        if index_block_of_file is None:
            return None

        removed_block = self._stash[index_block_of_file].remove(file_path)
        return removed_block

    def try_get_index(self, file_path: str) -> int:
        for i, bucket in enumerate(self._stash):
            for block in bucket.get_blocks():
                if block.get_file_name() == file_path:
                    return i

        return None

    def clear(self):
        self._stash.clear()

    def remove(self, file_path):
        index = self.try_get_index(file_path)
        if index is not None:
            self._stash.pop(index)

        raise Exception("File not found in stash")

    # def add(self, file_path: str, data : bytes):
    #     # TODO should create block object
    #     self._stash.append(data)
