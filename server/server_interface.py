from processor import aggregate, filter, check
from listener import listener
import threading
if __name__ == '__main__':
    server = listener.Server()
    aggregator = aggregate.LogAggregator()

    sysmon_filterer = filter.LogFilterer('sysmon')
    wireshark_filterer = filter.LogFilterer('wireshark')
    sysmon_checker = check.LogChecker('sysmon')
    wireshark_checker = check.LogChecker('wireshark')
    server_thread = threading.Thread(target=server.listen)
    aggregator_thread = threading.Thread(target=aggregator.start)
    sysmon_filterer_thread = threading.Thread(target=sysmon_filterer.start)
    wireshark_filterer_thread = threading.Thread(target=wireshark_filterer.start)
    sysmon_checker_thread = threading.Thread(target=sysmon_checker.start)
    wireshark_checker_thread = threading.Thread(target=wireshark_checker.start)
    try:
        server_thread.start()
        aggregator_thread.start()
        sysmon_filterer_thread.start()
        wireshark_filterer_thread.start()
        sysmon_checker_thread.start()
        wireshark_checker_thread.start()
    except KeyboardInterrupt:
        exit(0)
