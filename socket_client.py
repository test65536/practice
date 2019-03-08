import socket

sk = socket.socket()
sk.connect(('127.0.0.1', 8081))

while True:
    info = input('>:')
    sk.send(bytes(info.encode('utf-8')))
    ret = sk.recv(1024).decode('utf-8')
    print('server:', ret)
    if ret == 'bye':
        sk.send(b'bye')
        break
sk.close()
