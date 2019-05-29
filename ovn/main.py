# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 17:17
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : main.py

from kvm.createxml import CreatXml
from tool import run_command

from Ovn.ovn import *
import uuid
import os
import argparse


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
    cmd = ['ip', 'netns', 'list']
    re = run_command(cmd, check_exit_code=False)
    for netns in re.split():
        cmd = ['ip', 'netns', 'del', netns]
        run_command(cmd, check_exit_code=False)

    cmd = ['ovs-vsctl', 'list-ports', 'br-int']
    re = run_command(cmd, check_exit_code=False)
    for port in re.split():
        cmd = ['ovs-vsctl', 'del-port', 'br-int', port]
        re = run_command(cmd, check_exit_code=False)


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


def start_netns(num):
    cmdlist = []
    for i in range(1, num):
        p =SwitchPort(num)
        p = port(i)
        cmd = "ip netns add vm%s" % i
        cmdlist.append(cmd)

        cmd = "ovs-vsctl add-port br-int %s -- set interface %s type=internal" % (p.name, p.name)
        cmdlist.append(cmd)

        cmd = "ip link set %s address  %s" % (p.name, p.mac)
        cmdlist.append(cmd)

        cmd = "ip link set %s netns vm%s" % (p.name, i)
        cmdlist.append(cmd)

        #ip = "10.0.0."+str(i)
        #cmd = "ip netns exec vm%s ip addr add local %s/24 dev %s " % (i, ip, p.name)
        #cmdlist.append(cmd)

        cmd = "ip netns exec vm%s ip link set %s up" % (i, p.name)
        cmdlist.append(cmd)

        cmd = "ovs-vsctl set Interface %s external_ids:iface-id=p%s" % (p.name, i)
        cmdlist.append(cmd)

        cmd = "ip netns exec vm%s dhclient %s" % (i, p.name)
        cmdlist.append(cmd)

        cmd = "ip netns exec vm%s ip addr show %s" % (i, p.name)
        #re = os.popen(cmd)
        #print(re)
        #cmd = "ip netns exec vm1 ping 10.0.0.2"
        #cmdlist.append(cmd)

    for cmd in cmdlist:
        print(cmd)
        os.system(cmd)


    #cmd = ['ip', 'netns', 'exec', 'vm1', 'ping', '-c', '5', '10.0.0.3']
    # print(cmd)
    #re = run_command(cmd, check_exit_code=False)
    #print(re)


def net(num):
    nb = OvnNb()
    s1 = Switch("s1")
    s2 = Switch("s2")
    s3 = Switch("s3")
    nb.ls_add(s1)
    nb.ls_add(s2)
    nb.ls_add(s3)

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
    r1.lr_add_ports([r1_s1, r1_s2, r1_s3])

    s1_r1 = SwitchPort(name="s1-r1",
                       type="router",
                       mac="router",
                       options={'router-port': 'r1-s1'}
                       )
    s1.lsp_add(s1_r1)
    s2_r1 = SwitchPort(name="s2-r1",
                       type="router",
                       mac="router",
                       options={'router-port': 'r1-s2'}
                       )
    s2.lsp_add(s2_r1)

    s3_r1 = SwitchPort(name='s3-r1',
                       type='router',
                       mac='router',
                       options={'router-port': 'r1-s3'},
                       )

    s3.lsp_add(s3_r1)
    s3_edge1 = SwitchPort(name='s3-edge1',
                          options={'router-port': 'edge1-s3'},
                          type='router',
                          mac='router')
    s3.lsp_add(s3_edge1)

    ##################
    edge1 = Router(name='edge1')
                   #options={"chassis":'123'})

    nb.lr_add(edge1)
    edge1_s3 = RoutePort(name='edge1-s3',
                         ip='10.0.3.1/24')
    edge1.lrp_add(edge1_s3)
    #


if __name__ == '__main__':
    choices = {'s': start, 'c': clean, 'n': net, 'sn': start_netns}
    parser = argparse.ArgumentParser()
    parser.add_argument("do", help="define what to do")
    parser.add_argument("-n", type=int, help="number", default=5)
    args = parser.parse_args()
    function = choices[args.do]
    function(args.n+1)





