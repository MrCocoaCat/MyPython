# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 10:03
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : createxml.py

import xml.etree.ElementTree as ET
import os
import re


def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class createxml:
    def __init__(self, vm_uuid, source_file, vm_name, vnc_port,vm_mac_num, vm_dev):
        self._vm_uuid = str(vm_uuid)
        self._source_file = source_file
        self._vnc_port = str(vnc_port)
        self._vm_name = vm_name
        self._mac_num = vm_mac_num
        self._dev = vm_dev

        self._genmac()

    def _genmac(self):
        pattern = re.compile('.{2}')
        self._vm_mac = ':'.join(pattern.findall(str("%012x" % self._mac_num)))

    def genxml(self):
        self.root = ET.Element("domain")
        #创建self.root的子节点sub1，并添加属性
        name = ET.SubElement(self.root, "name")
        name.text =self._vm_name
        _uuid = ET.SubElement(self.root, "uuid")
        _uuid.text = self._vm_uuid

        memory = ET.SubElement(self.root, "memory")
        memory.text = "4388608"
        vcpu = ET.SubElement(self.root, "vcpu")
        vcpu.text = "2"
        os = ET.SubElement(self.root, "os")
        type = ET.SubElement(os, "type")
        type.attrib = {"arch": "x86_64", "machine": "pc"}
        boot = ET.SubElement(os, "boot")
        boot.attrib = {'dev': 'hd'}

        devices = ET.SubElement(self.root, "devices")

        emulator = ET.SubElement(devices, "emulator")
        emulator.text = "/usr/libexec/qemu-kvm"

        disk = ET.SubElement(devices, "disk")
        disk.attrib = {"type": 'file', "device": 'disk'}

        driver = ET.SubElement(disk, "driver")
        driver.attrib = {'name':'qemu' ,'type':'qcow2'}

        source = ET.SubElement(disk, "source")
        source.attrib={'file': self._source_file}

        target = ET.SubElement(disk, "target")
        target.attrib={'dev': 'hda', 'bus': 'ide'}

        interface = ET.SubElement(devices, "interface")
        interface.attrib={'type': 'bridge'}
        mac = ET.SubElement(interface, "mac")
        mac.attrib = {'address': self._vm_mac}
        source = ET.SubElement(interface, "source")
        source.attrib = {'bridge': 'br-int'}

        virtualport = ET.SubElement(interface, "virtualport")
        virtualport.attrib = {'type': 'openvswitch'}

        target = ET.SubElement(interface, "target")
        target.attrib = {'dev': self._dev }

        model = ET.SubElement(interface, "model")
        model.attrib = {'type': 'virtio'}

        graphics = ET.SubElement(devices, "graphics")
        graphics.attrib = {'type': 'vnc', 'port': self._vnc_port, 'autoport': 'no', 'listen':'0.0.0.0', 'keymap': 'en-us'}
        indent(self.root)

    def writexml(self, out_path):
        tree = ET.ElementTree(self.root)
        tree.write(out_path)

    def delxml(self,out_path):
        os.remove(out_path)
