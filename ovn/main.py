# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 17:17
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : main.py

from createxml import CreatXml
from tool import run_command
from tool import CmdException

from ovn import OvnNb
import uuid
import os
import argparse
from port import port

dirroot = '/root/liyubo/ovn-test2'
base_qcow2 = dirroot + '/ubuntu-16.04.6.qcow2'

logic_port = {}

def clean(num):
    for i in range(1, num):
        dirname = "ovn-" + str(i)
        dirpath = os.path.join(dirroot, dirname)
        vnc_port = 6000 + i
        name = "ovn-" + str(vnc_port)
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
        nb = OvnNb()
        nb.clean()


def start(num):
    print("start %d" % num)
    for i in range(1, num):
        dirname = "ovn-" + str(i)
        dirpath = os.path.join(dirroot, dirname)
        vm_uuid = uuid.uuid1()
        vnc_port = 6000 + i
        name = "ovn-" + str(vnc_port)
        p = port(i)
        qcow2_name = 'ubuntu-' + str(i) + '.qcow2'
        source_file = os.path.join(dirpath, qcow2_name)
        xmlname = name + '.xml'
        xmlpath = os.path.join(dirpath, xmlname)
        os.mkdir(dirpath)
        txml = CreatXml(vm_uuid=vm_uuid,
                        vm_source_file=source_file,
                        vnc_port=vnc_port,
                        vm_name=name,
                        vm_dev=p)
        txml.genxml()
        txml.writexml(xmlpath)
        cmd = ['qemu-img', 'create', '-b', base_qcow2, '-fqcow2', source_file]
        re = run_command(cmd, check_exit_code=False)
        print(re)
        cmd = ['virsh', 'create', xmlpath]
        re = run_command(cmd, check_exit_code=False)
        print(re)

        option = 'external_ids:iface-id=%s' % 'p'+str(i)
        cmd = ['ovs-vsctl', 'set', 'Interface', p.name, ]
        re = run_command(cmd, check_exit_code=False)


def net(num):
    nb = OvnNb()
    # try:
    #     nb.ls_add('s1')
    # except CmdException as e:
    #     print(e)

    print(nb.ls_dict)
    # for i in range(1, num):
    #     temp_port = port(i, name='p'+str(i))
    #     nb.lsp_add('s1', temp_port.name)
    #     nb.lsp_set_addresses(temp_port.name, temp_port.mac)
    #     nb.lsp_set_port_security(temp_port.name, temp_port.mac)


if __name__ == '__main__':
    choices = {'s': start, 'c': clean, 'n': net}
    parser = argparse.ArgumentParser()
    parser.add_argument("do", help="define what to do")
    parser.add_argument("-n", type=int, help="number",default=5)
    args = parser.parse_args()
    #print(args.do)
    #print(args.n)
    function = choices[args.do]
    function(args.n+1)





