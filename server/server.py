import json
import os
import socket
import numpy as np
import yaml
from sklearn.preprocessing import StandardScaler

import constants
import pickle
from sklearn.cluster import KMeans
import matplotlib
import utils
import requests

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import threading


class Server:
    def __init__(self):
        self.address = None
        self.port = None
        self.downloads_address = None
        self.load_config()

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS) as f:
            config = yaml.safe_load(f)
            self.address = config['server']['address']
            self.port = config['server']['port']
            self.downloads_address = config['server']['downloads_address']

    def handle_exit(self):
        print('Server closed')
        os.chdir(f'{self.downloads_address}/Sysmon')
        for file in os.listdir():
            os.remove(file)
        os.chdir(f'{self.downloads_address}/Wireshark')
        for file in os.listdir():
            os.remove(file)
        return

    def listen(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(self.address, self.port)
            server_socket.bind((self.address, self.port))
            print('Server is listening on port', self.port)
            server_socket.listen(1)
            while True:
                client_socket, client_address = server_socket.accept()
                file_name = client_socket.recv(1024).decode('utf-8')
                self.receive_logs(file_name, client_socket)
        except KeyboardInterrupt:
            pass
            # self.handle_exit()

    def receive_logs(self, file_name, client_socket):
        if 'sysmon' in file_name:
            saving_location = f'{self.downloads_address}/Sysmon/{file_name}'
        elif 'wireshark' in file_name:
            saving_location = f'{self.downloads_address}/Wireshark/{file_name}'
        else:
            saving_location = file_name

        with open(saving_location, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)
            print('File received')
            client_socket.close()


class LogProcessor:
    def __init__(self):
        self.downloads_address = None
        self.combined_logs_address = None
        self.load_config()

    def __str__(self):
        pass

    def load_config(self):
        with open(constants.SERVER_CONFIG_ADDRESS) as f:
            config = yaml.safe_load(f)
            self.downloads_address = config['LogProcessor']['downloads_address']
            self.combined_logs_address = config['LogProcessor']['combined_logs_address']

    def combine_logs(self):
        def combine(file_list, log_type, log_id, file_id):
            output = {}
            for file in file_list:
                with open(f'{self.downloads_address}/{log_type}/{file}', 'r') as f:
                    data = json.load(f)
                    for item in data:
                        output[log_id] = data[item]
                        log_id += 1
                os.remove(f'{self.downloads_address}/{log_type}/{file}')
            with open(f'{self.combined_logs_address}/{log_type}/combined-logs-{file_id}.json', 'w') as f:
                json.dump(output, f, indent=4)

        sysmon_log_id, sysmon_file_id = 0, 0
        wireshark_log_id, wireshark_file_id = 0, 0

        while True:
            sysmon_logs = utils.get_file_list(f'{self.downloads_address}/Sysmon')
            wireshark_logs = utils.get_file_list(f'{self.downloads_address}/Wireshark')
            if len(sysmon_logs) >= 10:
                combine(sysmon_logs[:10], 'Sysmon', sysmon_log_id, sysmon_file_id)
                sysmon_log_id = 0
                sysmon_file_id += 1
            if len(wireshark_logs) >= 10:
                combine(wireshark_logs[:10], 'Wireshark', wireshark_log_id, wireshark_file_id)
                wireshark_log_id = 0
                wireshark_file_id += 1

    def extract_features(self, file_name):
        with open(f'{self.combined_logs_address}/Sysmon/{file_name}', 'r') as f:
            file_data = {}
            data = json.load(f)
            for item in data:
                new_data = {}
                useful = ['ParentProcessGuid', 'Image', 'ParentImage']
                for key in useful:
                    try:
                        new_data[key] = data[item]['winlog']['event_data'][key]
                    except Exception:
                        if key == 'Image':
                            try:
                                new_data[key] = data[item]['winlog']['event_data']['Image'].split('\\')[-1]
                                # new_data[key] = data[item]['winlog']['event_data']['SourceImage']
                            except Exception:
                                new_data[key] = 'Other'
                        new_data[key] = 'Other'
                file_data[item] = new_data
        with open(f'{self.combined_logs_address}/Sysmon/lightweight-{file_name}', 'w') as f:
            json.dump(file_data, f, indent=4)

    def create_dataset(self, file):
        with open(f'{self.combined_logs_address}/Sysmon/{file}', 'r') as f:
            unique_data = {'ParentProcessGuid': [], 'Image': [], 'ParentImage': []}
            data = json.load(f)
            for item in data:
                for key in unique_data.keys():
                    if data[item][key] not in unique_data[key]:
                        unique_data[key].append(data[item][key])
            for item in data:
                for key in unique_data.keys():
                    data[item][key] = unique_data[key].index(data[item][key])
        with open(f'{self.combined_logs_address}/Sysmon/unique-processed-logs.json', 'w') as f:
            json.dump(data, f, indent=4)

        x = []
        with open(f'{self.combined_logs_address}/Sysmon/unique-processed-logs.json', 'r') as f:
            data = json.load(f)
            temp = []
            for item in data:
                temp.append([_ for _ in data[item].values()])
            x.append(temp)
        with open(f'{self.combined_logs_address}/Sysmon/dataset.pkl', 'wb') as f:
            pickle.dump(x, f)
        os.remove(f'{self.combined_logs_address}/Sysmon/{file}')
        # os.remove(f'{self.combined_logs_address}/Sysmon/unique-processed-logs.json')

    def filter(self):
        while True:
            combined_files = [x for x in os.listdir(f'{self.combined_logs_address}/Sysmon') if
                              x.count(f'combined-logs') > 0]
            combined_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
            if len(combined_files) > 1:
                self.extract_features(combined_files[0])
                self.create_dataset(f'lightweight-{combined_files[0]}')
                os.rename(f'{self.combined_logs_address}/Sysmon/{combined_files[0]}',
                          f'{self.combined_logs_address}/Sysmon/reserved/{combined_files[0]}')
                clustering = Clustering()
                labels, indexes = clustering.get_logs_to_process()
                count_of_each_label = {}
                for i in labels:
                    if i not in count_of_each_label.keys():
                        count_of_each_label[i] = 1
                    else:
                        count_of_each_label[i] += 1
                print(count_of_each_label)
                save_chosen_logs(combined_files[0], indexes)

    def update_database(self, executables_and_hashes, database, key):
        database[key] = executables_and_hashes[key]
        with open('combined_logs/Sysmon/database/database.json', 'w') as f:
            json.dump(database, f, indent=4)

    def check_database(self, executables_and_hashes):
        with open('combined_logs/Sysmon/database/database.json', 'r') as f:
            database = json.load(f)
            for key in executables_and_hashes.keys():
                if key not in database.keys():
                    self.update_database(executables_and_hashes, database, key)
                else:
                    if database[key]['threat'] == 'True':
                        print(f'fucking دژ افزار in {database[key]["location"]}')
                    elif database[key]['threat'] == 'unknown':
                        print('we should check it')
                        # result = check_hash(database[key]['hash'])
                        # with open('combined_logs/Sysmon/database/database.json', 'r') as f1:
                        #     database = json.load(f1)
                        #     database[key]['threat'] = result
                        #     with open('combined_logs/Sysmon/database/database.json', 'w') as f2:
                        #         json.dump(database, f2, indent=4)

    def check(self):
        while True:
            log_files = [x for x in os.listdir(f'{self.combined_logs_address}/Sysmon/filtered') if
                         x.count(f'filtered-') > 0]
            log_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
            if len(log_files) > 1:
                executables, hashes, location = find_executables(log_files[0])
                unique_executable_and_hash = {}
                for i in range(len(executables)):
                    if executables[i] not in unique_executable_and_hash.keys():
                        unique_executable_and_hash[executables[i].lower()] = {'hash': hashes[i],
                                                                              'location': location[i],
                                                                              'threat': 'unknown'}
                self.check_database(unique_executable_and_hash)
                os.remove(f'{self.combined_logs_address}/Sysmon/filtered/{log_files[0]}')


class Clustering:
    def __init__(self):
        self.dataset = None
        self.load_dataset()

    def __str__(self):
        pass

    def load_dataset(self):
        with open('combined_logs/Sysmon/dataset.pkl', 'rb') as f:
            self.dataset = pickle.load(f)[0]
            self.dataset = StandardScaler().fit_transform(self.dataset)

    def plot_silhouette_score(self):
        scores = []
        for i in range(2, 10):
            kmeans = KMeans(n_clusters=i, random_state=0).fit(self.dataset)
            score = silhouette_score(self.dataset, kmeans.labels_)
            scores.append(score)
        plt.plot(range(2, 10), scores)
        plt.show()

    def plot_elbow(self):
        scores = []
        for i in range(1, 10):
            kmeans = KMeans(n_clusters=i, random_state=0).fit(self.dataset)
            score = kmeans.inertia_
            scores.append(score)
        plt.plot(range(1, 10), scores)
        plt.show()

    def get_logs_to_process(self):
        kmeans = KMeans(n_clusters=2).fit(self.dataset)
        count_of_each_label = {}
        for i in kmeans.labels_:
            if i not in count_of_each_label.keys():
                count_of_each_label[i] = 1
            else:
                count_of_each_label[i] += 1
        min_label = min(count_of_each_label, key=count_of_each_label.get)
        log_index = [x for x in range(len(kmeans.labels_)) if kmeans.labels_[x] == min_label]
        return np.ndarray.tolist(kmeans.labels_), log_index


def save_chosen_logs(file, indexes):
    with open(f'combined_logs/Sysmon/filtered/filtered-{file}', 'w') as f:
        new_data = {}
        with open(f'combined_logs/Sysmon/reserved/{file}', 'r') as fl:
            data = json.load(fl)
            for item in indexes:
                new_data[item] = data[str(item)]
        json.dump(new_data, f, indent=4)


def find_executables(file):
    with open(f'combined_logs/Sysmon/filtered/{file}', 'r') as f:
        print(file)
        data = json.load(f)
        executables = []
        hashes = []
        location = []
        for item in data:
            try:
                executables.append((data[item]['winlog']['event_data']['Image'].split('\\')[-1]))
                location.append(data[item]['winlog']['event_data']['Image'])
            except Exception:
                executables.append('None')
                location.append('None')
            try:
                hashes.append(data[item]['winlog']['event_data']['Hashes'].split('=')[-1])
            except Exception:
                hashes.append('None')
        return executables, hashes, location


def check_hash(hash_):
    api_key = '40e1a086cd412e236cf6436a791f26b3bf2c92c5fc3f356db727b6debd7226db'
    params = {'apikey': api_key, 'resource': hash_}
    url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    print(url)
    print(url.json())
    json_response = url.json()
    if json_response['response_code'] == 1:
        is_threat = json_response['positives'] / json_response['total'] > 0.2
        if is_threat:
            return 'True'
        else:
            return 'False'
    else:
        return 'not found'


if __name__ == '__main__':
    server = Server()
    log_processor = LogProcessor()
    server_thread = threading.Thread(target=server.listen)
    combiner_thread = threading.Thread(target=log_processor.combine_logs)
    filterer_thread = threading.Thread(target=log_processor.filter)
    checker_thread = threading.Thread(target=log_processor.check)
    server_thread.daemon = True
    combiner_thread.daemon = True
    filterer_thread.daemon = True
    checker_thread.daemon = True
    server_thread.start()
    combiner_thread.start()
    filterer_thread.start()
    checker_thread.start()
    combiner_thread.join()
    filterer_thread.join()
    checker_thread.join()
    server_thread.join()
