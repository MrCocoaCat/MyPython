# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 10:46
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : base.py
import re


class PortBase:
    def __init__(self, name, mac=None, num=None):
        self.name = name
        self.num = num
        self.mac = mac
        if self.mac is None and self.num is not None:
            self.mac = self._gen_mac(self.num)

    def _gen_mac(self, num):
        pattern = re.compile('.{2}')
        return ':'.join(pattern.findall(str("%012x" % num)))


class SwitchBase:
    def __init__(self, name):
        self.name = name
        self.ports = []


class RouterBase:
    def __init__(self, name):
        self.name = name
        self.ports = []