# -*- coding: utf-8 -*-
import socket


def tcp_client():
    # 1. 创建socket
    # SOCK_STREAM表示其为TCP 模式
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adr = ("127.0.0.1", 8997)
    # 2. 连接对方
    sock.connect(adr)
    # 3. 发送内容到对方服务器
    for i in range(1000):
        msg = "this is client %s" % str(i)
        print(msg)
        sock.send(msg.encode())
        rst = sock.recv(500)
        print(rst)
    sock.close()


if __name__ == '__main__':
    tcp_client()
