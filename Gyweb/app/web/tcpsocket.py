import socket
import threading


class socketserver:
    def __init__(self, content):
        address = '127.0.0.2'
        port = 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.sock.listen(10)
        self.data=""
        print('Waiting for connection...')
        # 接受一个新连接:
        self.conn, self.addr = self.sock.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=self.recvmsg, args=(self.conn, self.addr, content))
        t.start()

    def recvmsg(self, soc, addre, content):
        print("accept from %s", addre)
        if content["flag"] == 1:
            self.conn.send(bytes(content["data"], "utf-8"))
            content["flag"] = 0
            content["data"] = ""
        else:
            self.conn.send(bytes("Welcome!", "utf-8"))
        print(self.conn.recv(1024))

    def sendmsg(self, soc, addre, content):
        print("accept from %s", addre)
        if content["flag"] == 1:
            self.conn.send(bytes(content["data"], "utf-8"))
        else:
            self.conn.send(bytes("Welcome!", "utf-8"))
        self.data = self.conn.recv(1024)
        self.Del()
    def callback_data(self):
        return self.data
    def Del(self):
        self.conn.close()

