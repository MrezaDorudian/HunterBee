import os
import socket
import yaml
import constants


class Server:
    def __init__(self):
        self.address = None
        self.port = None
        self.downloads_address = None
        self.load_config()
        self.server_socket = None
        self.listen()
        pass

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS) as f:
            config = yaml.safe_load(f)
            self.address = config['server']['address']
            self.port = config['server']['port']
            self.downloads_address = config['server']['downloads_address']

    def handle_exit(self):
        print('Server closed')
        os.chdir(f'{self.downloads_address}/Sysmon')
        for file in os.listdir():
            os.remove(file)
        os.chdir(f'{self.downloads_address}/Wireshark')
        for file in os.listdir():
            os.remove(file)
        return

    def listen(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.address, self.port))
            self.server_socket.listen()
            print('Server is listening on port', self.port)
            while True:
                client_socket, client_address = self.server_socket.accept()
                file_name = client_socket.recv(1024).decode('utf-8')
                self.receive_logs(file_name, client_socket)
        except KeyboardInterrupt:
            self.handle_exit()

    def receive_logs(self, file_name, client_socket):
        if 'sysmon' in file_name:
            saving_location = f'{self.downloads_address}/Sysmon/{file_name}'
        elif 'wireshark' in file_name:
            saving_location = f'{self.downloads_address}/Wireshark/{file_name}'
        else:
            saving_location = file_name

        with open(saving_location, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)
            print('File received')
            client_socket.close()


def filter_logs():
    pass


def process_logs():
    pass


server = Server()
