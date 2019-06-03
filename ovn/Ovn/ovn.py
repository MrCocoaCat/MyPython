# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py


from Base.base import PortBase
from Base.base import SwitchBase
from Base.base import RouterBase
from Base.base import run_command

class CmdException(Exception):
    def __init__(self, err):
        self.err = err


class OvnPort(PortBase):
    id = 1

    def __init__(self, name, mac=None, num=None, uuid=None):
        PortBase.__init__(self, name=name)
        # print("init OvnPorts")
        if num is None:
            self.num = OvnPort.id
            # print("num is %s" % num)
            OvnPort.id += 1
        else:
            self.num = num
        if mac is not None:
            self.mac = mac
        else:
            self.mac = self._gen_mac(self.num)

        self.uuid = uuid


class SwitchPort(OvnPort):
    def __init__(self, name,
                 num=None,
                 mac=None,
                 ip=None,
                 type=None,
                 uuid=None,
                 options=None):
        OvnPort.__init__(self, name, mac=mac, num=num, uuid=uuid)
        self._type_tup = ("router", "localnet", "localport", "l2gateway", "vtep")
        if type in self._type_tup:
            self.type = type
        else:
            self.type = None
        if (mac is None) and (self.type =="router") :
            self.mac = "router"
        self.ip = ip
        self.options = options


class RoutePort(OvnPort):
    def __init__(self, name, ip, num=None, mac=None, peer=None):
        OvnPort.__init__(self, name, mac=mac, num=num)
        self.ip = ip
        self.peer = peer


