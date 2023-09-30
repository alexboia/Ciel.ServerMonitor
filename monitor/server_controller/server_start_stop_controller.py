import logging
from pywinauto.controls.win32_controls import ButtonWrapper
from pywinauto import win32defines

from ..application_finder import ApplicationFinder
from .support.server_control_button_search_criteria import ServerControlButtonSearchCriteria
from .support.server_control_button_finder import ServerControlButtonFinder
from .server_application_controller_options import ServerApplicationControllerOptions

class ServerStartStopController:
    def __init__(self, application_finder:ApplicationFinder, options: ServerApplicationControllerOptions) -> None:
        self._button_finder = ServerControlButtonFinder(application_finder, 
            ServerControlButtonSearchCriteria(options.get_parent_auto_ids(), 
                options.get_btn_start_selector(), 
                options.get_btn_stop_selector()))

    def start(self) -> bool:
        button: ButtonWrapper = self._button_finder.find_start_button()
        if button is not None:
            return self._click(button)
        else:
            logging.debug('Start button element not found')
            return False

    def _click(self, button: ButtonWrapper) -> bool:
        if button.is_enabled():
            try:
                button.click(button='left')
            except:
                logging.exception('Error performing button click. Attempting direct')
                try:
                    button.send_message(win32defines.BM_CLICK, 0, 0)
                    return True
                except:
                    logging.exception('Error performing performing direct button click')
        else:
            logging.debug('Button not enabled')

        return False

    def stop(self) -> bool:
        button: ButtonWrapper = self._button_finder.find_stop_button()
        if button is not None:
            return self._click(button)
        else:
            logging.debug('Stop button element not found')
            return False

    def is_started(self) -> bool:
        button: ButtonWrapper = self._button_finder.find_start_button()
        return button is not None and not button.is_enabled()