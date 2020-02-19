# -*- coding: utf-8 -*-
# @Time    : 2020/2/19 14:58
# @Author  : liyubo
# @Email   : liyubo@iie.ac.cn
import time
import sys
import stomp


class MyListener(stomp.ConnectionListener):

    def __init__(self, conn, print_to_log=False,):
        self.print_to_log = print_to_log
        self._conn = conn

    def __print(self, msg, *args):
        print(msg % args)

    def on_connecting(self, host_and_port):
        """
        :param (str,int) host_and_port:
        """
        self.__print('on_connecting %s %s', *host_and_port)

    def on_connected(self, headers, body):
        """
        :param dict headers:
        :param body:
        """
        self.__print('on_connected %s %s', headers, body)

    def on_disconnected(self):
        self.__print('on_disconnected')

    def on_message(self, headers, body):
        """
        Called by the STOMP connection when a MESSAGE frame is received.
        :param dict headers:
        :param body:
        """
        ack_id = headers.setdefault('message-id', None)
        subscription = headers.setdefault('subscription', None)
        # deal with something
        print("deal with  %s" % body)
        time.sleep(1)
        # deal over
        if ack_id and subscription:
            # send ACK frame
            self._conn.ack(ack_id, subscription)


def Producer():
    conn = stomp.Connection12([('192.168.83.132', 61613)])
    conn.connect('admin', 'password', wait=True)
    for i in range(1000):
        mes = str(i)
        # '/topic/q1' 表示名为test 的topic
        # '/queue/q1' 表示名为test 的queue
        conn.send(body=mes, destination='/queue/test')
        print("send %s" % mes)
        time.sleep(1)
    conn.disconnect()


def Consumer():
    conn = stomp.Connection([('192.168.83.132', 61613)])
    conn.set_listener('1', MyListener(conn=conn))
    conn.connect('admin', 'password', wait=True)
    try:
        conn.subscribe(destination='/queue/test', id="c1", ack='client-individual')
        while True:
            pass
    except KeyboardInterrupt:
        conn.disconnect()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("input argument."
              " 'c' is Consumer"
              " 'p' is Producer")
    else:
        argument_dict = {'c': Consumer, 'p': Producer}
        fun = argument_dict[sys.argv[1]]
        fun()
