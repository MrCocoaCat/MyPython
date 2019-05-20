# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 17:17
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : main.py

from createxml import CreatXml
from tool import run_command
from ovn import OvnNb
import uuid
import os
import sys
import argparse



dirroot = '/root/liyubo/ovn-test2'

def clean(num):
    for i in range(1, num):
        dirname = "ovn-" + str(i)
        dirpath = os.path.join(dirroot, dirname)
        port = 6000 + i
        name = "ovn-" + str(port)
        qcow2_name = 'ubuntu-' + str(i) + '.qcow2'
        source_file = os.path.join(dirpath, qcow2_name)
        xmlname = name + '.xml'
        xmlpath = os.path.join(dirpath, xmlname)
        # 删除文件夹
        if os.path.exists(source_file):
            os.remove(source_file)
        if os.path.exists(xmlpath):
            os.remove(xmlpath)
        if os.path.exists(dirpath):
            os.rmdir(dirpath)
            # 关闭虚拟机
        cmd = ['virsh', 'destroy', name]
        re = run_command(cmd, check_exit_code=False)
        print(re)


def start(num):
    for i in range(1, num):
        dirname = "ovn-" + str(i)
        dirpath = os.path.join(dirroot, dirname)
        vm_uuid = uuid.uuid1()
        port = 6000 + i
        name = "ovn-" + str(port)
        mac_num = i
        dev = "tap" + str(i)
        qcow2_name = 'ubuntu-' + str(i) + '.qcow2'
        source_file = os.path.join(dirpath, qcow2_name)
        xmlname = name + '.xml'
        xmlpath = os.path.join(dirpath, xmlname)
        os.mkdir(dirpath)
        txml = CreatXml(vm_uuid=vm_uuid,
                        vm_source_file=source_file,
                        vnc_port=port,
                        vm_mac_num=mac_num,
                        vm_name=name,
                        vm_dev=dev)

        txml.genxml()
        txml.writexml(xmlpath)
        base_qcow2 = dirroot + '/ubuntu-16.04.6.qcow2'
        cmd = ['qemu-img', 'create', '-b', base_qcow2, '-fqcow2', source_file]
        re = run_command(cmd, check_exit_code=False)
        print(re)
        cmd = ['virsh', 'create', xmlpath]
        re = run_command(cmd, check_exit_code=False)
        print(re)


if __name__ == '__main__':
    choices = {'start': start, 'clean': clean}
    parser = argparse.ArgumentParser()
    parser.parse_args()






