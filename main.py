from src.oram.OramClient import OramClient
from src.server.OramHTTPRequestHandler import OramHTTPRequestHandler
import sys

from src.storage.RemoteFsClient import RemoteFsClient

if __name__ == '__main__':
    # print(f'Number of arguments:{len(sys.argv)} arguments.')
    # if (len(sys.argv) != 2 or sys.argv[1] not in ['server', 'client']):
    #     print('Usage: python3 main.py <client/server>')
    #     sys.exit()
    # if sys.argv[1] == 'server':
    #     OramHTTPRequestHandler.run()
    #
    # elif sys.argv[1] == 'client':
    #     pass
    oram_manager: OramClient = OramClient(4, 512, RemoteFsClient())
    file_content = "hello, this is the content of file number "
    oram_manager.write("file1", bytes(file_content + "1", "utf-8"))
    # data_as_string: str = oram_manager.read("file1").decode("utf-8")
    # assert data_as_string == (file_content + "1"), f"Files content are not equal: \nExpected {(file_content + '1')}\nActual {data_as_string}"
    # oram_manager.delete("file1")
    # assert oram_manager.read("file1") is None, f"File is not deleted"
