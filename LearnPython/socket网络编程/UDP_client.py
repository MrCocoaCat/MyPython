# -*- coding:utf-8 -*-
import socket
import time

def clientFunc():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    for i in range(1000):
        text = "%s" % str(i)
        data = text.encode()
        addr = ("127.0.0.1", 8000)
        sock.sendto(data, addr)
        print("send  ", text)
        try:
            data2, addr = sock.recvfrom(500)
            text2 = data2.decode()
            print("recive from server ", text2)
        except Exception as e:
           pass
        time.sleep(1)


if __name__ == '__main__':
    clientFunc()



