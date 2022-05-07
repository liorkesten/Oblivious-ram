from typing import List

from src.oram.OramTreeBlock import OramTreeBlock
from src.oram.OramTreeBucket import OramTreeBucket


class OramStash:
    def __init__(self, capacity=0):
        self._capacity = capacity
        self._stash: List[OramTreeBlock] = []

    def add_buckets(self, buckets: List[OramTreeBucket]):
        for bucket in buckets:
            self.add_bucket(bucket)

    def add_bucket(self, bucket: OramTreeBucket):
        # TODO should I check the capacity?
        # Add bucket to stash -> extract blocks from bucket
        blocks_of_buckets = bucket.get_blocks()
        self._stash.extend(blocks_of_buckets)

    def add_block(self, block: OramTreeBlock):
        self._stash.append(block)

    def get(self, file_path):
        index = self.try_get_index(file_path)
        if index is not None:
            return self._stash[index]

        raise Exception("File not found in stash")

    def get_and_pop(self, file_path: str):
        index = self.try_get_index(file_path)
        if index is not None:
            value = self._stash.pop(index)
            return value

        raise Exception("File not found in stash")

    def try_get_index(self, item: str):
        for i in range(len(self._stash)):
            if self._stash[i] == item:  # TODO I need to check item against the file_path - handle with encryption
                return i

        return None

    def clear(self):
        self._stash.clear()

    def remove(self, file_path):
        index = self.try_get_index(file_path)
        if index is not None:
            self._stash.pop(index)

        raise Exception("File not found in stash")

    def add(self, file_path, data):
        # TODO should create block object
        self._stash.append(data)
