from configparser import ConfigParser
from .monitor_config import MonitorConfig
from .monitor_config_provider import MonitorConfigProvider
from .default_monitor_config_provider import DefaultMonitorConfigProvider

class IniConfigProvider(MonitorConfigProvider):
    def __init__(self, file_path:str) -> None:
        super().__init__()
        self._file = file_path
        self._default_provider = DefaultMonitorConfigProvider()

    def get_config(self) -> MonitorConfig:
        config_src:ConfigParser = self._get_src()
        defaults:MonitorConfig = self._get_defaults()

        sections:list[str] = config_src.sections()

        app_search_config:dict[str, any] = self._get_app_search_config(config_src, 
            sections, 
            defaults)

        element_search_config:dict[str, any] = self._get_element_search_config(config_src, 
            sections, 
            defaults)

        poll_config:dict[str,any] = self._get_poll_config(config_src, 
            sections, 
            defaults)

        server_controller_config = self._get_server_controller_config(config_src, 
            sections, 
            defaults)

        trim_processor_config:dict[str, any] = self._get_trim_processor_config(config_src, 
            sections, 
            defaults)

        log_processor_config:dict[str,dict[str,any]] = self._get_log_processor_config(config_src, 
            sections, 
            defaults)

        processors_config = {
            'trim': trim_processor_config,
            'log': log_processor_config
        }

        config:MonitorConfig = MonitorConfig(app_search_config, 
            element_search_config, 
            poll_config, 
            server_controller_config,
            processors_config)

        return config

    def _get_app_search_config(self, config_src:ConfigParser, sections: list[str], defaults:MonitorConfig) -> dict[str, any]:
        c_type:str = None
        c_keyword:str = None

        if 'app_search_config' in sections:
            c_type = config_src['app_search_config']['type'] or None
            c_keyword = config_src['app_search_config']['keyword'] or None

        if c_type is None:
            c_type = defaults.get_app_search_configuration('type')
        if c_keyword is None:
            c_keyword = defaults.get_app_search_configuration('keyword')

        return {
            'type': c_type,
            'keyword': c_keyword
        }

    def _get_element_search_config(self, config_src:ConfigParser, sections: list[str], defaults:MonitorConfig) -> dict[str, any]:
        c_server_messages_search_path: list[str] = None
        c_process_messages_search_path: list[str] = None
        if 'element_search_config' in sections:
            c_server_messages_search_path = (config_src['element_search_config']['server_messages_search_path'] or '').split(',')
            c_process_messages_search_path = (config_src['element_search_config']['process_messages_search_path'] or '').split(',')

        if c_server_messages_search_path is None or len(c_server_messages_search_path) == 0:
            c_server_messages_search_path = defaults.get_server_message_element_search_configuration('server_messages_search_path')
        if c_process_messages_search_path is None:
            c_process_messages_search_path = defaults.get_server_message_element_search_configuration('process_messages_search_path')

        return {
            'server_messages_search_path': c_server_messages_search_path,
            'process_messages_search_path': c_process_messages_search_path
        }

    def _get_poll_config(self, config_src:ConfigParser, sections: list[str], defaults:MonitorConfig) -> dict[str, any]:
        poll_seconds:int = defaults.get_poll_confg('poll_seconds')
        if 'poll_config' in sections:
            c_poll_seconds = config_src['poll_config']['poll_seconds']
            if c_poll_seconds is not None and c_poll_seconds != '' and c_poll_seconds != '0':
                maybe_poll_seconds = int(c_poll_seconds)
                if maybe_poll_seconds > 0:
                    poll_seconds = maybe_poll_seconds

        return {
            'poll_seconds': poll_seconds
        }

    def _get_server_controller_config(self, config_src:ConfigParser, sections: list[str], defaults:MonitorConfig) -> dict[str, any]:
        c_dir_path: str = None
        c_parent_auto_ids:  list[str] = None
        c_btn_start_selector: str = None
        c_btn_stop_selector: str = None
        
        if 'server_controller_config' in sections:
            c_dir_path = config_src['server_controller_config']['dir_path'] or ''
            c_parent_auto_ids = (config_src['server_controller_config']['parent_auto_ids'] or '').split(',')
            c_btn_start_selector = config_src['server_controller_config']['btn_start_selector'] or ''
            c_btn_stop_selector = config_src['server_controller_config']['btn_stop_selector'] or ''

        if c_dir_path is None or len(c_dir_path) == 0:
            c_dir_path = defaults.get_server_controller_configuration('dir_path')
        if c_parent_auto_ids is None or len(c_parent_auto_ids) == 0:
            c_parent_auto_ids = defaults.get_server_controller_configuration('parent_auto_ids')
        if c_btn_start_selector is None or len(c_btn_start_selector) == 0:
            c_btn_start_selector = defaults.get_server_controller_configuration('btn_start_selector')
        if c_btn_stop_selector is None or len(c_btn_stop_selector) == 0:
            c_btn_stop_selector = defaults.get_server_controller_configuration('btn_stop_selector')

        return {
            'dir_path': c_dir_path,
            'parent_auto_ids': c_parent_auto_ids,
            'btn_start_selector': c_btn_start_selector,
            'btn_stop_selector': c_btn_stop_selector
        }

    def _get_trim_processor_config(self, config_src:ConfigParser, sections: list[str], defaults:MonitorConfig) -> dict[str, any]:
        trim_processor_config:dict[str, any] = defaults.get_processor_configuration('trim')
        if 'processors_config.trim' in sections:
            c_max_line_count = config_src['processors_config.trim']['max_line_count']
            c_leave_line_count = config_src['processors_config.trim']['leave_line_count']

            if c_max_line_count is not None and c_max_line_count != '' and c_max_line_count != '0':
                trim_processor_config['max_line_count'] = int(c_max_line_count)

            if c_leave_line_count is not None and c_leave_line_count != '' and c_leave_line_count != '0':
                trim_processor_config['leave_line_count'] = int(c_leave_line_count)  

        return trim_processor_config

    def _get_log_processor_config(self, config_src:ConfigParser, sections: list[str], defaults:MonitorConfig) -> dict[str, any]:
        log_processor_config:dict[str,dict[str,any]] = defaults.get_processor_configuration('log')
        if 'processors_config.log' in sections:
            c_destination_dir = config_src['processors_config.log']['destination_dir']
            c_destination_file_name = config_src['processors_config.log']['destination_file_name']
            c_rotate_size = config_src['processors_config.log']['rotate_size']

            if c_destination_dir is not None and c_destination_dir != '':
                log_processor_config['destination_dir'] = c_destination_dir

            if c_destination_file_name is not None and c_destination_file_name != '':
                log_processor_config['destination_file_name'] = c_destination_file_name

            if c_rotate_size is not None and c_rotate_size != '':
                log_processor_config['rotate_size'] = c_rotate_size

        return log_processor_config

    def _get_src(self) -> ConfigParser:
        config_src:ConfigParser = ConfigParser()
        config_src.read(self._file)
        return config_src

    def _get_defaults(self) -> MonitorConfig:
        return self._default_provider.get_config()