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
        cmd = ['ovs-vsctl', 'set', 'Interface', p.name, option]
        run_command(cmd, check_exit_code=False)


def start_netns(num):
    cmdlist = []
    for i in range(1, num):
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
        cmdlist.append(cmd)
        #cmd = "ip netns exec vm1 ping 10.0.0.2"
        #cmdlist.append(cmd)

    for cmd in cmdlist:
        print(cmd)
        #re = os.popen(cmd)
        #print(re)

    #cmd = ['ip', 'netns', 'exec', 'vm1', 'ping', '-c', '5', '10.0.0.3']
    # print(cmd)
    #re = run_command(cmd, check_exit_code=False)
    #print(re)


def net(num):
    nb = OvnNb()
    nb.ls_add('s1')
    dhcp_option = nb.create_DHCP_Options(cidr="10.0.0.0/24")
    nb.dhcp_option_set_options(dhcp_option=dhcp_option,
                               server_id=1,
                               server_mac='00:00:00:00:02:00',
                               router='10.0.0.254',
                               lease_time='3600')
    for i in range(1, num):
        temp_port = port(i, name='p'+str(i))
        nb.lsp_add('s1', temp_port.name)
        ip = '10.0.0.' + str(i)
        nb.lsp_set_addresses(temp_port.name, temp_port.mac, ip)
        nb.lsp_set_port_security(temp_port.name, temp_port.mac, ip)
        nb.ovn_nbctl_lsp_set_dhcpv4_options(temp_port.name, dhcp_option)


if __name__ == '__main__':
    choices = {'s': start, 'c': clean, 'n': net, 'sn': start_netns}
    parser = argparse.ArgumentParser()
    parser.add_argument("do", help="define what to do")
    parser.add_argument("-n", type=int, help="number", default=2)
    args = parser.parse_args()
    #print(args.do)
    #print(args.n)
    function = choices[args.do]
    function(args.n+1)





