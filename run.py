from http import server
import os
import sys
import signal
import logging
from functools import partial

from monitor.helper.size import strtoint_byte_size
from monitor.helper.console_output import ConsoleOutput

from monitor.config.monitor_config import MonitorConfig
from monitor.config.ini_config_provider import IniConfigProvider

from monitor.application_search_criteria import ApplicationSearchCriteria
from monitor.application_finder import ApplicationFinder

from monitor.server_message_element_search_criteria import ServerMessageElementSearchCriteria
from monitor.server_message_element_finder import ServerMessageElementFinder

from monitor.server_message_processor.message_processor import MessageProcessor
from monitor.server_message_processor.trim_message_processor_options import TrimMessageProcessorOptions
from monitor.server_message_processor.trim_message_processor import TrimMessageProcessor

from monitor.server_message_processor.log_message_processor_options import LogMessageProcessorOptions
from monitor.server_message_processor.log_message_processor import LogMessageProcessor

from monitor.server_message_monitor.server_message_monitor_options import ServerMessageMonitorOptions
from monitor.server_message_monitor.server_message_monitor import ServerMessageMonitor
from monitor.server_message_monitor.server_message_monitor_controller import ServerMessageMonitorController

from monitor.server_controller.server_application_controller_options import ServerApplicationControllerOptions
from monitor.server_controller.server_start_stop_controller import ServerStartStopController

from pywinauto import Application
from pywinauto.controls.win32_controls import EditWrapper

def configure_logging() -> None:
    logging.basicConfig(filename = './logs/runtime/monitor.log', level=logging.DEBUG)

def sigint_signal_handler(sig_num, frame, monitor_ctrl:ServerMessageMonitorController, out:ConsoleOutput):
    print('')
    out.monitor_stop_requested()
    monitor_ctrl.stop_monitoring()
    out.monitor_stopped()

def build_processors(config: MonitorConfig) -> list[MessageProcessor]:
    processors: list[MessageProcessor] = []
    processor_names: list[str] = config.get_processors_names()

    if 'trim' in processor_names:
        trim_processor_options:TrimMessageProcessorOptions = TrimMessageProcessorOptions(
            max_line_count = config.get_processor_configuration_value('trim', 'max_line_count'), 
            leave_line_count = config.get_processor_configuration_value('trim', 'leave_line_count')
        )

        trim_processor:TrimMessageProcessor = TrimMessageProcessor(trim_processor_options)
        processors.append(trim_processor)

    if 'log' in processor_names:
        destination_file_path:str = os.path.join(
            os.path.join(os.path.realpath(config.get_processor_configuration_value('log', 'destination_dir'))),
            config.get_processor_configuration_value('log', 'destination_file_name')
        )

        rotate_size_bytes:int = strtoint_byte_size(config.get_processor_configuration_value('log', 'rotate_size'))

        log_processor_options: LogMessageProcessorOptions = LogMessageProcessorOptions(
            destination_file = destination_file_path,
            rotate_size_bytes = rotate_size_bytes
        )

        log_processor:LogMessageProcessor = LogMessageProcessor(log_processor_options)
        processors.append(log_processor)

    return processors

def build_application_finder(config:MonitorConfig) -> ApplicationFinder:
    app_search_criteria:ApplicationSearchCriteria = ApplicationSearchCriteria(
        config.get_app_search_configuration('type'), 
        config.get_app_search_configuration('keyword')
    )

    return ApplicationFinder(app_search_criteria)

def build_element_finder(app_finder:ApplicationFinder, config: MonitorConfig) -> ServerMessageElementFinder:
    server_messages_search_path = config.get_server_message_element_search_configuration('server_messages_search_path')
    process_messages_search_path = config.get_server_message_element_search_configuration('process_messages_search_path')

    server_messages_element_search_criteria:ServerMessageElementSearchCriteria = ServerMessageElementSearchCriteria(
        server_messages_search_path[:-1], 
        server_messages_search_path[-1:][0]
    )

    process_messages_element_search_criteria:ServerMessageElementSearchCriteria = ServerMessageElementSearchCriteria(
        process_messages_search_path[:-1], 
        process_messages_search_path[-1:][0]
    )

    element_finder:ServerMessageElementFinder = ServerMessageElementFinder(app_finder, 
        server_messages_element_search_criteria, 
        process_messages_element_search_criteria)
        
    return element_finder

