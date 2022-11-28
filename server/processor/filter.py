import json
import os
import numpy as np
import yaml
from sklearn.cluster import KMeans
import server.constants as constants
import server.utils as utils


class FeatureExtractor:
    def __init__(self, file_address, log_type):
        self.file_address = file_address
        self.log_type = log_type
        self.lightweight_log = dict()
        self.generated_dataset = None

    def __str__(self):
        pass

    def extract_features(self):
        try:
            with open(self.file_address, 'r') as file:
                file_data = {}
                data = json.load(file)
                for item in data:
                    new_data = {}
                    if self.log_type == 'sysmon':
                        for key in constants.SYSMON_FEATURES:
                            try:
                                new_data[key] = data[item]['winlog']['event_data'][key]
                            except KeyError:
                                if key == 'Image':
                                    try:
                                        new_data[key] = data[item]['winlog']['event_data']['Image'].split('\\')[-1]
                                    except Exception:
                                        new_data[key] = 'Other'
                                new_data[key] = 'Other'
                    file_data[item] = new_data
                self.lightweight_log = file_data
        except json.decoder.JSONDecodeError:
            self.extract_features()

    def create_dataset(self):
        unique_data = dict()
        if self.log_type == 'sysmon':
            for item in constants.SYSMON_FEATURES:
                unique_data[item] = []

        for item in self.lightweight_log:
            for key in unique_data.keys():
                if self.lightweight_log[item][key] not in unique_data[key]:
                    unique_data[key].append(self.lightweight_log[item][key])
        for item in self.lightweight_log:
            for key in unique_data.keys():
                self.lightweight_log[item][key] = unique_data[key].index(self.lightweight_log[item][key])

        x_vector = []
        for item in self.lightweight_log:
            x_vector.append([_ for _ in self.lightweight_log[item].values()])
        self.generated_dataset = np.array(x_vector)

    def start(self):
        self.extract_features()
        self.create_dataset()


class Clustering(KMeans):
    def __init__(self, file_address, log_type):
        super().__init__(n_clusters=constants.CLUSTER_NUMBER)
        self.file_address = file_address
        self.log_type = log_type
        self.filtered_logs_address = None
        self.load_config()
        self.feature_extractor = FeatureExtractor(self.file_address, self.log_type)
        self.feature_extractor.start()
        self.labels, self.indexes = self.get_logs_to_process()

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS, 'r') as file:
            config = yaml.safe_load(file)
            self.filtered_logs_address = config['Clustering']['filtered_logs_address']

    def get_logs_to_process(self):
        self.fit(self.feature_extractor.generated_dataset)
        count_of_each_label = {}
        for i in self.labels_:
            if i not in count_of_each_label.keys():
                count_of_each_label[i] = 1
            else:
                count_of_each_label[i] += 1
        min_label = min(count_of_each_label, key=count_of_each_label.get)
        log_index = [x for x in range(len(self.labels_)) if self.labels_[x] == min_label]
        return self.labels_, log_index

    def filter_logs(self, output_address):
        with open(output_address, 'w') as output_file:
            new_data = {}
            with open(self.file_address, 'r') as input_file:
                data = json.load(input_file)
                for item in self.indexes:
                    new_data[item] = data[str(item)]
            json.dump(new_data, output_file, indent=4)


class LogFilterer:
    def __init__(self, log_type):
        self.log_type = log_type
        self.aggregated_logs_address = None
        self.filtered_logs_address = None
        self.load_config()
        pass

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS, 'r') as file:
            config = yaml.safe_load(file)
            self.aggregated_logs_address = config['LogFilterer']['aggregated_logs_address']
            self.filtered_logs_address = config['LogFilterer']['filtered_logs_address']

    def start(self):
        while True:
            aggregated_logs = utils.get_file_list(f'{self.aggregated_logs_address}/{self.log_type}')
            if len(aggregated_logs) > 0:
                if self.log_type == 'sysmon':
                    clustering = Clustering(f'{self.aggregated_logs_address}/{self.log_type}/{aggregated_logs[0]}',
                                            self.log_type)
                    clustering.filter_logs(
                        f'{self.filtered_logs_address}/{self.log_type}/filtered-logs-{aggregated_logs[0]}')
                    os.remove(f'{self.aggregated_logs_address}/{self.log_type}/{aggregated_logs[0]}')
                elif self.log_type == 'wireshark':
                    # copy file
                    try:
                        with open(f'{self.aggregated_logs_address}/{self.log_type}/{aggregated_logs[0]}', 'r') as fin:
                            data = json.load(fin)
                        with open(f'{self.filtered_logs_address}/{self.log_type}/filtered-logs-{aggregated_logs[0]}', 'w') as fout:
                            json.dump(data, fout)
                            os.remove(f'{self.aggregated_logs_address}/{self.log_type}/{aggregated_logs[0]}')
                    except json.decoder.JSONDecodeError:
                        self.start()


if __name__ == '__main__':
    log_filterer = LogFilterer('sysmon')
    log_filterer.start()
