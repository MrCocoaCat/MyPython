# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py


import yaml
from tools.install_venv import run_command
import re

num = 1


def generate_mac():
    global num
    num += 1
    pattern = re.compile('.{2}')
    mac = ':'.join(pattern.findall(str("%012x" % num)))
    return mac


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


class NAT(LogicalBase):
    """
    NAT
    NAT rules
    """
    def __init__(self, _uuid=None, external_ids=None, external_ip=None, external_mac=None,
                 logical_ip=None, logical_port=None, type=None):
        LogicalBase.__init__(self, _uuid)
        self.external_ids = external_ids
        self.external_ip = external_ip
        self.external_mac = external_mac
        self.logical_ip = logical_ip
        self.logical_port = logical_port
        nat_type_tup = ("snat", "dnat", "dnat_and_snat")
        if type in nat_type_tup:
            self.type = type
        else:
            raise Exception("wrong type")

class RouterStaticRoute(LogicalBase):
    def __init__(self,_uuid, external_ids=None, ip_prefix=None,
                 nexthop =None, output_port=None, policy=None):
        LogicalBase.__init__(self,_uuid)
        self.external_ids = external_ids
        self.ip_prefix = ip_prefix
        self.nexthop = nexthop
        self.output_port = output_port
        self.policy = policy

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
        if isinstance(dhcpv4_options, DHCP):
            self.dhcpv4_options = dhcpv4_options.get_uuid()
        else:
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

    def syn(self):
        cmd = ['ovn-nbctl', '-f', 'json', 'list', 'Logical_Switch_Port', self.name]
        re = run_command(cmd)
        # js = json.loads(re, encoding='utf-8')
        js = yaml.safe_load(re)
        data = js["data"]
        head = js["headings"]
        data = [self.cell(i) for i in data[0]]
        self.__dict__ = dict(zip(head, data))


