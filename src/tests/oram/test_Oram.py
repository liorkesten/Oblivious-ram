import unittest
from unittest import TestCase

from src.oram.Oram import Oram
from src.storage.LocalFsClient import LocalFsClient


class Test(TestCase):
    def test_oram(self):
        oram_manager: Oram = Oram(16, 512, LocalFsClient("C:\workspace\Studies\AdvancedCrypto\Oram\DB"))
        file_content = "hello, this is the content of file number "
        oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
        data_as_string: str = oram_manager.read("file1").decode("utf-8")
        print(data_as_string)
        assert data_as_string == (file_content + "1"), f"Files content are not equal: \nExpected {(file_content + '1')}\nActual {data_as_string}"

        oram_manager.write("file1", bytes(file_content + "2", "utf-8"))
        data_as_string: str = oram_manager.read("file1").decode("utf-8")
        print(data_as_string)
        assert data_as_string == (file_content + "2"), f"Files content are not equal: \nExpected {(file_content + '2')}\nActual {data_as_string}"


if __name__ == '__main__':
    unittest.main()
