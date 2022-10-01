import os
import socket

import yaml


def get_config():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as f:
        config = yaml.safe_load(f)
        return config['server']['downloads_address'], config['server']['address'], config['server']['port']


def receive_logs():
    downloads_address, address, port = get_config()
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((address, port))
        server_socket.listen(5)
        print('Server is listening on port', port)
        while True:
            client_socket, client_address = server_socket.accept()
            print('Connection from', client_address)
            file_name = client_socket.recv(1024).decode('utf-8')
            print(file_name, 'sdasdasdssssssssssssss')
            if 'sysmon' in file_name:
                saving_location = f'{downloads_address}/Sysmon/{file_name}'
            elif 'wireshark' in file_name:
                saving_location = f'{downloads_address}/Wireshark/{file_name}'
            else:
                saving_location = file_name

            print(saving_location, 'asdsadasda')
            with open(saving_location, 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            client_socket.close()
            print('File received')
    except KeyboardInterrupt:
        print('Server closed')
        os.chdir(f'{downloads_address}/Sysmon')
        for file in os.listdir():
            os.remove(file)
        os.chdir(f'{downloads_address}/Wireshark')
        for file in os.listdir():
            os.remove(file)
        exit(-1)


def filter_logs():
    pass


def process_logs():
    pass


receive_logs()