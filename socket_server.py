import socket

sk = socket.socket()  # 买手机
sk.bind(('127.0.0.1', 8081))  # 绑定手机卡
sk.listen()  # 监听

conn, addr = sk.accept()
print(addr)

while True:
    ret = conn.recv(1024).decode('utf-8')
    if ret == 'bye':
        print('client:', ret)
        break
    print('client:', ret)
    info = input('>:')
    conn.send(bytes(info.encode('utf-8')))

conn.close()
sk.close()
