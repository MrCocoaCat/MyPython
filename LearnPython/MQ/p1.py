# -*- coding: utf-8 -*-
# @Time    : 2020/2/14 19:41
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : activemq1.py

import time
import stomp

conn = stomp.Connection12([('192.168.83.132', 61613)])
conn.connect('admin', 'password', wait=True)
i = 0
while True:
    i += 1
    mes = str(i)
    conn.send(body=mes, destination='q1')
    print("send %s" % mes)
conn.disconnect()
