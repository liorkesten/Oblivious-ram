import unittest
import os

from src.storage.LocalFsClient import LocalFsClient


class MyTestCase(unittest.TestCase):
    def test_something(self):
        current_working_directory = os.getcwd()
        client = LocalFsClient(current_working_directory)
        client.write("test.txt", "test")


if __name__ == '__main__':
    unittest.main()
