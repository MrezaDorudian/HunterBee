import pyshark
import os
import json
import yaml
# install wireshark & tshark and add tshark to environment variable


def capture_packets():
    config = get_config()
    capture = pyshark.LiveCapture(interface=config['interface'], output_file=config['pcap_address'])
    capture.sniff(packet_count=config['packet_count'])
    os.system(f'tshark -r {config["pcap_address"]} -T json > {config["json_address"]}')


def reformat_json():
    config = get_config()
    with open(config['json_address'], 'r+') as f:
        all_packets = json.load(f)
        packet_data = {}
        for index, packet in enumerate(all_packets):
            layers = packet['_source']['layers']
            layer_data = {}
            for layer in layers:
                layer_data[layer] = layers[layer]
            packet_data[index] = layer_data
        # delete file content
        f.seek(0)
        f.truncate()
        json.dump(packet_data, f, indent=4)


def run():
    capture_packets()
    reformat_json()

def get_config():
    with open('../config.yaml') as file:
        config = yaml.safe_load(file)
        fields = {
            'interface': config['wireshark']['interface'],
            'packet_count': config['wireshark']['packet_count'],
            'pcap_address': config['wireshark']['pcap_address'],
            'json_address': config['wireshark']['json_address']
        }
        return fields



run()