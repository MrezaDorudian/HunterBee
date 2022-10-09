import os
import requests
from server.listener.listener import constants


def get_file_list(folder_address):
    log_type = ''
    if 'sysmon' in folder_address:
        log_type = 'sysmon'
    elif 'wireshark' in folder_address:
        log_type = 'wireshark'
    if 'aggregated' in folder_address:
        log_type = 'aggregated'
    if 'filtered' in folder_address:
        log_type = 'filtered'
    target_file_list = [x for x in os.listdir(folder_address) if x.count(f'{log_type}-logs') > 0]
    target_file_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    return target_file_list


def check_hash(targe_hash):
    params = {'apikey': constants.API_KEY, 'resource': targe_hash}
    url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    json_response = url.json()
    if json_response['response_code'] == 1:
        is_threat = json_response['positives'] / json_response['total'] > 0.2
        if is_threat:
            return 'True'
        else:
            return 'False'
    else:
        return 'not found'
