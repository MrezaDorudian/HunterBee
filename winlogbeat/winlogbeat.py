import subprocess
import yaml


def check_installed():
    result = subprocess.run(['check.bat'], capture_output=True, text=True)
    return result.returncode == 0


def get_status():
    if check_installed():
        result = subprocess.run(['check.bat'], capture_output=True, text=True)
        result_list = result.stdout.split('\n')
        status = [line.strip() for line in result_list if line.strip()][-1].split(' ')[0]
        return status
    else:
        return 'Not installed'


def utilities(command):
    try:
        subprocess.run([f'{command}.bat', get_folder_address()])
    except FileNotFoundError:
        print(f'{command} not found')


def get_folder_address():
    with open('../config.yaml') as file:
        config = yaml.safe_load(file)
        return config['winlogbeat']['folder_address']
