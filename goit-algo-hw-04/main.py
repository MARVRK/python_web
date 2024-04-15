import urllib.parse
import json
import socket
import logging
import sys
import mimetypes
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread



BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
DATA_FILE = STORAGE_DIR / "data.json"

def ensure_storage():
    if not STORAGE_DIR.exists():
        STORAGE_DIR.mkdir(parents=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

BUFFER_SIZE = 1024
HTTP_PORT = 3000
HTTP_HOST = '0.0.0.0'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 5000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        rout = urllib.parse.urlparse(self.path)
        match rout.path:
            case '/':
                self.send_html_file("index.html")
            case '/message':
                self.send_html_file("message.html")
            case _:
                file = BASE_DIR.joinpath(rout.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html_file("error.html", 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        
        if 'username' in parsed_data and 'message' in parsed_data:
            username = parsed_data['username'][0]
            message = parsed_data['message'][0]
            
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(f'{username}::{message}'.encode('utf-8'), (SOCKET_HOST, SOCKET_PORT))
            udp_socket.close()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            data = {
                timestamp: {
                    'username': username,
                    'message': message
                }
            }
            with open('storage/data.json', 'a+') as file:
                json.dump(data, file, indent=2)
                file.write('\n')
            self.send_response(302)
            self.send_header('Location', '/message')
            self.end_headers()
        else:
            self.send_error(400, 'Bad Request: Required fields are missing')

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

def run_socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.close()

def run_http_server(host, port):
    address = (host, port)
    http_server = HTTPServer(address, HttpHandler)  
    try:
        ensure_storage() 
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http_server.server_close()






if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    server = Thread(target=run_http_server, args=(HTTP_HOST, HTTP_PORT))
    server.start()

    server_socket = Thread(target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT))
    server_socket.start()

