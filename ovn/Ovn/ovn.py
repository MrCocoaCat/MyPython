# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py

class SwitchPort():
    def __init__(self, name,
                 num=None,
                 mac=None,
                 ip=None,
                 type=None,
                 uuid=None,
                 options=None):
        pass


class RoutePort():
    def __init__(self, name, ip, num=None, mac=None, peer=None):
        self.ip = ip
        self.peer = peer


class Switch():
    def __init__(self, name, uuid=None, acls=None, dns_records=None, external_ids=None,
                 load_balancer=None, other_config=None, ports=None, qos_rules=None):
        self._uuid = uuid
        self.acls = acls or []
        self.dns_records = dns_records or []
        self.external_ids = external_ids or {}
        self.load_balancer = load_balancer or []
        self.other_config = other_config or {}
        self.ports = ports or []
        self.qos_rules = qos_rules or []


class Router():
    def __init__(self, name, uuid=None, options=None):
        self.uuid = uuid
        self.options = options
        self._route_list = []
        self._nat_list = []



class DHCP():
    def __init__(self, cidr, server_id=None, server_mac=None, router=None, lease_time=None):
        self.uuid = None


class OvnNb:
    def __init__(self):
        self.ls_dict = {}
        self.lr_dict = {}



"""
ovn-nbctl --columns=name list Logical_Router_Port    --format=json
"""

