import sys
import time
import os
import client.utils as utils
import capture


def start():
    try:
        while True:
            json_files = [x for x in os.listdir(capture.get_config()['address']) if x.count('.json') > 0]
            # it will cause a bug without sorting
            json_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
            pcap_files = [x for x in os.listdir(capture.get_config()['address']) if x.count('.pcap') > 0]
            pcap_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

            if len(json_files) > 2 or len(pcap_files) > 2:
                if len(pcap_files) > 2:
                    os.remove(f'{capture.get_config()["address"]}/{pcap_files.pop(0)}')

                if len(json_files) > 2:
                    try:
                        utils.send_to_server(f'{capture.get_config()["address"]}/{json_files[0]}')
                        os.remove(f'{capture.get_config()["address"]}/{json_files.pop(0)}')
                    except ConnectionRefusedError:
                        print('server not listening')
            else:
                time.sleep(10)
    except Exception as e:
        print(e)
        raise KeyboardInterrupt


if __name__ == '__main__':
    try:
        capture.start()
        start()
    except KeyboardInterrupt:
        time.sleep(1)
        utils.send_remaining_files(capture.get_config()["address"], 'wireshark')
        os.chdir(capture.get_config()["address"])
        for file in os.listdir():
            os.remove(file)
        exit(-2)
