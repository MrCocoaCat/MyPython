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


dirroot = '/root/liyubo/ovn-test2/build/'
base_qcow2 = dirroot + '/ubuntu-16.04.6.qcow2'


def clean(num):
    for i in range(1, 7):
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
    cmd = ['ip', 'netns', 'list']
    re = run_command(cmd, check_exit_code=False)
    for netns in re.split():
        cmd = ['ip', 'netns', 'del', netns]
        run_command(cmd, check_exit_code=False)

    cmd = ['ovs-vsctl', 'list-ports', 'br-int']
    run_command(cmd, check_exit_code=False)
    for port in re.split():
        cmd = ['ovs-vsctl', 'del-port', 'br-int', port]
        run_command(cmd, check_exit_code=False)


class Port(PortBase):
    def __init__(self, name, num=None,mac =None):
        PortBase.__init__(self, name=name, num=num, mac=mac)


def start(num):
    print("start %d" % num)
    for i in range(1, 7):
        dirname = "ovn-" + str(i)
        dirpath = os.path.join(dirroot, dirname)
        vm_uuid = uuid.uuid1()
        vnc_port = 6000 + i
        name = "ovn-" + str(vnc_port)
        p = Port(name="tap" + str(i), num=i)
        print(p.mac)
        print(p.name)
        print(p.num)
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
        cmd = ['ovs-vsctl', 'set', 'Interface', p.name, option]
        run_command(cmd, check_exit_code=False)


def net_test(num):
    nb = OvnNb()
    s1 = Switch("s1")
    s2 = Switch("s2")
    s3 = Switch("s3")
    nb.ls_adds([s1, s2, s3])

    dhcp1 = DHCP(cidr="10.0.1.0/24",
                 server_id='10.0.1.254',
                 server_mac='00:00:00:00:02:00',
                 router='10.0.1.254',
                 lease_time='3600',)
    dhcp2 = DHCP(cidr="10.0.2.0/24",
                 server_id='10.0.2.254',
                 server_mac='00:00:00:00:02:00',
                 router='10.0.2.254',
                 lease_time='3600', )
    dhcp3 = DHCP(cidr="10.0.3.0/24",
                 server_id='10.0.3.254',
                 server_mac='00:00:00:00:03:00',
                 router='10.0.3.254',
                 lease_time='3600', )
    for i in range(1, 3):
        temp_port = SwitchPort(name='p'+str(i),
                               ip='10.0.1.' + str(i))
        s1.lsp_add(temp_port)
        s1.ovn_nbctl_lsp_set_dhcpv4_options(temp_port, dhcp1)

    for i in range(3, 5):
        temp_port = SwitchPort(name='p' + str(i),
                               ip='10.0.2.' + str(i))
        s2.lsp_add(temp_port)
        s2.ovn_nbctl_lsp_set_dhcpv4_options(temp_port, dhcp2)

    for i in range(5, 7):
        temp_port = SwitchPort(name='p' + str(i),
                               ip='10.0.3.' + str(i))
        s3.lsp_add(temp_port)
        s3.ovn_nbctl_lsp_set_dhcpv4_options(temp_port, dhcp3)

    r1 = Router("r1")
    nb.lr_add(r1)
    r1_s1 = RoutePort(name="r1-s1",
                      ip="10.0.1.254/24")
    r1_s2 = RoutePort(name="r1-s2",
                      ip="10.0.2.254/24")
    r1_s3 = RoutePort(name='r1-s3',
                      ip="10.0.3.254/24")
    r1.add_ports([r1_s1, r1_s2, r1_s3])

    s1_r1 = SwitchPort(name="s1-r1",
                       type="router",
                       options={'router-port': 'r1-s1'}
                       )
    s1.lsp_add(s1_r1)
    s2_r1 = SwitchPort(name="s2-r1",
                       type="router",
                       options={'router-port': 'r1-s2'}
                       )
    s2.lsp_add(s2_r1)

    s3_r1 = SwitchPort(name='s3-r1',
                       type='router',
                       options={'router-port': 'r1-s3'},
                       )

    s3.lsp_add(s3_r1)
    s3_edge1 = SwitchPort(name='s3-edge1',
                          options={'router-port': 'edge1-s3'},
                          type='router')
    s3.lsp_add(s3_edge1)

    ##################
    edge1 = Router(name='edge1',
                   options={"chassis": '123'})

    nb.lr_add(edge1)
    edge1_s3 = RoutePort(name='edge1-s3',
                         ip='10.0.3.1/24')
    edge1_outside = RoutePort(name="edge1-outside",
                              ip="192.168.125.201/24")
    edge1.add_ports([edge1_s3, edge1_outside])

    edge1.add_route(prefix="10.0.0.0/16",
                       nexthop="10.0.3.254")
    edge1.add_route(prefix="0.0.0.0/0",
                       nexthop="192.168.125.254")
    edge1.add_nat(nat_type="snat",
                     external_ip="192.168.125.201",
                     logical_ip="10.0.0.0/16")

    r1.add_route(prefix="0.0.0.0/0",
                    nexthop="10.0.3.1")

    outside = Switch(name="outside")
    nb.ls_add(outside)
    outside_edge1 = SwitchPort(name="outside-edge1",
                               type="router",
                               options={"router-port": "edge1-outside"})

    outside_localnet = SwitchPort(name="outside-localnet",
                                  mac="unknown",
                                  type="localnet",
                                  options={"network_name": "dataNet"})
    outside.ls_add_ports([outside_edge1, outside_localnet])


def net(num):
    print(num)


if __name__ == '__main__':
    choices = {'s': start, 'c': clean, 'n': net}
    parser = argparse.ArgumentParser()
    parser.add_argument("do", help="define what to do")
    parser.add_argument("-n", type=int, help="number", default=5)
    args = parser.parse_args()
    function = choices[args.do]
    function(args.n+1)





