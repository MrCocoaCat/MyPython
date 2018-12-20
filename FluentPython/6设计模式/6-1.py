# -*- coding: utf-8 -*-
# @Time    : 2018/12/20 13:19
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 6-1.py

from abc import ABC,abstractmethod
from collections import namedtuple


Customer = namedtuple('Customer', 'name fidelity')
