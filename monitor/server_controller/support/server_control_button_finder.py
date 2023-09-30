import logging
from pywinauto import Application, WindowSpecification
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.controls.win32_controls import ButtonWrapper

from ...helper.ui import find_target_window
from ...application_finder import ApplicationFinder
from .server_control_button_search_criteria import ServerControlButtonSearchCriteria

class ServerControlButtonFinder:
    def __init__(self, application_finder:ApplicationFinder, criteria:ServerControlButtonSearchCriteria ) -> None:
        self._application_finder = application_finder
        self._criteria = criteria

    def find_start_button(self) -> ButtonWrapper:
        application: Application = self._get_application()
        if application is not None:
            return self._find_button(application, self._criteria.get_btn_start_selector())
        else:
            return None

    def _get_application(self) -> Application:
        try:
            return self._application_finder.find()
        except:
            logging.exception('Error retrieving application')
            return None

    def _find_button(self, application: Application, button_selector: str) -> ButtonWrapper:
        try:
            search_wnd: WindowSpecification = find_target_window(application, self._criteria.get_parent_auto_ids())
            for c in search_wnd.children():
                if c.control_id() == button_selector or c.friendly_class_name() == button_selector or c.automation_id() == button_selector:
                    return c

            #TODO: check if button
            return getattr(search_wnd, button_selector)
        except ElementNotFoundError:
            logging.exception('Error searching for button element')
            return None

    def find_stop_button(self) -> ButtonWrapper:
        application: Application = self._get_application()
        if application is not None:
            return self._find_button(application, self._criteria.get_btn_stop_selector())
        else:
            return None