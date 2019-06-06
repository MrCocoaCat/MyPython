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

    cmd = "ovn-nbctl --all destroy Logical_Router"
    os.system(cmd)

    os.system("ovs-vsctl --if-exists del-br br9s0f0")


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
        dev_mac = logic_port.addresses.split()[0]
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
                 server_mac=generate_mac(),
                 router='10.0.1.254',
                 lease_time='3600', )
    ovn = OvnNb()
    os.system("ovs-vsctl add-br br9s0f0")
    os.system("ovs-vsctl add-port br9s0f0 enp9s0f0  ")
    os.system("ip addr add 10.127.0.130/24 dev  br9s0f0")
    os.system("ip link set  br9s0f0 up")

    for i in list(range(1, num))[::2]:
        print(i)
        # 交换机1
        s1 = Switch(name="s"+str(i), other_config="subnet=10.0.1.0/24")
        ovn.add_switch(s1)
        port_pr = SwitchPort(name="pr_peer"+str(i), type="router", addresses="router",
                             options={'router-port': "pr" + str(i)})
        port1 = SwitchPort(name="p"+str(i),   addresses=[generate_mac()+" 10.0.1.2/24"], dhcpv4_options=dhcp1)
        port2 = SwitchPort(name="p"+str(i+1), addresses=[generate_mac()+" 10.0.1.3/24"], dhcpv4_options=dhcp1)
        s1.add_ports([port_pr, port1, port2])
        domain(port1, i)
        domain(port2, i+1)
        # 路由器
        r1 = Router(name="r"+str(i),options={"chassis":"123"})
        ovn.add_router(r1)
        out = RoutePort(name="out"+str(i), mac=generate_mac(), network="10.127.0.10/24")
        port_p = RoutePort(name="pr" + str(i), mac=generate_mac(), network="10.0.1.254/24")

        r1.add_ports([port_p, out])
        # r1.add_route(RouterStaticRoute(ip_prefix="10.0.0.0/24", nexthop="10.0.0.254"))
        r1.add_nat(NAT(type='snat', external_ip='10.127.0.10', logical_ip='10.0.1.0/24'))
        #
        # # 交换机outside
        outside = Switch(name="outside")
        ovn.add_switch(outside)
        outside_localnet = SwitchPort(name="outside-localnet", type="localnet", addresses="unknown",
                                      options={'network_name': 'dataNet'})
        port = SwitchPort(name="out_peer" + str(i + 1), type="router", addresses="router",
                          options={'router-port': "out" + str(i)})
        outside.add_ports([port, outside_localnet])



if __name__ == '__main__':
    choices = {'c': clean, 's': start}
    parser = argparse.ArgumentParser()
    parser.add_argument("do", type=str, help="define what to do", default='s')
    parser.add_argument("-n", type=int, help="number", default=2)
    args = parser.parse_args()
    function = choices[args.do]
    function(args.n+1)






