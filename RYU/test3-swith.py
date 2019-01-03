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
                          "0x148bd3d3ad316": "192.168.125.43"}

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
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=priority,
                                match=match,
                                command=ofproto.OFPFC_DELETE,
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
            match1 = parser.OFPMatch(in_port=9)
            actions1 = [parser.OFPActionOutput(11)]
            #self.add_flow(datapath, 1, match1, actions1)
            self.del_flow(datapath, 1, match1, actions1)
            match2 = parser.OFPMatch(in_port=11)
            actions2 = [parser.OFPActionOutput(9)]
            #self.add_flow(datapath, 1, match2, actions2)
            self.del_flow(datapath, 1, match2, actions2)
            match3 = parser.OFPMatch(in_port=10)
            actions3 = [parser.OFPActionOutput(12)]
            #self.add_flow(datapath, 1, match3, actions3)
            self.del_flow(datapath, 1, match3, actions3)
            match4 = parser.OFPMatch(in_port=12)
            actions4 = [parser.OFPActionOutput(10)]
            #self.add_flow(datapath, 1, match4, actions4)
            self.del_flow(datapath, 1, match4, actions4)

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

