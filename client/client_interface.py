import multiprocessing
import os
import constants
import yaml
from sysmon import sysmon_interface
from wireshark import wireshark_interface

if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=sysmon_interface.start)
    process_2 = multiprocessing.Process(target=wireshark_interface.start)
    process_1.start()
    process_2.start()
    try:
        process_1.join()
        process_2.join()
    except KeyboardInterrupt:
        process_1.terminate()
        process_2.terminate()
    finally:
        with open(constants.CLIENT_CONFIG_ADDRESS, 'r') as file:
            config = yaml.safe_load(file)
            sysmon_folder = config['sysmon']['address']
            wireshark_folder = config['wireshark']['address']
            os.chdir(sysmon_folder)
            for _ in os.listdir():
                os.remove(_)
            os.chdir(wireshark_folder)
            for _ in os.listdir():
                os.remove(_)
        exit(0)
