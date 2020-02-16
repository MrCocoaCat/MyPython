# -*- coding: utf-8 -*-
# @Time    : 2020/2/15 17:26
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : listen.py
import time
import sys
import stomp


class MyListener(stomp.ConnectionListener):

    def __init__(self, print_to_log=False, con=None):
        self.print_to_log = print_to_log
        self.conn = con

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

    def on_heartbeat_timeout(self):
        self.__print('on_heartbeat_timeout')

    def on_before_message(self, headers, body):
        """
        Called by the STOMP connection before a message is returned to the client app.
        Returns a tuple containing the headers and body
        (so that implementing listeners can pre-process the content).
        :param dict headers:
        :param body:
        """
        #self.__print('on_before_message %s %s', headers, body)
        return headers, body

    def on_message(self, headers, body):
        """
        Called by the STOMP connection when a MESSAGE frame is received.
        :param dict headers:
        :param body:
        """
        # self.__print('on_message %s %s', headers, body)
        # message_id = headers['message-id']
        ack_id = headers.setdefault('message-id', None)
        subscription = headers.setdefault('subscription',None)
        # print(message_id)
        time.sleep(1)
        print(" finish %s" % body)
        if ack_id and subscription:
            self.conn.ack(ack_id,subscription)
            print("ack %s " % ack_id)


    def on_receipt(self, headers, body):
        """
        :param dict headers:
        :param body:
        """
        self.__print('on_receipt %s %s', headers, body)

    def on_error(self, headers, body):
        """
        :param dict headers:
        :param body:
        """
        self.__print('on_error %s %s', headers, body)

    def on_send(self, frame):
        """
        :param Frame frame:
        """
        # self.__print('on_send %s %s %s', frame.cmd, frame.headers, frame.body)

    def on_heartbeat(self):
        self.__print('on_heartbeat')
