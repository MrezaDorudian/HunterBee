import os
import subprocess
import time
import logs
import client.utils as utils
import client.winlogbeat.winlogbeat_interface as winlogbeat


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
        try:
            winlogbeat.utilities('start')
            while True:
                ndjson_files = [x for x in os.listdir(logs.get_folder_address()) if x.count('.ndjson') > 0]
                ndjson_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
                json_files = [x for x in os.listdir(logs.get_folder_address()) if x.count('.json') > 0]
                json_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
                if len(ndjson_files) > 2 or len(json_files) > 2:
                    if len(ndjson_files) > 2:
                        file_id = ndjson_files[0].split('.')[0].split('-')[-1]
                        logs.read_logs(ndjson_files[0], file_id)
                        os.remove(f'{logs.get_folder_address()}/{ndjson_files.pop(0)}')

                    if len(json_files) > 2:
                        try:
                            utils.send_to_server(f'{logs.get_folder_address()}/{json_files[0]}')
                            os.remove(f'{logs.get_folder_address()}/{json_files.pop(0)}')
                        except ConnectionRefusedError:
                            print('server not listening')
                else:
                    time.sleep(10)
        except Exception as e:
            print(e)
            raise KeyboardInterrupt

    else:
        print('Not installed')


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        winlogbeat.utilities('stop')
        time.sleep(1)
        utils.send_remaining_files(logs.get_folder_address(), 'sysmon')
        os.chdir(logs.get_folder_address())
        for file in os.listdir():
            os.remove(file)
        exit(-1)
