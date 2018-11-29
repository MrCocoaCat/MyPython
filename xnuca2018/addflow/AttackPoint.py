# -*- coding: utf-8 -*-

import os
import sys
import paramiko
import time
def ssh(sys_ip,cmds):
    """
    :param sys_ip:执行命令的服务器IP
    :param cmds: 执行的命令
    :return: 执行命令结果
    """

    # 创建ssh客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=sys_ip, username="root")
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmds)
    # 获取命令执行结果,返回的数据是一个list
    # print "doing cmd ",cmds
    result = stdout.readlines()
    ssh.close()
    return result

def attack_to_point(teamnu):
    pass

def point_to_attack(teamnu):
    print teamnu
    hostIP = "192.168.0." + str(100 + teamnu)
    attack_ip = "10.121.21." + str(teamnu)
    for i in range(5):
        point_ip = "10.121.100"+str(teamnu)+str(i)
        ofcmd="ip,nw_src="+point_ip+",nw_dst="+attack_ip+",priority=2,action=drop"
        cmds ="ovs-ofctl add-flow br_unicom "+"\""+ofcmd+"\""
        print cmds
        #result=ssh(hostip,cmds)
        #print result

def main(argv):
    print argv
    print argv==1
    if argv == "0":
        print "add Attack To point"
        for i in range(1,21):
                attack_to_point(teamnu=i)
                print "*" * 20
    elif argv == "1":
        print "Add Point to Attack"
        for i in range(1,21):
                point_to_attack(teamnu=i)
                print "*" * 20


if __name__ == '__main__':
    starttime = time.time()
    main(sys.argv[1])
    endtime = time.time()
    print "---------------------"
    print "using",str(endtime - starttime)
    print "==================== "
