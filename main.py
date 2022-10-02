import socket
import requests

json_data = {
    "0": {
        "frame": {
            "frame.interface_id": "0",
            "frame.interface_id_tree": {
                "frame.interface_name": "\\Device\\NPF_{E8268623-F789-4D5A-B92C-F0F4E5669F31}",
                "frame.interface_description": "Wi-Fi"
            },
            "frame.encap_type": "1",
            "frame.time": "Sep 27, 2022 17:59:48.436295000 Iran Standard Time",
            "frame.offset_shift": "0.000000000",
            "frame.time_epoch": "1664288988.436295000",
            "frame.time_delta": "0.000000000",
            "frame.time_delta_displayed": "0.000000000",
            "frame.time_relative": "0.000000000",
            "frame.number": "1",
            "frame.len": "60",
            "frame.cap_len": "60",
            "frame.marked": "0",
            "frame.ignored": "0",
            "frame.protocols": "eth:ethertype:ip:tcp"
        },
        "eth": {
            "eth.dst": "10:fe:ed:20:e5:7c",
            "eth.dst_tree": {
                "eth.dst_resolved": "Tp-LinkT_20:e5:7c",
                "eth.dst.oui": "1113837",
                "eth.dst.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.addr": "10:fe:ed:20:e5:7c",
                "eth.addr_resolved": "Tp-LinkT_20:e5:7c",
                "eth.addr.oui": "1113837",
                "eth.addr.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.dst.lg": "0",
                "eth.lg": "0",
                "eth.dst.ig": "0",
                "eth.ig": "0"
            },
            "eth.src": "34:e8:94:69:23:19",
            "eth.src_tree": {
                "eth.src_resolved": "Tp-LinkT_69:23:19",
                "eth.src.oui": "3467412",
                "eth.src.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.addr": "34:e8:94:69:23:19",
                "eth.addr_resolved": "Tp-LinkT_69:23:19",
                "eth.addr.oui": "3467412",
                "eth.addr.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.src.lg": "0",
                "eth.lg": "0",
                "eth.src.ig": "0",
                "eth.ig": "0"
            },
            "eth.type": "0x0800",
            "eth.padding": "00:00:00:00:00:00"
        },
        "ip": {
            "ip.version": "4",
            "ip.hdr_len": "20",
            "ip.dsfield": "0x00",
            "ip.dsfield_tree": {
                "ip.dsfield.dscp": "0",
                "ip.dsfield.ecn": "0"
            },
            "ip.len": "40",
            "ip.id": "0x0000",
            "ip.flags": "0x40",
            "ip.flags_tree": {
                "ip.flags.rb": "0",
                "ip.flags.df": "1",
                "ip.flags.mf": "0"
            },
            "ip.frag_offset": "0",
            "ip.ttl": "38",
            "ip.proto": "6",
            "ip.checksum": "0x955f",
            "ip.checksum.status": "2",
            "ip.src": "89.187.163.167",
            "ip.addr": "192.168.1.102",
            "ip.src_host": "89.187.163.167",
            "ip.host": "192.168.1.102",
            "ip.dst": "192.168.1.102",
            "ip.dst_host": "192.168.1.102"
        },
        "tcp": {
            "tcp.srcport": "9002",
            "tcp.dstport": "51565",
            "tcp.port": "51565",
            "tcp.stream": "0",
            "tcp.completeness": "0",
            "tcp.len": "0",
            "tcp.seq": "1",
            "tcp.seq_raw": "2869490873",
            "tcp.nxtseq": "1",
            "tcp.ack": "1",
            "tcp.ack_raw": "2189379319",
            "tcp.hdr_len": "20",
            "tcp.flags": "0x0010",
            "tcp.flags_tree": {
                "tcp.flags.res": "0",
                "tcp.flags.ns": "0",
                "tcp.flags.cwr": "0",
                "tcp.flags.ecn": "0",
                "tcp.flags.urg": "0",
                "tcp.flags.ack": "1",
                "tcp.flags.push": "0",
                "tcp.flags.reset": "0",
                "tcp.flags.syn": "0",
                "tcp.flags.fin": "0",
                "tcp.flags.str": "\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7A\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7"
            },
            "tcp.window_size_value": "501",
            "tcp.window_size": "501",
            "tcp.window_size_scalefactor": "-1",
            "tcp.checksum": "0x989d",
            "tcp.checksum.status": "2",
            "tcp.urgent_pointer": "0",
            "Timestamps": {
                "tcp.time_relative": "0.000000000",
                "tcp.time_delta": "0.000000000"
            }
        }
    },
    "1": {
        "frame": {
            "frame.interface_id": "0",
            "frame.interface_id_tree": {
                "frame.interface_name": "\\Device\\NPF_{E8268623-F789-4D5A-B92C-F0F4E5669F31}",
                "frame.interface_description": "Wi-Fi"
            },
            "frame.encap_type": "1",
            "frame.time": "Sep 27, 2022 17:59:48.463791000 Iran Standard Time",
            "frame.offset_shift": "0.000000000",
            "frame.time_epoch": "1664288988.463791000",
            "frame.time_delta": "0.027496000",
            "frame.time_delta_displayed": "0.027496000",
            "frame.time_relative": "0.027496000",
            "frame.number": "2",
            "frame.len": "60",
            "frame.cap_len": "60",
            "frame.marked": "0",
            "frame.ignored": "0",
            "frame.protocols": "eth:ethertype:ip:tcp"
        },
        "eth": {
            "eth.dst": "10:fe:ed:20:e5:7c",
            "eth.dst_tree": {
                "eth.dst_resolved": "Tp-LinkT_20:e5:7c",
                "eth.dst.oui": "1113837",
                "eth.dst.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.addr": "10:fe:ed:20:e5:7c",
                "eth.addr_resolved": "Tp-LinkT_20:e5:7c",
                "eth.addr.oui": "1113837",
                "eth.addr.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.dst.lg": "0",
                "eth.lg": "0",
                "eth.dst.ig": "0",
                "eth.ig": "0"
            },
            "eth.src": "34:e8:94:69:23:19",
            "eth.src_tree": {
                "eth.src_resolved": "Tp-LinkT_69:23:19",
                "eth.src.oui": "3467412",
                "eth.src.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.addr": "34:e8:94:69:23:19",
                "eth.addr_resolved": "Tp-LinkT_69:23:19",
                "eth.addr.oui": "3467412",
                "eth.addr.oui_resolved": "Tp-Link Technologies Co.,Ltd.",
                "eth.src.lg": "0",
                "eth.lg": "0",
                "eth.src.ig": "0",
                "eth.ig": "0"
            },
            "eth.type": "0x0800",
            "eth.padding": "00:00:00:00:00:00"
        },
        "ip": {
            "ip.version": "4",
            "ip.hdr_len": "20",
            "ip.dsfield": "0x00",
            "ip.dsfield_tree": {
                "ip.dsfield.dscp": "0",
                "ip.dsfield.ecn": "0"
            },
            "ip.len": "40",
            "ip.id": "0x0a84",
            "ip.flags": "0x40",
            "ip.flags_tree": {
                "ip.flags.rb": "0",
                "ip.flags.df": "1",
                "ip.flags.mf": "0"
            },
            "ip.frag_offset": "0",
            "ip.ttl": "39",
            "ip.proto": "6",
            "ip.checksum": "0x89db",
            "ip.checksum.status": "2",
            "ip.src": "89.187.163.167",
            "ip.addr": "192.168.1.102",
            "ip.src_host": "89.187.163.167",
            "ip.host": "192.168.1.102",
            "ip.dst": "192.168.1.102",
            "ip.dst_host": "192.168.1.102"
        },
        "tcp": {
            "tcp.srcport": "9002",
            "tcp.dstport": "51561",
            "tcp.port": "51561",
            "tcp.stream": "1",
            "tcp.completeness": "0",
            "tcp.len": "0",
            "tcp.seq": "1",
            "tcp.seq_raw": "2538231225",
            "tcp.nxtseq": "1",
            "tcp.ack": "1",
            "tcp.ack_raw": "3782061778",
            "tcp.hdr_len": "20",
            "tcp.flags": "0x0010",
            "tcp.flags_tree": {
                "tcp.flags.res": "0",
                "tcp.flags.ns": "0",
                "tcp.flags.cwr": "0",
                "tcp.flags.ecn": "0",
                "tcp.flags.urg": "0",
                "tcp.flags.ack": "1",
                "tcp.flags.push": "0",
                "tcp.flags.reset": "0",
                "tcp.flags.syn": "0",
                "tcp.flags.fin": "0",
                "tcp.flags.str": "\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7A\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7\u00c2\u00b7"
            },
            "tcp.window_size_value": "501",
            "tcp.window_size": "501",
            "tcp.window_size_scalefactor": "-1",
            "tcp.checksum": "0x8496",
            "tcp.checksum.status": "2",
            "tcp.urgent_pointer": "0",
            "Timestamps": {
                "tcp.time_relative": "0.000000000",
                "tcp.time_delta": "0.000000000"
            }
        }
    }
}





message_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message_server.connect(('localhost', 6666))

# +msg|streamName1|sourceName1|this is log message\0


msg_1 = f'+msg|stream_1|source_1|wireshark stuff\0'
msg_2 = f'+msg|stream_2|source_2|sysmon stuff\0'

message_server.send(msg_1.encode('utf-8'))
message_server.send(msg_2.encode('utf-8'))
message_server.close()