# -*- coding: utf-8 -*-
# @Time    : 2020/2/14 21:30
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : c2.py
import stomp
from MQ.listen import MyListener

conn = stomp.Connection([('192.168.83.132', 61613)])
conn.set_listener('2', MyListener(con=conn))
conn.connect('admin', 'password', wait=True)

try:
    conn.subscribe(destination='/topic/topic1', id="c2", ack='client-individual')
    while True:
        pass
except Exception():
    conn.unsubscribe("1")
    conn.disconnect()

