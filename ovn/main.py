# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 17:17
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : main.py
from createxml import createxml
import uuid

if __name__ == '__main__':
    i = 1
    uuid = uuid.uuid1()
    port = 6000+i
    name = "ovn-" + str(port)
    mac_num = i
    dev = "tap"+str(i)
    txml = createxml(vm_uuid=uuid,
                     source_file='/root/liyubo/ovn-test/ovn1/ubuntu-16.04.6.qcow2',
                     vnc_port=port,
                     vm_mac_num=mac_num,
                     vm_name=name,
                     vm_dev=dev)
    txml.delxml("./test01.xml")
    txml.genxml()
    #txml.writexml("./test01.xml")