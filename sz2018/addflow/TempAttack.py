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

def delcomm(team_nu):
    host_ip = "192.168.0." + str(100 + team_nu)
    print "del-flows to team%s on %s" % (team_nu, host_ip)
    attck_ip = "10.121.21." + str(team_nu)
    all_point = "10.121.100.0/24"
    ofcmd="ip,nw_src="+attck_ip+",nw_dst="+all_point
    del_cmds ="ovs-ofctl del-flows br_unicom "+"\""+ofcmd+"\""
    print del_cmds
    #result=ssh(hostip,cmds)
    #print result

def addcomm(team_nu):
    host_ip = "192.168.0." + str(100 + team_nu)
    print "add-flow to team%s on %s" % (team_nu, host_ip)
    attck_ip = "10.121.21." + str(team_nu)
    all_point="10.121.100.0/24"

    ofcmd="ip,nw_src="+attck_ip+",nw_dst="+all_point+",priority=5,action=drop"
    add_cmds ="ovs-ofctl add-flow br_unicom "+"\""+ofcmd+"\""
    print add_cmds
    #result=ssh(host_ip,add_cmds)
    #print result

def main(argv):
    if argv == "1":
        print "begin add ..."
        for i in range(1,21):
                addcomm(team_nu=i)
                print "*" * 20
    elif argv == "0":
        print "begin del ..."
        for i in range(1,21):
                delcomm(team_nu=i)
                print "*" * 20


if __name__ == '__main__':
    starttime = time.time()
    main(sys.argv[1])
    endtime = time.time()
    print "---------------------"
    print "finish,using",str(endtime - starttime)
    print "you can using \"ovs-ofctl dump-flows\" to see ACL"

