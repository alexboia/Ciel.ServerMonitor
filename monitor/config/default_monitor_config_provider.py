from .monitor_config import MonitorConfig
from .monitor_config_provider import MonitorConfigProvider

class DefaultMonitorConfigProvider(MonitorConfigProvider):
    def get_config(self) -> MonitorConfig:
        app_search_config:dict[str, any] = {
            'type': 'regexp_title', 
            'keyword': '(.*)Administrare Server(.*)'
        }

        element_search_config:dict[str, any] = {
            'server_messages_search_path': ['tbServer.select','txtServerMessages', 'Edit'],
            'process_messages_search_path': ['tabPageTasks.select','txtProcessMessages', 'Edit']
        }

        poll_config:dict[str,any] = {
            'poll_seconds': 1
        }

        server_controller_config: dict[str, any] = {
            'ciel_dir_path': r'C:\Program Files\NextUp Software\NextUp ERP Complet',
            'parent_auto_ids': ['FrmWebServicesControlPanel'],
            'btn_start_selector': 'btnStartServer',
            'btn_stop_selector': 'btnStopServer'
        }

        processors_config = {
            'trim': {
                'max_line_count': 100,
                'leave_line_count': 10
            },
            'log': {
                'destination_dir': './logs',
                'destination_file_name': 'server-messages-$datetime$-$rindex$.log',
                'rotate_size': '1M'
            }
        }

        config:MonitorConfig = MonitorConfig(app_search_config, 
            element_search_config, 
            poll_config, 
            server_controller_config,
            processors_config)

        return config