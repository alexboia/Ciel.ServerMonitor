import logging
from pywinauto import Application
from .application_search_criteria import ApplicationSearchCriteria

class ApplicationFinder:
    def __init__(self, criteria:ApplicationSearchCriteria):
        self._criteria = criteria
        self._current_application = None
        
    def find(self) -> Application:
        application: Application = None
        if self._current_application is not None:
            try:
                if self._current_application.is_process_running():
                    application = self._current_application
            except:
                logging.exception('Failed to detect if application process is running')

        if application is None:
            try:
                application = self._create_app()
                if self._criteria.is_regexp_title_search():
                    return application.connect(title_re=self._criteria.get_keyword(), visible_only=False) 
                elif self._criteria.is_exact_title_search():
                    return application.connect(title=self._criteria.get_keyword(), visible_only=False)
                else:
                    application = None
            except:
                logging.exception('Error occurred when searching for application')
                application = None

            self._current_application = application

        return application

    def _create_app(self) -> Application:
        return Application(backend='win32')

    def is_app_reachable(self) -> bool:
        return self.find() is not None