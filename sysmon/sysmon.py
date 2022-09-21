import os
import subprocess
import time
import socket
import threading
import yaml

import logs

def check_installed():
    try:
        result = subprocess.run(['sysmon.exe'], capture_output=True, text=True)
        if 'System Monitor' in result.stdout:
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def check_version():
    if check_installed():
        result = subprocess.run(['sysmon.exe'], capture_output=True, text=True)
        version = result.stdout.split('\n')[1].split(' ')[2].strip()
        return version
    else:
        return 'Not installed'


def get_config():
    if check_installed():
        result = subprocess.run(['sysmon.exe', '-c'], capture_output=True, text=True)
        config = f'configuration{"".join(result.stdout.split("Rule configuration")[1:])}'
        print(config)


def set_config(file_address):
    if check_installed():
        subprocess.run(['sysmon.exe', '-c', file_address])
    else:
        print('Not installed')


def save_logs():
    if check_installed():
        while True:
            ndjson_folders = [x for x in os.listdir(logs.get_folder_address()) if x.count('.ndjson') > 0]
            json_folders = [x for x in os.listdir(logs.get_folder_address()) if x.count('.json') > 0]

            if len(ndjson_folders) > 1 or len(json_folders) > 1:
                if len(ndjson_folders) > 1:
                    file_id = ndjson_folders[0].split('.')[0].split('-')[-1]
                    logs.read_logs(ndjson_folders[0], file_id)
                    os.remove(f'{logs.get_folder_address()}/{ndjson_folders[0]}')

                if len(json_folders) > 1:
                    send_to_server(f'{logs.get_folder_address()}/{json_folders[0]}')
                    os.remove(f'{logs.get_folder_address()}/{json_folders[0]}')
            else:
                time.sleep(10)
    else:
        print('Not installed')


def send_to_server(file_address):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(get_server_info())
    #     send log files to server
    with open(file_address, 'rb') as f:
        client.send(f.read())
    os.remove(file_address)



def get_server_info():
    with open('../config.yaml') as file:
        config = yaml.safe_load(file)
        return config['server']['address'], config['server']['port']


save_logs()