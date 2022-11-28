import json
import os
import yaml
from server import constants
from server.utils import get_file_list


class LogAggregator:
    def __init__(self):
        self.downloads_address = None
        self.aggregated_logs_address = None
        self.load_config()
        self.info = {'sysmon': {'log_id': 0, 'file_id': 0}, 'wireshark': {'log_id': 0, 'file_id': 0}}

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS) as f:
            config = yaml.safe_load(f)
            self.downloads_address = config['LogAggregator']['downloads_address']
            self.aggregated_logs_address = config['LogAggregator']['aggregated_logs_address']

    def aggregate_logs(self, file_list, log_type):
        output = {}
        for file in file_list:
            try:
                with open(f'{self.downloads_address}/{log_type}/{file}', 'r') as f:
                    data = json.load(f)
                    for item in data:
                        output[self.info[log_type]['log_id']] = data[item]
                        self.info[log_type]['log_id'] += 1
                os.remove(f'{self.downloads_address}/{log_type}/{file}')
            except:
                self.aggregated_logs_address(file, log_type)
        with open(f'{self.aggregated_logs_address}/{log_type}/aggregated-logs-{self.info[log_type]["file_id"]}.json',
                  'w') as f:
            json.dump(output, f, indent=4)

    def start(self):
        print('LogAggregator started')
        while True:
            sysmon_logs = get_file_list(f'{self.downloads_address}/sysmon')
            wireshark_logs = get_file_list(f'{self.downloads_address}/wireshark')
            if len(sysmon_logs) >= constants.AGGREGATE_DELAY:
                self.aggregate_logs(sysmon_logs[:constants.AGGREGATE_DELAY], 'sysmon')
                self.info['sysmon']['log_id'] = 0
                self.info['sysmon']['file_id'] += 1
            if len(wireshark_logs) >= constants.AGGREGATE_DELAY:
                self.aggregate_logs(wireshark_logs[:constants.AGGREGATE_DELAY], 'wireshark')
                self.info['wireshark']['log_id'] = 0
                self.info['wireshark']['file_id'] += 1


if __name__ == '__main__':
    log_aggregator = LogAggregator()
    log_aggregator.start()
