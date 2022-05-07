import unittest

from src.oram.OramTreeBlock import OramTreeBlock


class MyTestCase(unittest.TestCase):
    def test_to_bytes_and_read_bytes_work(self):
        block = OramTreeBlock(False, bytes("lior kesten", "utf-8"), 140)
        block_as_bytes = block.write_block_to_bytes()
        block2 = OramTreeBlock.read_block_from_bytes(block_as_bytes)
        assert block.get_plain_text() == block2.get_plain_text()


if __name__ == '__main__':
    unittest.main()
