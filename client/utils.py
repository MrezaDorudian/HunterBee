import os
import socket
import yaml


def send_to_server(file_address):
    file_name = file_address.split('/')[-1]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(get_server_info())
    # enlarge the file name size to 1024
    file_name = file_name.ljust(1024)
    client.send(file_name.encode('utf-8'))
    with open(file_address, 'rb') as f:
        client.sendall(f.read())
    client.close()


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

    json_files = [x for x in os.listdir(folder_address) if x.count('.json') > 0]
    for file in json_files:
        try:
            send_to_server(f'{folder_address}/{file}')
            os.remove(file)
        except ConnectionRefusedError:
            print('server not listening')

    pass


def get_server_info():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        return config['server']['address'], config['server']['port']
