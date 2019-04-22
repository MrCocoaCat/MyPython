# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 9:27
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : creat.py

import os
import subprocess
import sys

# ROOT 路径，本脚本所在的绝对路径的上层路径
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 执行系统命令函数
def run_command(cmd, redirect_output=True, check_exit_code=True):
    """
    执行命令，在一个程序外的shell进程，执行目录为ROOT
    """
    # subprocess模块用于产生子进程
    # 如果参数为redirect_output ，则创建PIPE
    if redirect_output:
        stdout = subprocess.PIPE
    else:
        stdout = None
    # cwd 参数指定子进程的执行目录为ROOT，执行cwd 函数
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout)
    # 如果子进程输出了大量数据到stdout或者stderr的管道，并达到了系统pipe的缓存大小的话，
    # 子进程会等待父进程读取管道，而父进程此时正wait着的话，将会产生死锁。

    # 使用communicate() 返回值为 (stdoutdata , stderrdata )
    output = proc.communicate()[0]
    if check_exit_code and proc.returncode != 0:
        # 程序不返回0，则失败
        raise Exception('Command "%s" failed.\n%s' % (' '.join(cmd), output))
    return output


def create_bridge():
 pass