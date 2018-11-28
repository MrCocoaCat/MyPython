# -*- coding:utf-8 -*-
import os
import paramiko

def ssh(sys_ip,cmds):
    #创建ssh客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=sys_ip, username="root")
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmds)
    #获取命令执行结果,返回的数据是一个list
    #print "doing cmd ",cmds
    result = stdout.readlines()
    ssh.close()
    return result

def gencomm(hostip,iphead):
    print hostip
    for i in range(1,6):
            for j in range(i,6):
                    src=iphead+str(i)
                    dest=iphead+str(j)
                    ofcmd="ip,nw_src="+src+",nw_dst="+dest+",priority=2,action=drop"
                    cmds ="ovs-ofctl add-flow br_unicom "+"\""+ofcmd+"\""
                    #print cmds
                    result=ssh(hostip,cmds)
                    print result

if __name__ == '__main__':
    for i in range(1,21):
            ip="10.121.100."+str(i)
            hostip="192.168.0."+str(100+i)
            gencomm(hostip=hostip,iphead=ip)
            print "*" * 20


			
