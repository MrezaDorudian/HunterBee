import json
import subprocess

import pyshark
from client.utils import *
from client import constants
import threading


class Capturer:
    def __init__(self):
        self.folder_address = None
        self.interface = None
        self.packet_count = None
        self.load_config()
        pass

    def __str__(self):
        return f'Capturer Object\ninterface: {self.interface}, packet_count: {self.packet_count}'

    def load_config(self):
        self.folder_address = load_config()['address']
        self.interface = load_config()['interface']
        self.packet_count = load_config()['packet_count']

    @staticmethod
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
            f.seek(0)
            f.truncate()
            json.dump(packet_data, f, indent=4)

    def start(self):
        file_id = 0
        while True:
            try:
                capture = pyshark.LiveCapture(interface=self.interface,
                                              output_file=f'{self.folder_address}/wireshark-logs-{file_id}.pcap')
                capture.sniff(packet_count=self.packet_count)
                subprocess.run(
                    f'tshark -r {self.folder_address}/wireshark-logs-{file_id}.pcap -T json > '
                    f'{self.folder_address}/wireshark-logs-{file_id}.json',
                    shell=True)
                self.reformat_json(f'{self.folder_address}/wireshark-logs-{file_id}.json')
                file_id += 1
                capture.close()
            except Exception:
                return


class Wireshark:
    def __init__(self):
        self.folder_address = None
        self.load_config()

    def __str__(self):
        return f'Wireshark Object'

    def load_config(self):
        self.folder_address = load_config()['address']

    def start(self):
        try:
            while True:
                pcap_files = get_file_list(self.folder_address, 'pcap')
                json_files = get_file_list(self.folder_address, 'json')

                if len(json_files) > constants.SENDING_DELAY or len(pcap_files) > constants.SENDING_DELAY:
                    if len(pcap_files) > constants.SENDING_DELAY:
                        os.remove(f'{self.folder_address}/{pcap_files.pop(0)}')

                    if len(json_files) > constants.SENDING_DELAY:
                        error = send_to_server(f'{self.folder_address}/{json_files[0]}')
                        if not error:
                            os.remove(f'{self.folder_address}/{json_files.pop(0)}')
        except KeyboardInterrupt:
            return


def handle_exit(folder_address):
    send_remaining_files(folder_address, 'wireshark')
    os.chdir(folder_address)
    for file in os.listdir():
        os.remove(file)
    return


def load_config():
    with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
        config = yaml.safe_load(file)
        return {'interface': config['wireshark']['interface'],
                'packet_count': config['wireshark']['packet_count'],
                'address': config['wireshark']['address']}


def start():
    capturer = Capturer()
    wireshark = Wireshark()
    wireshark_thread = threading.Thread(target=wireshark.start)
    wireshark_thread.daemon = True
    try:
        wireshark_thread.start()
        capturer.start()
    except KeyboardInterrupt:
        handle_exit(wireshark.folder_address)
