# -*- coding: utf-8 -*-
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import ryu.app.ofctl.api

# 继承ryu.base.app_manager.RyuApp
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.num = 0
        self.switchDic = {"0x1741f4aa82eef": "192.168.125.47",
                          "0x148bd3d3ad316": "192.168.125.43",
                          "0x148bd3d3abf96": "192.168.125.45"}

    def list_add_flow(self, add_list):
        for i in add_list:
            self.add_flow(i[0], i[1], i[2], i[3])

    def list_del_flow(self, add_list):
        for i in add_list:
            self.del_flow(i[0], i[1], i[2], i[3])

    def add_flow(self, datapath, priority, match, actions):
        print "begin add flow ..."
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=priority,
                                match=match,
                                instructions=inst)
        datapath.send_msg(mod)

    def del_flow(self, datapath, priority, match, actions):
        print "begin del flow ..."
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath,
                                cookie=0,
                                cookie_mask=0,
                                table_id=0,
                                command=ofproto.OFPFC_DELETE,
                                idle_timeout=0,
                                hard_timeout=0,
                                priority=priority,
                                buffer_id=ofproto.OFP_NO_BUFFER,
                                out_port=ofproto.OFPP_ANY,
                                out_group=ofproto.OFPG_ANY,
                                flags=0,
                                match=match,
                                instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        datapath_id = hex(datapath.id)
        print "datapath id :%x switch IP:%s" % (datapath.id, self.switchDic[datapath_id])
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        if datapath_id == "0x1741f4aa82eef":
            #47
            match1 = parser.OFPMatch(in_port=8)
            actions1 = [parser.OFPActionOutput(9)]
            match2 = parser.OFPMatch(in_port=9)
            actions2 = [parser.OFPActionOutput(8)]
            flow_list1 = []
            flow_list1.append((datapath, 5, match1, actions1))
            flow_list1.append((datapath, 5, match2, actions2))
            self.list_add_flow(flow_list1)
            #self.list_del_flow(flow_list1)
        elif datapath_id == "0x148bd3d3ad316":
            # 43
            match1 = parser.OFPMatch(in_port=29)
            actions1 = [parser.OFPActionOutput(36)]
            match2 = parser.OFPMatch(in_port=36)
            actions2 = [parser.OFPActionOutput(29)]
            flow_list1 = []
            flow_list1.append((datapath, 5, match1, actions1))
            flow_list1.append((datapath, 5, match2, actions2))
            self.list_add_flow(flow_list1)
           # self.list_del_flow(flow_list1)

    # pack-in
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        #print "ethertype is %x" % eth.ethertype
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            #print "ignore lldp packet"
            return
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.logger.info("packet in %x src:%s dst:%s in_port:%s ", dpid, src, dst, in_port)
        self.num += 1
        print "round num: %d" % self.num

