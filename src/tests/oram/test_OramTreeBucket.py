from unittest import TestCase

from src.oram.OramTreeBucket import OramTreeBucket


class TestOramTreeBucket(TestCase):
    def test_write_bucket_to_bytes(self):
        capacity = 160
        block_size = 200
        index = 4
        bucket: OramTreeBucket = OramTreeBucket(index=index, capacity=capacity, block_size=block_size)
        bucket.add("file1", bytes("lior kesten1", "utf-8"))
        bucket.add("file2", bytes("lior kesten2", "utf-8"))
        bucket.add("file3", bytes("lior kesten3", "utf-8"))
        bucket.add("file4", bytes("lior kesten4", "utf-8"))
        bucket.add("file5", bytes("lior kesten5", "utf-8"))
        bucket_as_bytes = bucket.write_bucket_to_bytes()
        new_bucket = OramTreeBucket.read_bucket_from_bytes(index, bucket_as_bytes, block_size, capacity)
        assert len(new_bucket.get_blocks()) == len(bucket.get_blocks())
        for old_block, new_block in zip(bucket.get_blocks(), new_bucket.get_blocks()):
            assert old_block.get_plain_text() == new_block.get_plain_text()
