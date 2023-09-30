import logging
from pywinauto import Application, WindowSpecification
from pywinauto.controls.win32_controls import EditWrapper
from pywinauto.findwindows import ElementNotFoundError
from .server_message_element_search_criteria import ServerMessageElementSearchCriteria
from .application_finder import ApplicationFinder
from .helper.ui import find_target_window

class ServerMessageElementFinder:
    def __init__(self, application_finder: ApplicationFinder, server_criteria: ServerMessageElementSearchCriteria, process_criteria: ServerMessageElementSearchCriteria ) -> None:
        self._application_finder = application_finder
        self._server_criteria = server_criteria
        self._process_criteria = process_criteria

    def find_server_messages_element(self) -> EditWrapper:
        application: Application = self._application_finder.find()
        return self._find_by_criteria(application, self._server_criteria)

    def _find_by_criteria(self, application: Application, criteria: ServerMessageElementSearchCriteria) -> EditWrapper:
        try:
            search_wnd: WindowSpecification = find_target_window(application, criteria.get_parent_auto_ids())
            if search_wnd is None:
                return None

            for c in search_wnd.children():
                selector:str = criteria.get_final_selector()
                if c.control_id() == selector or c.friendly_class_name() == selector:
                    return c

            return getattr(search_wnd, criteria.get_final_selector())
        except ElementNotFoundError:
            logging.exception('Error searching for element')
            return None

    def find_process_messages_element(self) -> EditWrapper:
        application: Application = self._application_finder.find()
        return self._find_by_criteria(application, self._process_criteria)
        