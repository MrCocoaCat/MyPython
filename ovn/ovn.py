# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : ovn.py

from tool import run_command


class OvnNb:
    def __init__(self):
        pass

    @staticmethod
    def ls_add(ls):
        cmd = ['ovn-nbctl', 'ls-add', ls]
        run_command(cmd, check_exit_code=False)

    @staticmethod
    def lsp_add(lsp):
        cmd = ['ovn-nbctl', 'lsp-add', lsp]
        run_command(cmd, check_exit_code=False)
