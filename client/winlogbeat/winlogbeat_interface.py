import os
import subprocess
import yaml


def check_installed():
    current_directory = os.getcwd()
    os.chdir(get_bat_files_address())
    os.chdir(current_directory)
    result = subprocess.run([f'{get_bat_files_address()}/check.bat'], capture_output=True, text=True)
    return result.returncode == 0


def get_status():
    if check_installed():
        result = subprocess.run([f'{get_bat_files_address()}/check.bat'], capture_output=True, text=True)
        result_list = result.stdout.split('\n')
        status = [line.strip() for line in result_list if line.strip()][-1].split(' ')[0]
        return status
    else:
        return 'Not installed'


def utilities(command):
    try:
        subprocess.run([f'{get_bat_files_address()}/{command}.bat', get_folder_address()])
    except FileNotFoundError:
        print(f'{command} not found')


def get_folder_address():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        return config['winlogbeat']['address']


def get_bat_files_address():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        return config['winlogbeat']['bat_files_address']


# synchronize the output log file
def set_winlogbeat_config():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        sysmon_folder_address = config['sysmon']['address']

    with open(f'{get_folder_address()}/winlogbeat.yml', 'r+') as file:
        config = yaml.safe_load(file)
        if config['output.file']['path'] != sysmon_folder_address:
            config['output.file']['path'] = sysmon_folder_address
            file.seek(0)
            file.truncate()
            yaml.dump(config, file)
