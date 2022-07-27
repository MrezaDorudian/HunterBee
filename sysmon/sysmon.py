import subprocess


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
        result = subprocess.run(['sysmon.exe', '-s'], capture_output=True, text=True)

        config = f'<{"<".join(result.stdout.split("<")[1:])}'
        print(config)
        with open('current_config.xml', 'w') as f:
            f.write(config)


def set_config(file_address):
    if check_installed():
        subprocess.run(['sysmon.exe', '-c', file_address])
    else:
        print('Not installed')
