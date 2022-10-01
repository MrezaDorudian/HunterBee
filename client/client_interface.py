import multiprocessing
from client.sysmon.sysmon_interface import Sysmon


if __name__ == '__main__':
    sysmon = Sysmon()
    process_1 = multiprocessing.Process(target=sysmon.start)
    process_1.daemon = True
    process_1.start()
    try:
        process_1.join()
    except KeyboardInterrupt:
        process_1.terminate()
        exit(-10)

