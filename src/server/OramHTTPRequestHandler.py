import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from src.server.OramHandler import OramHandler

routes = ["/", "read", "write"]


class OramHTTPRequestHandler(BaseHTTPRequestHandler):
    oram_handler = OramHandler()

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
        match parsed_url.path:
            case "/":
                pass
            case "/write":
                file_path = parse_qs(parsed_url.query)['file_path'][0]
                return self.oram_handler.write(file_path)

            case default:
                return self.unknown_route()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        match parsed_url.path:
            case "/":
                pass
            case "/read":
                file_path = parse_qs(parsed_url.query)['file_path'][0]
                return self.oram_handler.read(file_path)
            case default:
                return self.unknown_route()

    def unknown_route(self):
        self.write_response(404, "404 Not Found", "text/plain")

    def write_response(self, status_code: int, content: str, content_type: str):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        content = bytes(content, "UTF-8")
        self.wfile.write(content)
