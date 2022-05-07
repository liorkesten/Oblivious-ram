import sys
from src.client.OramClient import OramClient

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 main.py <host> <port> <read/write> <file_path>')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    operation = sys.argv[3]
    file_path = sys.argv[4]
    print(f"Starting client with host: {host}, port: {port}, operation: {operation}, file_path: {file_path}")
    client = OramClient(host, port)
    if operation == 'read':
        client.read(file_path)
    elif operation == 'write':
        client.write(file_path)
