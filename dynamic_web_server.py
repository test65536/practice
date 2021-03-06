import socket
import multiprocessing
import re  # 正则表达式
import sys

# 常量，所有字母大写
HTML_ROOT_DIR = '.'
WSGI_PYTHON_DIR = '.'


class HTTPServer(object):
    """"""
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server_socket.listen(128)

    def start_response(self, status, headers):
        # server_headers = [("Server", "MY SERVER")]
        response_headers = "HTTP/1.1" + status + "\n\r"
        for header in headers:
            response_headers += "%s: %s\r\n" % header
        self.response_headers = response_headers

    def start(self):
        self.server_socket.listen(128)
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print("[%s:%s]用户连接上了" % client_addr)
            handle_client_process = multiprocessing.Process(target=self.handle_client, args=(client_socket,))
            handle_client_process.start()  # 开启进程
            client_socket.close()

    def handle_client(self, client_socket):
        # 获取客户端请求
        request_data = client_socket.recv(1024)
        print("request data:", request_data)
        request_lines = request_data.splitlines()  # 按行截断
        for lines in request_lines:
            print(lines)
        #  解析请求报文
        # 'GET / HTTP/1.1'
        response_start_line = request_lines[0]
        # 提取用户请求的文件名
        print("response start line:\n"+"*" * 50, str(response_start_line))
        file_name = re.match(r"\w+ +(/[^ ]*) ", response_start_line.decode("utf-8")).group(1)

        # 用户请求my_time.py
        if file_name.endswith(".py"):
            m = __import__(file_name[1:-3])  # 去掉 /和 .py,调用的名字只有my_time
            env = {}
            response_body = m.application(env, self.start_response)
            response = self.response_headers + "\r\n" + response_body
        else:
            if "/" == file_name:  # 少写=出错，常量写在左边
                file_name = "/index.html"

            try:
                # 打开文件，读取内容
                file = open(HTML_ROOT_DIR + file_name, "rb")  # b二进制，不带b，文本方式
            except IOError:
                response_start_line = "HTTP/1.1 404 Not found\r\n"  # \r\n windows换行符，linux-\r
                response_headers = "Server\r\n"
                response_body = "file not found"
            else:
                file_data = file.read()
                file.close()

                # 构造响应数据
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Server\r\n"
                response_body = file_data.decode("utf-8")

            response = response_start_line + response_headers + "\r\n" + response_body
            print("response data:", response)
        # 返回响应数据
        client_socket.send(bytes(response, "utf-8"))
        # 关闭客户端连接
        client_socket.close()

    def set_port(self, port):
        self.server_socket.bind(("", port))  # 任意IP地址


def main():
    sys.path.insert(1, WSGI_PYTHON_DIR)
    http_server = HTTPServer()
    http_server.set_port(8000)  # Ctrl+左键，查看方法定义
    http_server.start()


# 使用127.0.0.1:8000
#   或10.0.0.105:8000
#   或202.196.118.51:8888(需端口映射) 访问
if __name__ == '__main__':
    main()
