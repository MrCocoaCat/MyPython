# -*- coding: utf-8 -*-
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
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

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Instruction 规定对符合match时，所进行的指令
        # OFPInstructionGotoTable
        # OFPInstructionWriteMetadata:寫入Metadata 以做為下一個table 所需的參考資料。
        # OFPInstructionActions:在目前的action set中寫入新的action，如果有相同的则覆盖
        # OFPInstructionMeter:指定該封包到所定義的meter table。
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        # APPLY_ACTIONS为立即为报文执行指令
        if buffer_id:
            # 消息类别为OFPFlowMod，instructions为指令
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
            # 发送至switch
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath
        print datapath
        ofproto = datapath.ofproto
        print ofproto
        parser = datapath.ofproto_parser

        out_port = 1
        in_port = 2
        actions = [parser.OFPActionOutput(out_port, ofproto.OFPCML_NO_BUFFER)]

        match = parser.OFPMatch(in_port=in_port)
        # verify if we have a valid buffer_id, if yes avoid to send both
        # flow_mod & packet_out
        self.add_flow(datapath, 1, match, actions)




