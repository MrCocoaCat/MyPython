# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 11:13
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : port.py
import re

class port:
    def __init__(self, num, name=None, mac=None):
        self.num = num

        if name:
            self.name = name
        else:
            self._genname()

        if mac:
            self.mac = mac
        else:
            self._genmac()

    def _genmac(self):
        pattern = re.compile('.{2}')
        self.mac = ':'.join(pattern.findall(str("%012x" % self.num)))

    def _genname(self):
        self.name = "tap" + str(self.num)

