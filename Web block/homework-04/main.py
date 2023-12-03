import pathlib
from datetime import datetime
import logging
from threading import Thread
import json
from pathlib import Path
import urllib.parse
import mimetypes
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler


BASE_DIR = Path()
BUFFER_SIZE = 1024
HTTP_PORT = 3000
HTTP_HOST = '0.0.0.0'
SOCKET_PORT = 5000
SOCKET_HOST = '127.0.0.1'


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        if route.path == '/':
            self.send_html('index.html')
        elif route.path == '/message':
            self.send_html('message.html')
        else:
            file = BASE_DIR.joinpath(route.path[1:])
            if file.exists():
                self.send_static(file)
            else:
                self.send_html('error.html', status_code=404)

    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        client_socket.close()
        self.send_response(302)
        self.send_header(keyword='Location', value='/message')
        self.end_headers()

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header(keyword='Content-Type', value='text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header(keyword='Content-Type', value=mime_type)
        else:
            self.send_header(keyword='Content-Type', value='text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


def save_data_from_form(data):
    body_message = urllib.parse.unquote_plus(data.decode())
    try:
        parse_message = {key: value for key, value in [el.split('=') for el in body_message.split('&')]}

        with open('storage/data.json', 'r', encoding='utf-8') as fh:
            path = Path('storage/data.json')
            if path.stat().st_size == 0: #check if file is empty
                base_of_messages = {str(datetime.now()): parse_message}
            else:
                base_of_messages = json.load(fh)
                base_of_messages[str(datetime.now())] = parse_message

        with open('storage/data.json', 'w', encoding='utf-8') as fh:
            json.dump(base_of_messages, fh, ensure_ascii=False, indent=4)

    except ValueError as err:
        logging.error(err)
    except OSError as err:
        logging.error(err)


def run_socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    logging.info('Starting socket server')
    try:
        while True:
            message, address = server_socket.recvfrom(BUFFER_SIZE)
            logging.info(f'Socked received {address}:{message}')
            save_data_from_form(message)
    except KeyboardInterrupt:
        logging.info('Socket server stopped from keyboard')
    finally:
        server_socket.close()


def run_http_server(host, port):
    address = (host, port)
    http_server = HTTPServer(address, MyHTTPRequestHandler)
    logging.info('Starting HTTP server')
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        logging.info('HTTP server stopped from keyboard')
    finally:
        http_server.server_close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    STORAGE_DIR = pathlib.Path().joinpath('storage')
    FILE_STORAGE = STORAGE_DIR / 'data.json'
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as fh:
            json.dump({}, fh, ensure_ascii=False)

    server = Thread(target=run_http_server, args=(HTTP_HOST, HTTP_PORT))
    server.start()

    server_socket = Thread(target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT))
    server_socket.start()