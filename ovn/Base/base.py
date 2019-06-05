# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 10:46
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : base.py
import re
import subprocess
import os
ROOT = os.path.dirname(os.path.realpath(__file__))

def run_command(cmd, redirect_output=True, check_exit_code=True):
    """
    执行命令，在一个程序外的shell进程,
    执行目录为ROOT
    """
    if redirect_output:
        stdout = subprocess.PIPE
    else:
        stdout = None
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout)
    output = proc.communicate()[0]
    if check_exit_code and proc.returncode != 0:
        # 程序不返回0，则失败
        err = 'Command "%s" failed.: %s' % (cmd, output)
        #e = CmdException(err)
        raise Exception(err)
    return output



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
        self._ports_list = []


class RouterBase:
    def __init__(self, name):
        self.name = name
        self._ports_list = []