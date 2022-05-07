import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from src.storage.LocalFsClient import LocalFsClient


class OramHTTPRequestHandler(BaseHTTPRequestHandler):
    local_fs_client = LocalFsClient("C:\workspace\Studies\AdvancedCrypto\Oram\Server")

    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    @staticmethod
    def run(address="localhost", port=8080):
        web_server = HTTPServer((address, port), OramHTTPRequestHandler)
        try:
            print(f"Starting to listen on {address}:{port}")
            web_server.serve_forever()
        except KeyboardInterrupt:
            pass

        web_server.server_close()
        print(f"Server stopped")

    def do_POST(self):
        parsed_url = urlparse(self.path)
        print(f"Handling POST request - {parsed_url.path}")
        match parsed_url.path:
            case "/":
                pass
            case "/write":
                file_path = parse_qs(parsed_url.query)['filename'][0]
                content_len = int(self.headers.get('Content-Length'))
                data = self.rfile.read(content_len)
                response = self.local_fs_client.write(file_path, data=data)
                return self.write_response(200, response, "text/plain")

            case default:
                return self.unknown_route()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        print(f"Handling GET request - {parsed_url.path}")
        match parsed_url.path:
            case "/":
                pass
            case "/read":
                file_path = parse_qs(parsed_url.query)['filename'][0]
                try:
                    content = self.local_fs_client.read(file_path)
                    return self.write_response(200, content, "text/plain")
                except FileNotFoundError:
                    return self.write_response(404, "404 Not Found", "text/plain")
            case default:
                return self.unknown_route()

    def unknown_route(self):
        self.write_response(404, "404 Not Found", "text/plain")

    def write_response(self, status_code: int, content: bytes, content_type: str):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)
