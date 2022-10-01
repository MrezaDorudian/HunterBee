import json
import multiprocessing
import pyshark
from urllib3.connectionpool import xrange

from client.utils import *
from client import constants
from multiprocessing import Process, Manager


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
                os.system(
                    f'tshark -r {self.folder_address}/wireshark-logs-{file_id}.pcap -T json > {self.folder_address}/wireshark-logs-{file_id}.json')
                self.reformat_json(f'{self.folder_address}/wireshark-logs-{file_id}.json')
                file_id += 1
                capture.close()
            except Exception:
                return


class Wireshark:
    def __init__(self):
        self.folder_address = None
        self.load_config()
        pass

    def __str__(self):
        return f'Wireshark Object'

    def load_config(self):
        self.folder_address = load_config()['address']

    def handle_exit(self):
        send_remaining_files(self.folder_address, 'wireshark')
        os.chdir(self.folder_address)
        for file in os.listdir():
            os.remove(file)
        return

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
            self.handle_exit()
            return


def load_config():
    with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
        config = yaml.safe_load(file)
        return {'interface': config['wireshark']['interface'],
                'packet_count': config['wireshark']['packet_count'],
                'address': config['wireshark']['address']}


if __name__ == '__main__':
    capturer = Capturer()
    wireshark = Wireshark()

    processes = []

    manager = Manager()

    p_1 = Process(target=capturer.start)
    p_1.start()
    p_2 = Process(target=wireshark.start)
    p_2.start()

    try:
        p_1.join()
        p_2.join()
    except KeyboardInterrupt:
        p_1.terminate()
        p_2.terminate()
        manager.shutdown()
        exit(-100)
