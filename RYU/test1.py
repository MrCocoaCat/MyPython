# -*- coding: utf-8 -*-
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
import ryu.app
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

# 继承ryu.base.app_manager.RyuApp
class SimpleSwitch13(app_manager.RyuApp):
    # 指定openflow版本
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath
        print "datapath: %x " % datapath.id
        ofproto = datapath.ofproto
        print ofproto
        parser = datapath.ofproto_parser

        match1 = parser.OFPMatch(in_port=12, eth_dst='0025-9095-dcff')
        actions1 = [parser.OFPActionOutput(11)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions1)]

        mod1 = parser.OFPFlowMod(datapath,
                                 cookie=0,
                                 cookie_mask=0,
                                 table_id=0,
                                 command=ofproto.OFPFC_DELETE,
                                 idle_timeout=0,
                                 hard_timeout=0,
                                 priority=1,
                                 buffer_id=ofproto.OFP_NO_BUFFER,
                                 out_port=ofproto.OFPP_ANY,
                                 out_group=ofproto.OFPG_ANY,
                                 flags=0,
                                 match=match1,
                                 instructions=inst)
        print mod1
        req = datapath.send_msg(mod1)
        print req

        match2 = parser.OFPMatch(in_port=11, eth_dst='0025-9095-dcfb')
        actions2 = [parser.OFPActionOutput(12)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions2)]

        mod2 = parser.OFPFlowMod(datapath,
                                 cookie=0,
                                 cookie_mask=0,
                                 table_id=0,
                                 command=ofproto.OFPFC_DELETE,
                                 idle_timeout=0,
                                 hard_timeout=0,
                                 priority=1,
                                 buffer_id=ofproto.OFP_NO_BUFFER,
                                 out_port=ofproto.OFPP_ANY,
                                 out_group=ofproto.OFPG_ANY,
                                 flags=0,
                                 match=match2,
                                 instructions=inst)
        print mod2
        req = datapath.send_msg(mod2)
        print req

