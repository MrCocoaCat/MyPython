# -*- coding: utf-8 -*-

# 优先级3
# 添加攻击点无法访问本队得分点规则
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

def add_attack_to_point(team_nu):

    host_ip = "192.168.0." + str(100 + team_nu)
    print "doing add-flow to team%s on %s"%(team_nu,host_ip)
    attack_ip = "10.121.21." + str(team_nu)
    for i in range(1,6):
        point_ip = "10.121.100."+str(team_nu)+str(i)
        ofcmd="ip,nw_src="+attack_ip+",nw_dst="+point_ip+",priority=3,action=drop"
        cmds ="ovs-ofctl add-flow br_unicom "+"\""+ofcmd+"\""
        print cmds
        result=ssh(host_ip,cmds)
        print result

def del_attack_to_point(team_nu):

    host_ip = "192.168.0." + str(100 + team_nu)
    print "doing del-flows to team%s on %s"%(team_nu,host_ip)
    attack_ip = "10.121.21." + str(team_nu)
    for i in range(1,6):
        point_ip = "10.121.100."+str(team_nu)+str(i)
        ofcmd="ip,nw_src="+attack_ip+",nw_dst="+point_ip
        cmds ="ovs-ofctl del-flows br_unicom "+"\""+ofcmd+"\""
        print cmds
        result = ssh(host_ip, cmds)
        print result

def main(argv):
    if argv == "0":
        print "del Attack To point"
        for i in range(1,21):
                del_attack_to_point(team_nu=i)
                print "*" * 20
    elif argv == "1":
        print "Add Point to Attack"
        for i in range(1,21):
                add_attack_to_point(team_nu=i)
                print "*" * 20


if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv[1])
    end_time = time.time()
    print "---------------------"
    print "finish attack_to_point,using", str(end_time - start_time)
    print "you can using \"ovs-ofctl dump-flows\" to see ACL"
    print "==================== "
