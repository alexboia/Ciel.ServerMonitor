import logging
from .server_message_monitor import ServerMessageMonitor

class ServerMessageMonitorController:
    def __init__(self, monitor: ServerMessageMonitor) -> None:
        self._monitor = monitor

    def start_monitoring(self):
        logging.debug('Starting monitoring...')
        self._monitor.start()
        logging.debug('Monitoring successfully started.')
        
    def stop_monitoring(self):
        logging.debug('Stopping monitoring...')
        try:
            self._monitor.request_stop()
            self._monitor.join()
            self._monitor.dispose()
            self._monitor = None
            logging.debug('Monitoring successfully stopped.')
        except:
            logging.exception('Error occurred whil stopping monitoring.')
       
    def is_monitoring(self):
        return self._monitor is not None and self._monitor.is_stop_requested() is False