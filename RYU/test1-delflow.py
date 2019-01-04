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


class SimpleSwitch13(app_manager.RyuApp):
    # 指定openflow版本
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.switchDic = {"0x1741f4aa82eef": "192.168.125.47",
                          "0x148bd3d3ad316": "192.168.125.43"}

    def del_port(self, datapath, inport, outport):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(in_port=inport)
        actions = [parser.OFPActionOutput(outport)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath,
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
                                 match=match,
                                 instructions=inst)
        print mod
        req = datapath.send_msg(mod)
        print req
        pass

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        datapath_id = hex(datapath.id)
        print datapath_id
        if "192.168.125.47" == self.switchDic[datapath_id]:
            self.del_port(datapath, inport=11, outport=8)
            self.del_port(datapath, inport=8, outport=11)

        elif "192.168.125.43" == self.switchDic[datapath_id]:
            self.del_port(datapath, inport=36, outport=27)
            self.del_port(datapath, inport=27, outport=38)




