import os
import yaml
import ndjson


def read_logs():
    log_files = []
    for file in os.listdir(get_folder_address()):
        log_files.append(file)
    for file in log_files:
        with open(f'{get_folder_address()}/{file}') as f:
            data = ndjson.load(f)
            yield data


def get_folder_address():
    with open('../config.yaml') as file:
        config = yaml.safe_load(file)
        return config['sysmon']['folder_address']

