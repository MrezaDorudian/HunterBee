import json
import os
import yaml
import server.constants as constants
import server.utils as utils
import requests
import webbrowser


class LogChecker:
    def __init__(self, log_type):
        self.log_type = log_type
        self.filtered_log_address = None
        self.database_address = None
        self.load_config()

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS, 'r') as file:
            data = yaml.safe_load(file)
            self.filtered_log_address = data['LogChecker']['filtered_logs_address']
            self.database_address = data['LogChecker']['database_address']

    def update_database(self, database):
        with open(f'{self.database_address}/database.json', 'w') as file:
            json.dump(database, file, indent=4)

    def check_database(self, executables_and_hashes):
        with open(f'{self.database_address}/database.json', 'r') as f1:
            database = json.load(f1)
            for key in executables_and_hashes.keys():
                if key not in database.keys():
                    database[key] = executables_and_hashes[key]
                    self.update_database(database)
                else:
                    if database[key]['threat'] == 'True':
                        print(f'دژ افزار in {database[key]["location"]}')
                        print(f'TimeStamp: {executables_and_hashes[key]["timestamp"]}')
                        with open(f'{self.database_address}/alerts.json', 'r+') as f2:
                            data = json.load(f2)
                            alert_counts = str(len(data))
                            data[alert_counts] = {'Timestamp': executables_and_hashes[key]["timestamp"],
                                                  'location': database[key]['location']}
                            f2.seek(0)
                            f2.truncate()
                            json.dump(data, f2, indent=4)
                            response = requests.post('http://localhost:8787/api/create.json', json={'title': 'alerts',
                                                                                                    'content': data})
                            webbrowser.open(response.json()['location'])
                    elif database[key]['threat'] == 'unknown':
                        print('we should check it')
                        result = utils.check_hash(database[key]['hash'])
                        database[key]['threat'] = result
                        self.update_database(database)

    def find_executables(self, file):
        try:
            with open(f'{self.filtered_log_address}/{self.log_type}/{file}', 'r') as f:
                data = json.load(f)
                info = {'executables': [], 'hashes': [], 'location': [], 'timestamp': []}
                for item in data:
                    info['timestamp'].append(data[item]['@timestamp'])
                    try:
                        info['executables'].append((data[item]['winlog']['event_data']['Image'].split('\\')[-1]))
                        info['location'].append(data[item]['winlog']['event_data']['Image'])
                    except Exception:
                        info['executables'].append('None')
                        info['location'].append('None')
                    try:
                        info['hashes'].append(data[item]['winlog']['event_data']['Hashes'].split('=')[-1])
                    except Exception:
                        info['hashes'].append('None')
                return info['executables'], info['hashes'], info['location'], info['timestamp']
        except json.decoder.JSONDecodeError:
            self.find_executables(file)

    def check_packets(self, file):
        try:
            with open(file, 'r') as f1:
                data = json.load(f1)
                for item in data:
                    try:
                        flags = int(data[item]['tcp']['tcp.flags'], 16)
                        header_length = int(data[item]['tcp']['tcp.hdr_len'])
                        # Extracted Rule for Stealth Scan
                        if (flags <= 3) and (header_length <= 28):
                            print(f'Nmap Stealth scanning detected from {data[item]["ip"]["ip.src"]}')
                            print(f'TimeStamp: {data[item]["tcp"]["Timestamps"]["tcp.time_delta"]}')
                            with open(f'{self.database_address}/alerts.json', 'r+') as f2:
                                print('too file E')
                                json_data = json.load(f2)
                                alert_counts = str(len(json_data))
                                json_data[alert_counts] = {
                                    'Timestamp': data[item]["tcp"]["Timestamps"]["tcp.time_delta"],
                                    'SourceIP': data[item]["ip"]["ip.src"]}
                                f2.seek(0)
                                f2.truncate()
                                json.dump(json_data, f2, indent=4)
                                response = requests.post('http://localhost:8787/api/create.json',
                                                         json={'title': 'alerts',
                                                               'content': json_data})
                                webbrowser.open(response.json()['location'])


                    except Exception:
                        continue
        except json.decoder.JSONDecodeError:
            self.check_packets(file)

    def start(self):
        try:
            while True:
                filtered_logs = utils.get_file_list(f'{self.filtered_log_address}/{self.log_type}')
                if len(filtered_logs) > 0:
                    if self.log_type == 'sysmon':
                        executables, hashes, location, timestamp = self.find_executables(filtered_logs[0])
                        gathered_info = {}
                        for i in range(len(executables)):
                            if executables[i] not in gathered_info.keys():
                                gathered_info[executables[i].lower()] = {'hash': hashes[i], 'location': location[i],
                                                                         'threat': 'unknown', 'timestamp': timestamp[i]}
                        self.check_database(gathered_info)
                    elif self.log_type == 'wireshark':
                        self.check_packets(f'{self.filtered_log_address}/{self.log_type}/{filtered_logs[0]}')
                    os.remove(f'{self.filtered_log_address}/{self.log_type}/{filtered_logs[0]}')
        except TypeError:
            self.start()


if __name__ == '__main__':
    log_checker = LogChecker('sysmon')
    log_checker.start()
