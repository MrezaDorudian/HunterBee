import yaml
import ndjson
import json


def read_logs(file_name, counter):
    output_data = {}
    iterator = 0
    with open(f'{get_folder_address()}/{file_name}') as f:
        data = ndjson.load(f)
        for item in data:
            for key in ['@metadata', 'event', 'log', 'ecs', 'agent', 'message']:
                item.pop(key)
            for key in ['user', 'process', 'record_id', 'api', 'opcode', 'event_id', 'version', 'channel']:
                item['winlog'].pop(key)
            for key in ['os', 'mac', 'id', 'hostname', 'architecture']:
                item['host'].pop(key)
            output_data[iterator] = item
            iterator += 1
    # write output data as json file
    # json_address
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        json_address = config['sysmon']['address']
    with open(f'{json_address}/sysmon-logs-{counter}.json', 'w') as f:
        json.dump(output_data, f, indent=4)


def get_folder_address():
    with open(r'C:\Users\mrdor\PycharmProjects\Hunterbee\client\config.yaml') as file:
        config = yaml.safe_load(file)
        return config['sysmon']['address']






