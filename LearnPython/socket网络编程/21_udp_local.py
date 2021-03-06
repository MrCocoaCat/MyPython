# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 16:10
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 21_udp_local.py.py


import argparse, socket
from datetime import datetime

MAX_BYTES = 65535


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    # sock.getsockname() 获取socket的二元组
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        # 解码
        text = data.decode('ascii')
        print('recive from {} : {}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        # 编码
        data = text.encode('ascii')
        sock.sendto(data, address)


def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'this is client ,The time is {}'.format(datetime.now())
    # 编码，转换为字节
    data = text.encode('ascii')
    # client 未进行bind ,使用随机端口
    sock.sendto(data, ('127.0.0.1', port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)  # Danger! See Chapter 2
    # 解码
    text = data.decode('ascii')
    print('The server {} replied :{}'.format(address, text))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    # 默认端口为1060
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')

    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
