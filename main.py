from src.server.OramHTTPRequestHandler import OramHTTPRequestHandler
from src.client.OramClient import OramClient
import sys

if __name__ == '__main__':
    print(f'Number of arguments:{len(sys.argv)} arguments.')
    if (len(sys.argv) != 2 or sys.argv[1] not in ['server', 'client']):
        print('Usage: python3 main.py <client/server>')
        sys.exit()
    if sys.argv[1] == 'server':
        OramHTTPRequestHandler.run()

    elif sys.argv[1] == 'client':
        pass