def build_monitor(app_finder:ApplicationFinder, config: MonitorConfig) -> ServerMessageMonitor:
    target_element_finder:ServerMessageElementFinder = build_element_finder(app_finder, config)
    if target_element_finder is None:
        return None

    processors: list[MessageProcessor] = build_processors(config)

    monitor_options:ServerMessageMonitorOptions = ServerMessageMonitorOptions(config.get_poll_confg('poll_seconds'))
    monitor: ServerMessageMonitor = ServerMessageMonitor(monitor_options, 
        target_element_finder, 
        processors)

    return monitor

def build_server_controller(app_finder:ApplicationFinder, config: MonitorConfig) -> ServerStartStopController:
    options:ServerApplicationControllerOptions = ServerApplicationControllerOptions(
        config.get_server_controller_configuration('dir_path'),
        config.get_server_controller_configuration('parent_auto_ids'),
        config.get_server_controller_configuration('btn_start_selector'),
        config.get_server_controller_configuration('btn_stop_selector')
    )

    return ServerStartStopController(app_finder, options)

def build_monitor_controller(monitor: ServerMessageMonitor, config: MonitorConfig) -> ServerMessageMonitorController:
    return ServerMessageMonitorController(monitor)

def run_loop(server_ctrl: ServerStartStopController, monitor_ctrl: ServerMessageMonitorController, out:ConsoleOutput):
    is_monitor_started: bool = False
    while True:
        try:
            if not is_monitor_started:
                monitor_ctrl.start_monitoring()
                is_monitor_started = True

            line = input("\t> ")
            if line == 'quit':
                out.monitor_stop_requested()
                monitor_ctrl.stop_monitoring()
                out.monitor_stopped()

            elif line == 'start-ciel':
                out.server_start_requested()
                if not server_ctrl.is_started():
                    logging.debug('Attempting to start server...')
                    if server_ctrl.start():
                        out.error_message('Failed to start server.')
                    else:
                        out.generic_info('Successfully started server.')
                else:
                    logging.debug('Server is already started.')

            elif line == 'stop-ciel':
                out.server_stop_requested()
                if server_ctrl.is_started():
                    logging.debug('Attempting to stop server...')
                    if server_ctrl.stop():
                        out.error_message('Failed to stop server.')
                    else:
                        out.generic_info('Successfully stopped server.')
                else:
                    logging.debug('Server is already stopped.')

            elif line == 'status-ciel':
                if server_ctrl.is_started():
                    out.generic_info('Server is STARTED.')
                else:
                    out.generic_info('Server is STOPPED.')

            else:
                out.error_message('Unknown command')
        except EOFError:
            out.no_more_input()
        except:
            logging.exception('Unexpected error occurred in run loop')
            out.error_message('Unexpected error occurred in run loop')
            monitor_ctrl.stop_monitoring()
            out.monitor_stopped()
            break
        
        if monitor_ctrl.is_monitoring() is False:
            break

def run():
    global sigint_signal_handler

    out:ConsoleOutput = ConsoleOutput()
    out.begin()

    config: MonitorConfig = None
    app_finder: ApplicationFinder = None
    monitor: ServerMessageMonitor = None
    monitor_ctrl: ServerMessageMonitorController = None
    server_ctrl: ServerStartStopController = None

    try:
        configure_logging()
        config = get_config()

        app_finder = build_application_finder(config)
        server_ctrl = build_server_controller(app_finder, config)

        if not server_ctrl.is_started():
            logging.debug('Server is not started. Attempting to start...')
            out.attempting_to_start_server()
            
            if not server_ctrl.start():
                out.error_message('Failed to start server.')
                raise Exception('Failed to start server.')

            logging.debug('Server successfully started.')
            out.server_successfully_started()

        monitor = build_monitor(app_finder, config)

        if monitor is None:
            logging.debug('Target window not found')
            out.error_message('Target window not found!')
            out.end()
            return

        monitor_ctrl = build_monitor_controller(monitor, config)

        bound_sigint_signal_handler = partial(sigint_signal_handler, 
            monitor_ctrl=monitor_ctrl,
            out=out)
        signal.signal(signal.SIGINT, 
            bound_sigint_signal_handler)
    except:
        logging.exception('Unexpected error during monitoring setup')
        out.error_message('Unexpected error during monitoring setup')
        out.end()
        return

    run_loop(server_ctrl, monitor_ctrl, out)
    out.end()

def get_config() -> MonitorConfig:
    config_file = os.path.realpath('./config/monitor.ini')
    provider:IniConfigProvider = IniConfigProvider(config_file)
    return provider.get_config()

if __name__ == "__main__":
    run()