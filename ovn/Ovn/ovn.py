# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py


import yaml
from tools.install_venv import run_command


class LogicalBase:
    def __init__(self, uuid):
        self._uuid = uuid

    def __repr__(self):
        return "{}:{}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def set_uuid(self, uuid):
        if self.no_uuid():
            self._uuid = uuid
        else:
            raise Exception("")

    def get_uuid(self):
        if self.no_uuid():
            raise Exception("")
        else:
            return self._uuid

    def no_uuid(self):
        if self._uuid is None:
            return True
        else:
            return False


class SwitchPort(LogicalBase):
    """
     Logical_Switch_Port Table
     L2 logical switch port
    """
    def __init__(self, name, _uuid=None, addresses=None, dhcpv4_options=None,  dhcpv6_options=None,
                 dynamic_addresses=None, enabled=None, external_ids=None,
                 options=None, parent_name=None, port_security=None,
                 tag=None, tag_request=None, type=None,  up=None,  data_dict=None):
        LogicalBase.__init__(self, _uuid)
        # self._uuid = _uuid,
        self.addresses = addresses or []
        self.dhcpv4_options = dhcpv4_options or []
        self.dhcpv6_options = dhcpv6_options or []
        self.dynamic_addresses = dynamic_addresses or []
        self.enabled = enabled or []
        self.external_ids = external_ids or {}
        self.name = name
        self.options = options or {}
        self.parent_name = parent_name or []
        self.port_security = port_security or []
        self.tag = tag or []
        self.tag_request = tag_request or []
        self.type = type or ""
        if up:
            self.up = "true"
        else:
            self.up = "false"
        if isinstance(data_dict, dict):
            self.__dict__ = data_dict


class Switch(LogicalBase):
    """
    Logical_Switch  Table
    L2 logical switch
    """
    def __init__(self, name, _uuid=None, acls=None, dns_records=None, external_ids=None,
                 load_balancer=None, other_config=None, ports=None, qos_rules=None, data_dict=None):
        LogicalBase.__init__(self, _uuid)
        self.name = name
        # self._uuid = _uuid
        self.acls = acls or []
        self.dns_records = dns_records or []
        self.external_ids = external_ids or {}
        self.load_balancer = load_balancer or []
        self.other_config = other_config or {}
        self.ports = ports or []
        self.qos_rules = qos_rules or []
        if isinstance(data_dict, dict):
            self.__dict__ = data_dict


class RoutePort:
    def __init__(self, name, ip, num=None, mac=None, peer=None):
        self.ip = ip
        self.peer = peer


class Router:
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
        self.switch_dict = {}

    def cell(self, l):
        if isinstance(l, list) and len(l) == 2:
            if l[0] == "map":
                return dict(l[1])
            if l[0] == "set":
                return [self.cell(i) for i in l[1]]
            if l[0] == "uuid":
                return str(l[1])
        else:
            return l

    def add_switch(self, switch):
        if not isinstance(switch, Switch):
            raise Exception("wrong ")
        cmd = ['ovn-nbctl', 'create', 'Logical_Switch']
        for key, val in switch.__dict__.items():
            if key == "_uuid":
                continue
            if val:
                option = key + "=" + str(val)
                cmd.append(option)
        uuid = run_command(cmd).strip('\n')
        switch.set_uuid(uuid)
        self.switch_dict.setdefault(uuid, switch.name)
        return switch

    def get_switch(self, name):
        cmd = ['ovn-nbctl', '-f', 'json', 'list', 'Logical_Switch', name]
        re = run_command(cmd)
        #js = json.loads(re, encoding='utf-8')
        js = yaml.safe_load(re)
        data = js["data"]
        head = js["headings"]
        data = [self.cell(i) for i in data[0]]
        data_dict = dict(zip(head, data))
        return Switch(name, data_dict=data_dict)


    def add_switch_port(self, port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong ")
        cmd = ['ovn-nbctl', '--id=@'+port.name, 'create', 'Logical_Switch_Port']
        for key, val in port.__dict__.items():
            if key == "_uuid" or key == "name":
                continue
            if val:
                option = key + "=" + str(val)
                cmd.append(option)
        uuid = run_command(cmd).strip('\n')
        port.set_uuid(uuid)
        #self.switch_dict.setdefault(uuid, port.name)
        return port





