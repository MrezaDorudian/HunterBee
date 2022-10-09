from server.listener import listener
from processor import aggregate, filter, check
from listener import listener
import threading
if __name__ == '__main__':
    server = listener.Server()
    aggregator = aggregate.LogAggregator()
    filterer = filter.LogFilterer('sysmon')
    checker = check.LogChecker('sysmon')
    server_thread = threading.Thread(target=server.listen)
    aggregator_thread = threading.Thread(target=aggregator.start)
    filterer_thread = threading.Thread(target=filterer.start)
    checker_thread = threading.Thread(target=checker.start)
    try:
        server_thread.start()
        aggregator_thread.start()
        filterer_thread.start()
        checker_thread.start()
    except KeyboardInterrupt:
        exit(0)

