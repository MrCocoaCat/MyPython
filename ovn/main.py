# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 17:17
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : main.py

from kvm.createxml import CreatXml

from Ovn.ovn import *
import uuid
import os
import argparse
import time
from tools.install_venv import run_command

dirroot = '/root/liyubo/ovn-test2/build/'
base_qcow2 = dirroot + '/ubuntu-16.04.6.qcow2'


# def clock(func):
#     def clocked(*args):
#         t0 = time.perf_counter()
#         result = func(*args)
#         elapsed = time.perf_counter() - t0
#         name = func.__name__
#         arg_str = ','.join(repr(arg) for arg in args)
#         print('[%0.8fs] %s (%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#     return clocked

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
    cmd = ['ip', 'netns', 'list']
    re = run_command(cmd, check_exit_code=False)
    for netns in re.split():
        cmd = ['ip', 'netns', 'del', netns]
        run_command(cmd, check_exit_code=False)

    cmd = "ovn-nbctl --all destroy Logical_Switch"
    os.system(cmd)
    cmd = "ovn-nbctl --all destroy DHCP_Options"
    os.system(cmd)
    # cmd = ['ovs-vsctl', 'list-ports', 'br-int']
    # run_command(cmd, check_exit_code=False)
    # for port in re.split():
    #     cmd = ['ovs-vsctl', 'del-port', 'br-int', port]
    #     run_command(cmd, check_exit_code=False)


def domain(logic_port, num):
        dirname = "ovn-" + str(num)
        dirpath = os.path.join(dirroot, dirname)
        vm_uuid = uuid.uuid1()
        vnc_port = 6000 + num
        name = "ovn-" + str(vnc_port)
        qcow2_name = 'ubuntu-' + str(num) + '.qcow2'
        source_file = os.path.join(dirpath, qcow2_name)
        xmlname = name + '.xml'
        xmlpath = os.path.join(dirpath, xmlname)
        os.mkdir(dirpath)
        dev_mac = logic_port.dynamic_addresses.split()[0]
        dev_name = logic_port.name+"_peer"
        txml = CreatXml(vm_uuid=vm_uuid,
                        vm_source_file=source_file,
                        vnc_port=vnc_port,
                        vm_name=name,
                        vm_dev_name=dev_name,
                        vm_dev_mac=dev_mac)
        txml.writexml(xmlpath)
        cmd = ['qemu-img', 'create', '-b', base_qcow2, '-fqcow2', source_file]
        re = run_command(cmd, check_exit_code=False)
        cmd = ['virsh', 'create', xmlpath]
        re = run_command(cmd, check_exit_code=False)
        print("create domian %s ,dev %s , %s" % (name, dev_name, dev_mac))

        option = 'external_ids:iface-id=%s' % logic_port.name
        cmd = ['ovs-vsctl', 'set', 'Interface', dev_name, option]
        run_command(cmd, check_exit_code=False)


def start(num):
    dhcp1 = DHCP(cidr="10.0.1.0/24",
                 server_id='10.0.1.254',
                 server_mac='00:00:00:00:02:00',
                 router='10.0.1.254',
                 lease_time='3600', )
    ovn = OvnNb()

    for i in list(range(1, num))[::2]:
        print(i)
        s1 = Switch(name="s"+str(i), other_config="subnet=10.0.1.0/24")
        ovn.add_switch(s1)
        port1 = SwitchPort(name="p"+str(i), addresses="dynamic", dhcpv4_options=dhcp1)
        port2 = SwitchPort(name="p"+str(i+1), addresses="dynamic", dhcpv4_options=dhcp1)
        s1.add_ports([port1, port2])
        domain(port1, i)
        domain(port2, i+1)


if __name__ == '__main__':
    choices = {'c': clean, 's': start}
    parser = argparse.ArgumentParser()
    parser.add_argument("do", help="define what to do", default='s')
    parser.add_argument("-n", type=int, help="number", default=5)
    args = parser.parse_args()
    function = choices[args.do]
    function(args.n+1)






