# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py

from tool import run_command


class Switch:
    def __init__(self, name, uuid=None):
        self.name = name
        self.uuid = uuid
        self.port = []



class OvnNb:
    def __init__(self):
        self.ls_dict = {}
        self._syn_ls_dict()
        #self.lsp_dict = {}
        pass

    def clean(self):
        print(self.ls_dict)
        keys = self.ls_dict.keys()
        for key in keys:
            self.ls_del(key)

    def _syn_ls_dict(self):
        cmd = ['ovn-nbctl', 'ls-list']
        res = run_command(cmd, check_exit_code=True)
        lines = res.splitlines()
        for line in lines:
            ltemp = line.split()
            name = ltemp[1].strip('()')
            uuid = ltemp[0]
            s = Switch(name=name, uuid=uuid)
            self.ls_dict.setdefault(s.name, s)

    def ls_add(self, ls):
        s = Switch(name=ls)
        cmd = ['ovn-nbctl', 'ls-add', ls]
        run_command(cmd, check_exit_code=True)
        self.ls_dict.setdefault(s.name, s)

    def ls_del(self, ls):
        cmd = ['ovn-nbctl', 'ls-del', ls]
        run_command(cmd, check_exit_code=True)
        self.ls_dict.pop(ls)

    def lsp_add(self, ls, lsp):
        cmd = ['ovn-nbctl', 'lsp-add', ls, lsp]
        run_command(cmd, check_exit_code=True)
        #val = self.lsp_dict.setdefault(ls, [])
        #val.append(lsp)

    def lsp_del(self, ls, lsp):
        cmd = ['ovn-nbctl', 'lsp-del', ls, lsp]
        run_command(cmd, check_exit_code=True)
        #val = self.lsp_dict.setdefault(ls, default=[])
        #val.remove(lsp)

    @staticmethod
    def lsp_set_addresses(lsp, mac, ip=None):
        if not ip is None:
            option = mac + " " + ip
        else:
            option = mac
        cmd = ['ovn-nbctl', 'lsp-set-addresses', lsp, option]
        run_command(cmd, check_exit_code=True)

    @staticmethod
    def lsp_set_port_security(lsp, mac, ip=None):
        if not ip is None:
            option = mac + " " + ip
        else:
            option = mac
        cmd = ['ovn-nbctl', 'lsp-set-port-security', lsp, option]
        run_command(cmd, check_exit_code=True)

    @staticmethod
    def create_DHCP_Options(self, cidr):
        cmd = ['ovn-nbctl', 'create', 'DHCP_Options', 'cidr='+str(cidr)]
        re = run_command(cmd, check_exit_code=True)
        return re.strip('\n')

    @staticmethod
    def dhcp_option_set_options(self, dhcp_option, server_id, server_mac, router, lease_time):
        cmd = ['ovn-nbctl', 'dhcp-options-set-options', dhcp_option,
               'server_id='+str(server_id),
               'server_mac='+server_mac,
               'router='+router,
               'lease_time='+str(lease_time)]
        re = run_command(cmd, check_exit_code=True)
        print(re)
        return re

    def ovn_nbctl_lsp_set_dhcpv4_options(self, port, dhcp_options):
        cmd = ['ovn-nbctl', 'lsp-set-dhcpv4-options', port, dhcp_options]
        re = run_command(cmd, check_exit_code=True)
        return re







