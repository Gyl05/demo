import datetime
import re
import socket

class WSGIServer:
    def __init__(self, port, html_path='./html') -> None:
        self.port = port
        self.html_path = html_path
        self.new_socket = None
        self.server_socket = None

    def run(self):
        self.server_socket = server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", self.port))
        print(f"WsgiServer running on {self.port} ...")
        server_socket.listen(128)
        while True:
            self.new_socket, client_addr = server_socket.accept()
            status, action = self.handle_request()
            now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            print(f"{now} -- {client_addr} | {action} -- [{status}]")

    def handle_request(self):
        status = 500
        request = self.new_socket.recv(1024).decode('utf-8')
        request_lines = request.splitlines()
        tmp = re.match(r"([^/]*)([^ ]+)", request_lines[0])
        if tmp:
            file_name = tmp.group(2)
            if file_name == '/':
                file_name = '/index.html'
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
        return status, request_lines[0]


def main():
    http_server = WSGIServer(7890, './html')
    http_server.run()


if __name__ == '__main__':
    main()