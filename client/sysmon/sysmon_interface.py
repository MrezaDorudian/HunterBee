import json
import subprocess
import ndjson
from client.utils import *
from client.sysmon.winlogbeat.winlogbeat_interface import Winlogbeat
from client import constants


class Sysmon:
    def __init__(self):
        self.folder_address = None
        self.load_folder_address()
        self.basic_command = 'sysmon.exe'
        self.installed = self.check_installed()
        self.version = self.check_version()
        self.winlogbeat = Winlogbeat()

    def __str__(self):
        return f'Sysmon Object\ninstalled: {self.installed}, version: {self.version}'

    def check_installed(self):
        try:
            result = subprocess.run([self.basic_command], capture_output=True, text=True)
            if 'System Monitor' in result.stdout:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def check_version(self):
        if self.installed:
            result = subprocess.run([self.basic_command], capture_output=True, text=True)
            version = result.stdout.split('\n')[1].split(' ')[2].strip()
            return version
        else:
            return 'Not installed'

    def print_current_config(self):
        if self.installed:
            result = subprocess.run([self.basic_command, '-c'], capture_output=True, text=True)
            config = f'configuration{"".join(result.stdout.split("Rule configuration")[1:])}'
            print(config)

    def set_config(self, file_address):
        if self.installed:
            subprocess.run([self.basic_command, '-c', file_address])
        else:
            print('Not installed')

    def load_folder_address(self):
        with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
            config = yaml.safe_load(file)
            self.folder_address = config['sysmon']['address']

    def read_logs(self, file_name, file_id):
        output_data = {}
        iterator = 0
        with open(f'{self.folder_address}/{file_name}') as f:
            data = ndjson.load(f)
            for item in data:
                try:
                    for key in ['@metadata', 'event', 'log', 'ecs', 'agent', 'message']:
                        item.pop(key)
                    for key in ['user', 'process', 'record_id', 'api', 'opcode', 'event_id', 'version', 'channel']:
                        item['winlog'].pop(key)
                    for key in ['os', 'mac', 'id', 'hostname', 'architecture']:
                        item['host'].pop(key)
                except KeyError:
                    pass
                output_data[iterator] = item
                iterator += 1
        with open(f'{self.folder_address}/sysmon-logs-{file_id}.json', 'w') as f:
            json.dump(output_data, f, indent=4)

    def handle_exit(self):
        self.winlogbeat.utilities('stop')
        send_remaining_files(self.folder_address, 'sysmon')
        os.chdir(self.folder_address)
        for file in os.listdir():
            os.remove(file)
        return

    def start(self):
        if self.installed:
            self.winlogbeat.restart()
            while True:
                ndjson_files = get_file_list(self.folder_address, 'ndjson')
                json_files = get_file_list(self.folder_address, 'json')
                if len(ndjson_files) > constants.SENDING_DELAY or len(json_files) > constants.SENDING_DELAY:
                    if len(ndjson_files) > constants.SENDING_DELAY:
                        file_id = ndjson_files[0].split('.')[0].split('-')[-1]
                        if int(file_id) > 9999999:
                            file_id = '0'
                        self.read_logs(ndjson_files[0], file_id)
                        try:
                            os.remove(f'{self.folder_address}/{ndjson_files.pop(0)}')
                        except FileNotFoundError:
                            pass
                    if len(json_files) > constants.SENDING_DELAY:
                        error = send_to_server(f'{self.folder_address}/{json_files[0]}')
                        if not error:
                            os.remove(f'{self.folder_address}/{json_files.pop(0)}')
        else:
            print('Not installed')


def start():
    sysmon = Sysmon()
    try:
        sysmon.start()
    except KeyboardInterrupt:
        sysmon.handle_exit()
        return
