import random
from typing import List

from src.oram.OramTreeBlock import OramTreeBlock


class OramTreeBucket:
    def __init__(self, index: int, capacity: int, block_size: int):
        self._capacity = capacity
        self._block_size = block_size
        self._index = index  # the index of the node.
        # Padding with dummies
        self._blocks: List[OramTreeBlock] = []

    def __str__(self):
        return str(self._blocks)

    def __repr__(self):
        return str(self._blocks)

    def get_random_block(self) -> OramTreeBlock:
        if len(self._blocks) == 0:
            return None

        random_block = random.choice(self._blocks)
        if (random_block is None or random_block.is_dummy()):
            raise Exception("No block found")
        return random_block

    def add(self, file_name: str, plain_text: bytes):
        assert len(self._blocks) < self._capacity, "Node is full"
        new_block = OramTreeBlock(is_dummy=False, file_name=file_name, plain_text=plain_text, block_size=self._block_size)
        self._blocks.append(new_block)

    def remove(self, file_path) -> OramTreeBlock:
        for block in self._blocks:
            if block.get_file_name() == file_path:
                self._blocks.remove(block)  # TODO is  it working or should I use del?
                return block

        raise Exception("File not found")

    def get_blocks(self) -> List[OramTreeBlock]:
        return self._blocks

    def get_index(self) -> int:
        return self._index

    @staticmethod
    def read_bucket_from_bytes(bucket_index: int, data: bytes, block_size: int, capacity: int) -> 'OramTreeBucket':
        blocks = []
        for i in range(0, len(data), block_size + OramTreeBlock.NUMBER_OF_EXTRA_BYTES):
            block: OramTreeBlock = OramTreeBlock.read_block_from_bytes(data[i:i + block_size])
            # We want to skip dummies blocks
            if block.is_dummy():
                continue
            blocks.append(block)

        bucket = OramTreeBucket(bucket_index, capacity, block_size)
        bucket._blocks = blocks
        return bucket

    def write_bucket_to_bytes(self) -> bytes:
        data = b""
        for block in self._blocks:
            data += block.write_block_to_bytes()
        # Pad with dummies blocks
        for i in range(len(self._blocks), self._capacity):
            data += OramTreeBlock(is_dummy=True, block_size=self._block_size).write_block_to_bytes()

        return data
