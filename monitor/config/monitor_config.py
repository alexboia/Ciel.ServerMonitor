class MonitorConfig:
    def __init__(self, app_search:dict[str,any], element_search:dict[str, any], poll:dict[str, any], server_controller: dict[str, any], processors: dict[str, dict[str, any]]) -> None:
        self._app_search = app_search
        self._element_search = element_search
        self._poll = poll
        self._server_controller = server_controller
        self._processors = processors

    def get_app_search_configuration(self, key:str, defaultValue: any = None) -> any:
        return self._app_search.get(key) or defaultValue

    def get_server_message_element_search_configuration(self, key:str, default_value:any = None) -> any:
        return self._element_search.get(key) or default_value

    def get_poll_confg(self, key:str, default_value:any = None) -> any:
        return self._poll.get(key) or default_value

    def get_processors_names(self) -> list[str]:
        return list(self._processors.keys())

    def get_server_controller_configuration(self, key:str, default_value:any = None) -> any:
        return self._server_controller.get(key) or default_value

    def get_processor_configuration(self, processor_name:str) -> dict[str, any]:
        return self._processors.get(processor_name)

    def get_processor_configuration_value(self, processor_name:str, key:str, default_value:any = None) -> any:
        processorConfig:dict[str, any] = self.get_processor_configuration(processor_name)
        if processorConfig is not None:
            return processorConfig.get(key) or default_value
        else:
            return default_value