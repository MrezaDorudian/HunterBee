import os
import socket

import yaml

with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
    config = yaml.safe_load(file)
    downloads_address, address, port = config['server']['downloads_address'], config['server']['address'], \
                                       config['server']['port']

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(5)
    print('Server is listening on port', port)
    # save incoming files to the server folder
    while True:
        client_socket, client_address = server_socket.accept()
        print('Connection from', client_address)
        file_name = client_socket.recv(1024).decode('utf-8')
        if 'sysmon' in file_name:
            saving_location = f'downloads/Sysmon/{file_name}'
        elif 'wireshark' in file_name:
            saving_location = f'downloads/Wireshark/{file_name}'
        else:
            saving_location = file_name
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
