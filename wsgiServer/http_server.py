import datetime
import multiprocessing
import os
import re
import socket

import mini_web

class WSGIServer:
    def __init__(self, port, html_path='./html') -> None:
        self.port = port
        self.html_path = html_path
        self.new_socket = None
        self.server_socket = None
        self.headers = None
        self.status = ''

    def run(self):
        self.server_socket = server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", self.port))
        print(f"WsgiServer running on {self.port} ...")
        server_socket.listen(128)
        while True:
            self.new_socket, client_addr = server_socket.accept()
            new_process = multiprocessing.Process(target=self.handle_request)
            new_process.start()
            self.new_socket.close()

    def handle_request(self):
        pid = os.getpid()
        status = 500
        request = self.new_socket.recv(1024).decode('utf-8')
        request_lines = request.splitlines()
        if len(request_lines) < 1:
            return
        tmp = re.match(r"([^/]*)([^ ]+)", request_lines[0])
        http_method = request_lines[0].split(' ')[0]
        if tmp:
            file_name = tmp.group(2)
            if file_name == '/':
                file_name = '/index.html'
        else:
            return
        if file_name.endswith('.py'):  # 实现动静分离
            env = {'PATH_INFO': file_name}  # wsgi规定
            env['REQUEST_METHOD'] = http_method

            response_body = mini_web.application(env, self.set_status_headers)
            response = f"HTTP/1.1 {self.status}\r\n"
            for header in self.headers:
                response += f"{header[0]}:{header[1]}\r\n"
            response += "\r\n"
            response += response_body
            self.new_socket.send(response.encode('utf-8'))
            self.new_socket.close()
            return
        try:
            f = open(self.html_path + file_name, 'rb')
        except:
            response_header = "HTTP/1.1 404 not found\r\n"
            response_header += "\r\n"
            f = open(self.html_path + '/404.html', 'rb')
            status = 404
        else:
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "\r\n"
            status = 200
        finally:
            response_body = f.read()
            self.new_socket.send(response_header.encode('utf-8'))
            self.new_socket.send(response_body)
            f.close()
            self.new_socket.close()
        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        print(f"{now} -- [{status}] - {request_lines[0]} - {pid} 进程在服务...")

    def set_status_headers(self, status, headers):
        self.headers = headers
        self.status = status


def main():
    http_server = WSGIServer(7890, './html')
    http_server.run()


if __name__ == '__main__':
    main()