import logging
import time
import threading

from pywinauto.controls.win32_controls import EditWrapper

from ..helper.set_edit_text import set_edit_text_direct
from ..helper.console_output import ConsoleOutput

from .server_message_monitor_options import ServerMessageMonitorOptions
from ..server_message_element_finder import ServerMessageElementFinder
from ..server_message_processor.processing_result import ProcessingResult
from ..server_message_processor.message_processor import MessageProcessor

class ServerMessageMonitor(threading.Thread):
    def __init__(self, options: ServerMessageMonitorOptions, target_element_finder:ServerMessageElementFinder, processors: list[MessageProcessor]):
        threading.Thread.__init__(self)
        self._options = options
        self._target_element_finder = target_element_finder
        self._processors = processors
        self._stop_requested = False
        self._max_retry_count = 3

    def run(self):
        poll_seconds:int = self._get_poll_seconds()
        #Todo: handle total crashes and restart loop
        while not self._stop_requested:
            logging.debug('Begin clear additional logs...')
            self._clear_additional_server_log()
            logging.debug('Done clear additional logs.')

            if self._stop_requested:
                logging.debug('Stop requested. Exiting loop...')
                break

            can_continue: bool = self._discreet_sleep(1)
            if not can_continue:
                logging.debug('Stop requested. Exiting loop...')
                break
            
            logging.debug('Begin processing server messages...')
            self._process_server_messages()
            logging.debug('Done processing server messages.')

            if self._stop_requested:
                logging.debug('Stop requested. Exiting loop...')
                break

            can_continue = self._discreet_sleep(poll_seconds)
            if not can_continue:
                logging.debug('Stop requested. Exiting loop...')
                break

    def _discreet_sleep(self, seconds:int) -> None:
        sec: int = 0
        can_countinue: bool = True

        while sec < seconds:
            if self._stop_requested:
                can_countinue = False
                break
            time.sleep(1)
            sec += 1

        return can_countinue

    def _clear_additional_server_log(self) -> None:
        retry_count:int = 0
        while retry_count < self._max_retry_count and not self._stop_requested:
            try:
                target_process_element:EditWrapper = self._target_element_finder.find_process_messages_element()
                if target_process_element is None:
                    logging.debug('Process log element not found - probably tab not accessed yet.')
                    retry_count += 1
                    continue

                try:
                    target_process_element.set_edit_text('')
                    logging.debug('Successfully set text using .set_edit_text()')
                except:
                    logging.exception('Error setting text via .set_edit_text(). Attempting direct call...')
                    set_edit_text_direct(target_process_element, '')
                    logging.debug('Successfully set text using direct call')
                break
            except:
                logging.exception('Process log element not found after %d retries' % (retry_count))
                retry_count += 1

    def _process_server_messages(self):
        result:ProcessingResult = None
        target_server_element:EditWrapper = None
        retry_count:int = 0

        while retry_count < self._max_retry_count and not self._stop_requested:
            try:
                target_server_element = self._target_element_finder.find_server_messages_element()
                break
            except:
                retry_count += 1

        if target_server_element is not None:
            for p in self._processors:
                try:
                    result = p.process_text_lines(target_server_element, result)
                except:
                    logging.exception('Error running processor %s' % (p.__class__))
        else:
            logging.warning('Server log element not found after %d retries' % (retry_count))

    def _get_poll_seconds(self) -> int:
        return self._options.get_poll_seconds()

    def request_stop(self):
        self._stop_requested = True

    def is_stop_requested(self) -> bool:
        return self._stop_requested

    def dispose(self):
        self._processors = None
        self._target_element_finder = None
        self._options = None
        self._stop_requested = False