class Switch(SwitchBase):
    def __init__(self, name, uuid=None, acls=None, dns_records=None, external_ids=None,
                 load_balancer=None, other_config=None, ports=None, qos_rules=None):
        SwitchBase.__init__(self, name=name)
        self._uuid = uuid
        self.acls = acls or []
        self.dns_records = dns_records or []
        self.external_ids = external_ids or {}
        self.load_balancer = load_balancer or []
        self.other_config = other_config or {}
        self.ports = ports or []
        self.qos_rules = qos_rules or []
    # def _syn_ports(self):
    #     cmd = ['ovn-nbctl', 'lsp-list', self.name]
    #     res = run_command(cmd, check_exit_code=True)
    #     lines = res.splitlines()
    #     for line in lines:
    #         ltemp = line.split()
    #         name = ltemp[1].strip('()')
    #         uuid = ltemp[0]
    #         s = SwitchPort(name=name, uuid=uuid)
    #         self._ports_list.append(s)

    def lsp_add(self, port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")

        cmd = ['ovn-nbctl', 'lsp-add', self.name, port.name]
        run_command(cmd, check_exit_code=True)
        #self.ports.append(port)
        self.lsp_set_addresses(port)
        self.lsp_set_type(port)
        self.lsp_set_options(port)

    def ls_add_ports(self, ports_list):
        for port in ports_list:
            self.lsp_add(port)

    def lsp_del(self, port):
        if isinstance(port, SwitchPort):
            port_name = port.name
        elif isinstance(port, str):
            port_name = port
        else:
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-del', self.name, port_name]
        run_command(cmd, check_exit_code=True)
        #self.ports.pop(port)

    @staticmethod
    def lsp_set_addresses(port, mac=None, ip=None):
        tem_mac = None
        tem_ip = None
        if isinstance(port, SwitchPort):
            port_name = port.name
            if port.mac is not None:
                tem_mac = port.mac
            if port.ip is not None:
                tem_ip = port.ip
        elif isinstance(port, str):
            port_name = port
            if ip is not None:
                tem_ip =ip
            if mac is not None:
                tem_mac = mac
        else:
            raise Exception("wrong type")

        if tem_mac is None:
            raise Exception("type")
        if tem_ip is not None:
            option = tem_mac + " " + tem_ip
        else:
            option = tem_mac
        cmd = ['ovn-nbctl', 'lsp-set-addresses', port_name, option]
        run_command(cmd, check_exit_code=True)

    @staticmethod
    def lsp_set_port_security(port, mac=None, ip=None):
        tem_mac = None
        tem_ip = None
        if isinstance(port, SwitchPort):
            port_name = port.name
            if port.mac is not None:
                tem_mac = port.mac
            if port.ip is not None:
                tem_ip = port.ip
        elif isinstance(port, str):
            port_name = port
            if ip is not None:
                tem_ip = ip
            if mac is not None:
                tem_mac = mac
        else:
            raise Exception("wrong type")

        if tem_mac is None:
            raise Exception("type")
        if tem_ip is not None:
            option = tem_mac + " " + tem_ip
        else:
            option = tem_mac
        cmd = ['ovn-nbctl', 'lsp-set-port-security', port_name, option]
        run_command(cmd, check_exit_code=True)

    @staticmethod
    def ovn_nbctl_lsp_set_dhcpv4_options(port, dhcp):
        if isinstance(port, SwitchPort):
            tem_port = port
        elif isinstance(port, str):
            tem_port = SwitchPort(port)
        else:
            raise Exception("wrong type")

        if not isinstance(dhcp, DHCP):
            raise Exception("wrong type")

        cmd = ['ovn-nbctl', 'lsp-set-dhcpv4-options', tem_port.name, dhcp.uuid]
        re = run_command(cmd, check_exit_code=True)
        return re

    @staticmethod
    def lsp_set_type(port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-set-type', port.name, port.type]
        if port.type is not None:
            run_command(cmd, check_exit_code=True)

    @staticmethod
    def lsp_set_options(port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-set-options', port.name]
        if port.options:
            for key, val in port.options.items():
                option = key + "=" + val
                cmd.append(option)
            #print(cmd)
        run_command(cmd, check_exit_code=True)


class Router(RouterBase):
    def __init__(self, name, uuid=None, options=None):
        RouterBase.__init__(self, name=name)
        self.uuid = uuid
        self.options = options
        self._route_list = []
        self._nat_list = []

    def _syn_ports(self):
        cmd = ['ovn-nbctl', 'lsp-list', self.name]
        res = run_command(cmd, check_exit_code=True)
        lines = res.splitlines()
        for line in lines:
            ltemp = line.split()
            name = ltemp[1].strip('()')
            uuid = ltemp[0]
            s = SwitchPort(name=name, uuid=uuid)
            self._ports_list.append(s)

    def _syn_nats(self):
        pass

    def _syn_routes(self):
        pass

    def add_port(self, port):
        if not isinstance(port, RoutePort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lrp-add', self.name, port.name, port.mac, port.ip]
        if port.peer is not None:
            cmd.append("peer="+port.peer)
        run_command(cmd, check_exit_code=True)
        self._ports_list.append(port)

    def add_ports(self, port_list):
        for port in port_list:
            self.add_port(port)

    def del_port(self, port):
        if not isinstance(port, RoutePort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lrp-del', self.name, port.name]
        run_command(cmd, check_exit_code=True)
        self._ports_list.pop(port)

    def del_ports(self,port_list):
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

    def add_nat(self, nat_type, external_ip, logical_ip, logical_port=None, external_mac=None):
        nat_type_tup = ("snat", "dnat", "dnat_and_snat")
        if nat_type not in nat_type_tup:
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lr-nat-add', self.name, nat_type, external_ip, logical_ip]
        if logical_port is not None:
            cmd.append(logical_port)
        if external_mac is not None:
            cmd.append(external_mac)
        run_command(cmd, check_exit_code=True)


class OvnNb:
    def __init__(self):
        self.ls_dict = {}
        self.lr_dict = {}
        self._syn_dict()

    def clean(self):
        for key in self.ls_dict.values():
            self.ls_del(key)
        for key in self.lr_dict.values():
            self.lr_del(key)

    def _syn_dict(self):
        res = run_command(['ovn-nbctl', 'ls-list'], check_exit_code=True)
        lines = res.splitlines()
        for line in lines:
            ltemp = line.split()
            name = ltemp[1].strip('()')
            uuid = ltemp[0]
            s = Switch(name=name, uuid=uuid)
            self.ls_dict.setdefault(s.name, s)
        res = run_command(['ovn-nbctl', 'lr-list'], check_exit_code=True)
        lines = res.splitlines()
        for line in lines:
            ltemp = line.split()
            name = ltemp[1].strip('()')
            uuid = ltemp[0]
            s = Router(name=name, uuid=uuid)
            self.lr_dict.setdefault(s.name, s)

    def ls_add(self, ls):
        if not isinstance(ls, SwitchBase):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'ls-add', ls.name]
        run_command(cmd, check_exit_code=True)
        self.ls_dict.setdefault(ls.name, ls)

    def ls_adds(self, ls_list):
        for ls in ls_list:
            self.ls_add(ls)

    def ls_del(self, ls):
        cmd = ['ovn-nbctl', 'ls-del', ls.name]
        run_command(cmd, check_exit_code=True)
        self.ls_dict.pop(ls.name)

    def lr_add(self, lr):
        if not isinstance(lr, RouterBase):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'create', 'Logical_Router', 'name='+lr.name]
        if lr.options:
            for key, val in lr.options.items():
                cmd.append("options:"+key+"="+val)
        run_command(cmd, check_exit_code=True)
        self.lr_dict.setdefault(lr.name, lr)

    def lr_del(self, lr):
        if not isinstance(lr, RouterBase):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lr-del', lr.name]
        run_command(cmd, check_exit_code=True)
        self.lr_dict.pop(lr.name)


class DHCP():
    def __init__(self, cidr, server_id=None, server_mac=None, router=None, lease_time=None):
        self.uuid = None
        self._create_DHCP_Options(cidr)
        self.dhcp_option_set_options(self.uuid, server_id, server_mac, router, lease_time)

    def _create_DHCP_Options(self, cidr):
        cmd = ['ovn-nbctl', 'create', 'DHCP_Options', 'cidr='+str(cidr)]
        re = run_command(cmd, check_exit_code=True)
        self.uuid = re.strip('\n')
        return re

    def dhcp_option_set_options(self, dhcp_option, server_id, server_mac, router, lease_time):

        cmd = ['ovn-nbctl', 'dhcp-options-set-options', dhcp_option,
               'server_id='+str(server_id),
               'server_mac='+server_mac,
               'router='+router,
               'lease_time='+str(lease_time)]
        re = run_command(cmd, check_exit_code=True)
        return re



"""
ovn-nbctl --columns=name list Logical_Router_Port    --format=json
"""

