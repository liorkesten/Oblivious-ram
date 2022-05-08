import unittest
from unittest import TestCase

from src.oram.OramClient import OramClient
from src.storage.LocalFsClient import LocalFsClient
from src.storage.RemoteFsClient import RemoteFsClient


class Test(TestCase):
    # def test_oram(self):
    #     for i in range(10):
    #         oram_manager: OramClient = OramClient(16, 512, LocalFsClient("C:\workspace\Studies\AdvancedCrypto\Oram\DB"))
    #         file_content = "hello, this is the content of file number "
    #         oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
    #         data_as_string: str = oram_manager.read("file1").decode("utf-8")
    #         assert data_as_string == (file_content + "1"), f"Files content are not equal: \nExpected {(file_content + '1')}\nActual {data_as_string}"
    #
    #         oram_manager.write("file2", bytes(file_content + "2", "utf-8"))
    #         data_as_string: str = oram_manager.read("file2").decode("utf-8")
    #         assert data_as_string == (file_content + "2"), f"Files content are not equal: \nExpected {(file_content + '2')}\nActual {data_as_string}"
    #
    # def test_oram_read_twice(self):
    #     oram_manager: OramClient = OramClient(16, 512, LocalFsClient("C:\workspace\Studies\AdvancedCrypto\Oram\DB"))
    #     file_content = "hello, this is the content of file number "
    #     oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
    #     data_as_string: str = oram_manager.read("file1").decode("utf-8")
    #     assert data_as_string == (file_content + "1"), f"Files content are not equal: \nExpected {(file_content + '1')}\nActual {data_as_string}"
    #     data_as_string: str = oram_manager.read("file1").decode("utf-8")
    #     assert data_as_string == (file_content + "1"), f"Files content are not equal: \nExpected {(file_content + '1')}\nActual {data_as_string}"
    #
    # def test_oram_delete(self):
    #     oram_manager: OramClient = OramClient(16, 512, LocalFsClient("C:\workspace\Studies\AdvancedCrypto\Oram\DB"))
    #     file_content = "hello, this is the content of file number "
    #     oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
    #     data_as_string: str = oram_manager.read("file1").decode("utf-8")
    #     oram_manager.delete("file1")
    #     assert oram_manager.read("file1") is None, f"File is not deleted"
    #
    # def test_oram_remote_client(self):
    #     oram_manager: OramClient = OramClient(16, 512, RemoteFsClient())
    #     file_content = "hello, this is the content of file number "
    #     oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
    #     data_as_string: str = oram_manager.read("file1").decode("utf-8")
    #     assert data_as_string == (file_content + "1"), f"Files content are not equal: \nExpected {(file_content + '1')}\nActual {data_as_string}"

    def test_oram_remote_client_delete(self):
        oram_manager: OramClient = OramClient(16, 512, RemoteFsClient())
        file_content = "hello, this is the content of file number "
        oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
        data_as_string: str = oram_manager.read("file1").decode("utf-8")
        oram_manager.delete("file1")
        assert oram_manager.read("file1") is None, f"File is not deleted"

if __name__ == '__main__':
    unittest.main()
