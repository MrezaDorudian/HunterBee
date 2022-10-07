import os


def get_file_list(folder_address):
    if 'Sysmon' in folder_address:
        log_type = 'sysmon'
    elif 'Wireshark' in folder_address:
        log_type = 'wireshark'
    else:
        log_type = 'combined'
    target_file_list = [x for x in os.listdir(folder_address) if x.count(f'{log_type}-logs') > 0]
    target_file_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    return target_file_list
