# -*- coding: utf-8 -*-
# @Time    : 2020/2/14 21:30
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 1.py
import stomp
from MQ.listen import MyListener

conn = stomp.Connection([('192.168.83.132', 61613)])
conn.set_listener('1', MyListener(con=conn))
conn.connect('admin', 'password', wait=True)

try:
    conn.subscribe(destination='/topic/topic1', id="c1", ack='client-individual')
    # conn.unsubscribe("1")
    while True:
        pass
except Exception():
    conn.disconnect()

