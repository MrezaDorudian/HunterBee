import os
import subprocess
import time
import logs
import utils


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


def start():
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
                    utils.send_to_server(f'{logs.get_folder_address()}/{json_folders[0]}')
                    os.remove(f'{logs.get_folder_address()}/{json_folders[0]}')
            else:
                time.sleep(10)
    else:
        print('Not installed')
