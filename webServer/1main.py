import socket
import re

g_document_root = "./html"

def main():
    # 1.创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 2.绑定本地信息
    server_socket.bind(("", 8888))
    # 3.变为监听套接字
    server_socket.listen(128)
    # 4.等待对方链接
    while True:
        new_socket, client_addr = server_socket.accept()
        # 接收数据
        request = new_socket.recv(1024).decode('utf-8')
        lines = request.splitlines()
        # 提取接受的文件名
        print(lines)
        ret = re.match(r"([^/]*)([^ ]+)", lines[0])
        # if ret:
        #     print(ret.group(1), '->' ,ret.group(2))
        file_name =ret.group(2)
        if file_name == '/':
            file_name = '/index.html'
        try:
            f = open(g_document_root + file_name, 'rb')
        except:
            response_header = "HTTP/1.1 404 not found\r\n"
            response_header += "\r\n"
            response_body = open(g_document_root + '/404.html', 'rb').read()
            new_socket.send(response_header.encode('utf-8'))
            # 返回响应体
            new_socket.send(response_body)  # body是读的二进制，不用再encode
        else:
            content = f.read()
            # 读取文件，返回给客户端
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "\r\n"
            response_body = content
            # 返回响应头
            new_socket.send(response_header.encode('utf-8'))
            # 返回响应体
            new_socket.send(response_body)  # body是读的二进制，不用再encode
            f.close()
        finally:
            new_socket.close()


if __name__ == '__main__':
    main()