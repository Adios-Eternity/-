import socket
import threading


def recv(sock, addr, content):
    print ('Accept new connection from %s:%s...' % addr)
    if content["flag"] == 1:
        sock.send(bytes(content["data"], "utf-8"))
    else:
        sock.send(bytes('Welcome!', 'utf-8'))
    print(sock.recv(1024))
    while True:
        data = sock.recv(1024)
        print(data)

def connect(content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 对socket的配置重用ip和端口号
    s.bind(('127.0.0.2', 9999))
    s.listen(5)
    print('Waiting for connection...')
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=recv, args=(sock, addr, content))
        t.start()
