# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 16:23



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

def delcomm(hostip,attckip):
    """
    :param hostip:执行命令的服务器IP
    :return:
    """
    print hostip
    dest="10.121.100.0/24"
    src=attckip
    delofcmd="ip,nw_src="+src+",nw_dst="+dest
    cmds ="ovs-ofctl del-flows br_unicom "+"\""+delofcmd+"\""
    print cmds
        #result=ssh(hostip,cmds)
        #print result

def addcomm(hostip,attckip):
    """
    :param hostip:执行命令的服务器IP
    :return:
    """
    print hostip
    dest="10.121.100.0/24"
    src=attckip
    addofcmd="ip,nw_src="+src+",nw_dst="+dest+",priority=5,action=drop"
    cmds ="ovs-ofctl add-flow br_unicom "+"\""+addofcmd+"\""
    print cmds
        #result=ssh(hostip,cmds)
        #print result

def main(argv):
    print argv
    print argv==1
    if argv == "1":
        print "add"
        for i in range(1,21):
                hostip="192.168.0."+str(100+i)
                attckip="10.121.21."+str(i)
                addcomm(hostip=hostip,attckip=attckip)
                print "*" * 20
    elif argv == "0":
        print "del"
        for i in range(1,21):
                ip="192.168.0."+str(100+i)
                attckip = "10.121.21." + str(i)
                delcomm(hostip=ip,attckip=attckip)
                print "*" * 20


if __name__ == '__main__':
    starttime = time.time()
    main(sys.argv[1])
    endtime = time.time()
    print "---------------------"
    print "using",str(endtime - starttime)
    print "==================== "
