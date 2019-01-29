# -*- coding:utf-8 -*-
import socket

def clientFunc():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    text = "IT client message"
    data = text.encode()
    addr = ("127.0.0.1",7852)
    sock.sendto(data,addr)
    data,addr = sock.recvfrom(200)
    text = data.decode()
    print("recive` from server ",text)


if __name__ == '__main__':
    clientFunc()



