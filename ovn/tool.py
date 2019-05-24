# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 15:38
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : tool.py

import os
import subprocess


class CmdException(Exception):
    def __init__(self, err):
        self.err = err


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
