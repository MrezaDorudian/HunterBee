import json
import os
import pyshark
import yaml
from multiprocessing import Process


def capture_packets():
    file_id = 0
    while True:
        config = get_config()
        capture = pyshark.LiveCapture(interface=config['interface'],
                                      output_file=f'{config["address"]}/wireshark-logs-{file_id}.pcap')
        try:
            capture.sniff(packet_count=config['packet_count'])
        except KeyboardInterrupt:
            capture.close()
        try:
            os.system(
                f'tshark -r {config["address"]}/wireshark-logs-{file_id}.pcap -T json > {config["address"]}/wireshark-logs-{file_id}.json')
        except Exception as e:
            print(e)
        reformat_json(f'{config["address"]}/wireshark-logs-{file_id}.json')
        file_id += 1


def reformat_json(file_address):
    with open(file_address, 'r+') as f:
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


def get_config():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        fields = {
            'interface': config['wireshark']['interface'],
            'packet_count': config['wireshark']['packet_count'],
            'address': config['wireshark']['address'],
        }
        return fields


def start():
    process = Process(target=capture_packets)
    process.start()
