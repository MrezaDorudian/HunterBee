import json
import os
import yaml
import server.constants as constants
import server.utils as utils


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

    def update_database(self, executables_and_hashes, database, key):
        database[key] = executables_and_hashes[key]
        with open(f'{self.database_address}/database.json', 'w') as f:
            json.dump(database, f, indent=4)

    def check_database(self, executables_and_hashes):
        with open(f'{self.database_address}/database.json', 'r') as f:
            database = json.load(f)
            for key in executables_and_hashes.keys():
                if key not in database.keys():
                    self.update_database(executables_and_hashes, database, key)
                else:
                    if database[key]['threat'] == 'True':
                        print(f'fucking دژ افزار in {database[key]["location"]}')
                    elif database[key]['threat'] == 'unknown':
                        print('we should check it')
                        result = utils.check_hash(database[key]['hash'])
                        with open('combined_logs/sysmon/database/database.json', 'r') as f1:
                            database = json.load(f1)
                            database[key]['threat'] = result
                            with open('combined_logs/sysmon/database/database.json', 'w') as f2:
                                json.dump(database, f2, indent=4)

    def find_executables(self, file):
        with open(f'{self.filtered_log_address}/{self.log_type}/{file}', 'r') as f:
            data = json.load(f)
            info = {'executables': [], 'hashes': [], 'location': []}
            for item in data:
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
            return info['executables'], info['hashes'], info['location']

    def start(self):
        while True:
            filtered_logs = utils.get_file_list(f'{self.filtered_log_address}/{self.log_type}')
            if len(filtered_logs) > 1:
                executables, hashes, location = self.find_executables(filtered_logs[0])
                gathered_info = {}
                for i in range(len(executables)):
                    if executables[i] not in gathered_info.keys():
                        gathered_info[executables[i].lower()] = {'hash': hashes[i], 'location': location[i],
                                                                 'threat': 'unknown'}
                self.check_database(gathered_info)
                os.remove(f'{self.filtered_log_address}/{self.log_type}/{filtered_logs[0]}')


if __name__ == '__main__':
    log_checker = LogChecker('sysmon')
    log_checker.start()
