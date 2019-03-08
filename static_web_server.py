import socket
import multiprocessing
import time

HTML_ROOT_DIR = ''


def handle_client(client_socket):
    """处理客户端请求"""
    # 获取客户端请求
    request_data = client_socket.recv(1024)
    print("request data:\n"+"*"*50+"\n", request_data)
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server\r\n"
    response_body = time.ctime()
    response = response_start_line + response_headers + "\r\n" + response_body
    print("response data:\n"+"*"*50+"\n", response)
    # 返回响应数据
    client_socket.send(bytes(response, "utf-8"))
    # 关闭客户端连接
    client_socket.close()


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8000))
    server_socket.listen(128)

    while True:
        client_socket, client_addr= server_socket.accept()
        print("用户[%s:%s]连接上了!" % client_addr)
        handle_client_process = multiprocessing.Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()
