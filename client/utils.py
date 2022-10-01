import os
import socket
import yaml
import client.constants as constants


def send_to_server(file_address):
    file_name = file_address.split('/')[-1]
    file_name = file_name.ljust(1024)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(get_server_info())
        client.sendall(file_name.encode('utf-8'))
        with open(file_address, 'rb') as f:
            client.sendall(f.read())
        client.close()
    except ConnectionRefusedError:
        return True


def send_remaining_files(folder_address, log_type):
    if log_type == 'sysmon':
        file_type = '.ndjson'
    elif log_type == 'wireshark':
        file_type = '.pcap'
    else:
        file_type = ''

    os.chdir(folder_address)
    for file in os.listdir():
        if file_type in file:
            os.remove(file)

    json_files = get_file_list(folder_address, 'json')
    for file in json_files:
        error = send_to_server(f'{folder_address}/{file}')
        if error:
            break
        else:
            os.remove(file)


def get_server_info():
    with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
        config = yaml.safe_load(file)
        return config['server']['address'], config['server']['port']


def get_file_list(folder_address, file_type):
    target_file_list = [x for x in os.listdir(folder_address) if x.count(f'.{file_type}') > 0]
    target_file_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    return target_file_list