class Switch(LogicalBase):
    """
    Logical_Switch
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

    def add_port(self, port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")

        cmd = ['ovn-nbctl', 'lsp-add', self.name, port.name]
        run_command(cmd, check_exit_code=True)

        self._set_addresses(port)
        self._set_type(port)
        self._set_options(port)
        self._set_dhcpv4_options(port)
        port.syn()
        if port.addresses == 'dynamic':
            self.set_port_security(port)
            port.syn()

    def add_ports(self, ports_list):
        for port in ports_list:
            self.add_port(port)

    def del_port(self, port):
        if isinstance(port, SwitchPort):
            port_name = port.name
        elif isinstance(port, str):
            port_name = port
        else:
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-del', self.name, port_name]
        run_command(cmd, check_exit_code=True)

    def _set_addresses(self, port):
        cmd = ['ovn-nbctl', 'lsp-set-addresses', port.name]
        if isinstance(port.addresses,str):
            cmd.append(port.addresses)
        if isinstance(port.addresses, list):
            cmd.extend(port.addresses)
        run_command(cmd, check_exit_code=True)

    def set_port_security(self, port):
        cmd = ['ovn-nbctl', 'lsp-set-port-security', port.name, port.dynamic_addresses]
        run_command(cmd, check_exit_code=True)

    def _set_dhcpv4_options(self, port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")
        if not isinstance(port.dhcpv4_options, str):
            return

        cmd = ['ovn-nbctl', 'lsp-set-dhcpv4-options', port.name, port.dhcpv4_options]
        re = run_command(cmd, check_exit_code=True)
        return re

    @staticmethod
    def _set_type(port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-set-type', port.name, port.type]
        if port.type is not None:
            run_command(cmd, check_exit_code=True)

    @staticmethod
    def _set_options(port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-set-options', port.name]
        if port.options:
            for key, val in port.options.items():
                option = key + "=" + val
                cmd.append(option)
            # print(cmd)
        run_command(cmd, check_exit_code=True)


class RoutePort(LogicalBase):
    """
    Logical_Router_Port
    logical router port
    """
    def __init__(self, name, _uuid=None, enabled=None, external_ids=None, gateway_chassis=None,
                 ipv6_ra_configs=None, mac=None, network=None, options=None, peer=None):
        LogicalBase.__init__(self, _uuid)
        self.name = name
        self.enabled = enabled or []
        self.external_ids = external_ids or {}
        self.gateway_chassis = gateway_chassis or []
        self.ipv6_ra_configs = ipv6_ra_configs or {}
        self.mac = mac or ""
        self.network = network or []
        self.options = options
        self.peer = peer


class Router(LogicalBase):
    """
    Logical_Router
    L3 logical router      |
    """
    def __init__(self, _uuid=None, enabled=None, external_ids=None, load_balancer=None,name=None, nat=None
                 , options=None, ports=None, static_routes=None):
        LogicalBase.__init__(self, _uuid)
        self.name = name
        self.enabled = enabled or []
        self.external_ids = external_ids or {}
        self.load_balancer = load_balancer or []
        self.nat = nat or []
        self.options = options or {}
        self.ports = ports or []
        self.static_routes =static_routes or []

    def add_port(self, port):
        if not isinstance(port, RoutePort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lrp-add', self.name, port.name, port.mac]
        if isinstance(port.network, list):
            cmd.extend(port.network)
        if isinstance(port.network, str):
            cmd.append(port.network)
        if port.peer is not None:
            cmd.append("peer="+port.peer)
        print(cmd)
        run_command(cmd, check_exit_code=True)

    def add_ports(self, port_list):
        for port in port_list:
            self.add_port(port)

    def del_port(self, port):
        if not isinstance(port, RoutePort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lrp-del', self.name, port.name]
        run_command(cmd, check_exit_code=True)

    def del_ports(self, port_list):
        for port in port_list:
            self.del_port(port)

    def add_route(self, prefix, nexthop):
        cmd = ['ovn-nbctl', 'lr-route-add', self.name, prefix, nexthop]
        run_command(cmd, check_exit_code=True)

    def del_route(self, prefix=None):
        cmd = ['ovn-nbctl', 'lr-route-add', self.name]
        if prefix is not None:
            cmd.append(prefix)
        run_command(cmd, check_exit_code=True)

    def add_nat(self, nat):
        if not isinstance(nat, NAT):
            raise Exception("type")
        cmd = ['ovn-nbctl', 'lr-nat-add', self.name, nat.type, nat.external_ip, nat.logical_ip]
        if nat.logical_port is not None:
            cmd.append(nat.logical_port)
        if nat.external_mac is not None:
            cmd.append(nat.external_mac)
        run_command(cmd, check_exit_code=True)


class DHCP(LogicalBase):
    def __init__(self, _uuid=None, cidr=None, server_id=None, server_mac=None, router=None, lease_time=None):
        LogicalBase.__init__(self, _uuid)
        #self._uuid = _uuid
        self._create_DHCP_Options(cidr)
        self.dhcp_option_set_options(self._uuid, server_id, server_mac, router, lease_time)

    def _create_DHCP_Options(self, cidr):
        cmd = ['ovn-nbctl', 'create', 'DHCP_Options', 'cidr='+str(cidr)]
        re = run_command(cmd, check_exit_code=True)
        self._uuid = re.strip('\n')
        return re

    def dhcp_option_set_options(self, dhcp_option, server_id, server_mac, router, lease_time):
        cmd = ['ovn-nbctl', 'dhcp-options-set-options', dhcp_option,
               'server_id='+str(server_id),
               'server_mac='+server_mac,
               'router='+router,
               'lease_time='+str(lease_time)]
        re = run_command(cmd, check_exit_code=True)
        return re


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

    def add_router(self, router):
        if not isinstance(router, Router):
            raise Exception("wrong ")
        cmd = ['ovn-nbctl', 'create', 'Logical_Router']
        for key, val in router.__dict__.items():
            if key == "_uuid":
                continue
            if val:
                option = key + "=" + str(val)
                cmd.append(option)
        uuid = run_command(cmd).strip('\n')
        router.set_uuid(uuid)
        self.switch_dict.setdefault(uuid, router.name)
        return router




