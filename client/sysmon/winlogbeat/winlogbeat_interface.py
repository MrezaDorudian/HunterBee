import subprocess
import yaml
from client import constants


class Winlogbeat:
    def __init__(self):
        self.folder_address = None
        self.bat_file_addresses = None
        self.load_config()
        self.installed = self.check_installed()
        self.status = self.get_status()
        # self.synchronize_winlogbeat_config()

    def __str__(self):
        return f'Winlogbeat Object\ninstalled: {self.installed}, status: {self.status}'

    def check_installed(self):
        result = subprocess.run([f'{self.bat_file_addresses}/check.bat'], capture_output=True, text=True)
        return result.returncode == 0

    def get_status(self):
        if self.installed:
            result = subprocess.run([f'{self.bat_file_addresses}/check.bat'], capture_output=True, text=True)
            result_list = result.stdout.split('\n')
            status = [line.strip() for line in result_list if line.strip()][-1].split(' ')[0]
            return status
        else:
            return 'Not installed'

    def restart(self):
        self.utilities('stop')
        self.utilities('start')

    def utilities(self, command):
        if self.installed or command == 'install':
            try:
                subprocess.run([f'{self.bat_file_addresses}/{command}.bat', self.folder_address])
            except FileNotFoundError:
                print(f'{command} not valid')
        else:
            print('Winlogbeat is not installed')

    def load_config(self):
        with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
            config = yaml.safe_load(file)
            self.bat_file_addresses = config['winlogbeat']['bat_files_address']
            self.folder_address = config['winlogbeat']['address']

    def synchronize_winlogbeat_config(self):
        with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
            config = yaml.safe_load(file)
            sysmon_folder_address = config['sysmon']['address']

        with open(f'{self.folder_address}/winlogbeat.yml', 'r+') as file:
            config = yaml.safe_load(file)
            if config['output.file']['path'] != sysmon_folder_address:
                config['output.file']['path'] = sysmon_folder_address
                file.seek(0)
                file.truncate()
                yaml.dump(config, file)
