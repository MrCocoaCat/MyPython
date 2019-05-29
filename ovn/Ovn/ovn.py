# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py

from tool import run_command
from Base.base import *


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
        #print("OvnPort",self.mac)


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
        self.ip = ip
        self.options = options


class RoutePort(OvnPort):
    def __init__(self, name, ip, num=None, mac=None):
        OvnPort.__init__(self, name, mac=mac, num=num)
        self.ip = ip


class Switch(SwitchBase):
    def __init__(self, name, uuid=None):
        SwitchBase.__init__(self, name=name)
        self.uuid = uuid
        #self._syn_ports()

    def _syn_ports(self):
        cmd = ['ovn-nbctl', 'lsp-list', self.name]
        res = run_command(cmd, check_exit_code=True)
        lines = res.splitlines()
        for line in lines:
            ltemp = line.split()
            name = ltemp[1].strip('()')
            uuid = ltemp[0]
            s = SwitchPort(name=name, uuid=uuid)
            self.ports.append(s)

    def lsp_add(self, port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")

        cmd = ['ovn-nbctl', 'lsp-add', self.name, port.name]
        run_command(cmd, check_exit_code=True)
        self.ports.append(port)

        self.lsp_set_addresses(port)
        self.lsp_set_type(port)
        self.lsp_set_options(port)

    def ls_add_ports(self,ports_list):
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
        self.ports.pop(port)

    def lsp_set_addresses(self, port, mac=None, ip=None):
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

    def lsp_set_port_security(self, port, mac=None,ip=None):
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

    def ovn_nbctl_lsp_set_dhcpv4_options(self, port, dhcp):
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

    def lsp_set_type(self, port):
        if not isinstance(port, SwitchPort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lsp-set-type', port.name, port.type]
        if port.type is not None:
            run_command(cmd, check_exit_code=True)

    def lsp_set_options(self, port):
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

    def _syn_ports(self):
        cmd = ['ovn-nbctl', 'lsp-list', self.name]
        res = run_command(cmd, check_exit_code=True)
        lines = res.splitlines()
        for line in lines:
            ltemp = line.split()
            name = ltemp[1].strip('()')
            uuid = ltemp[0]
            s = SwitchPort(name=name, uuid=uuid)
            self.ports.append(s)

    def lrp_add(self, port):
        if not isinstance(port, RoutePort):
            raise Exception("wrong type")
        cmd = ['ovn-nbctl', 'lrp-add', self.name, port.name, port.mac, port.ip]
        run_command(cmd, check_exit_code=True)
        self.ports.append(port)

    def lr_add_ports(self, port_list):
        for port in port_list:
            self.lrp_add(port)

    def lrp_del(self):
        pass


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




