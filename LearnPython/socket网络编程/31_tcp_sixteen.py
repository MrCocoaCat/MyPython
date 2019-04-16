# -*- coding: utf-8 -*-
# @Time    : 2019/2/15 11:28
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 31_tcp_sixteen.py.py

# Simple TCP client and server that send and receive 16 octets

import argparse, socket


def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 可是使用正在关闭的套接字
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    # 该 socket被转换为监听套接字，该改变无法撤销
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        # 返回一个套接字,这个套接字用于发送消息
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        #
        message = recvall(sc, 16)
        print('  Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print('  Reply sent, socket closed')


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    # 一次性发送所有数据
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)