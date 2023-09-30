import logging
from pywinauto import Application, WindowSpecification

def find_target_window(application: Application, search_auto_ids: list[str]) -> WindowSpecification:
    try:
        top_wnd: WindowSpecification = application.top_window()
        search_wnd: WindowSpecification = top_wnd

        for s_auto_id in search_auto_ids:
            perform_select:bool = False
            if '.select' in s_auto_id:
                perform_select = True
                s_auto_id = s_auto_id.replace('.select', '')

            search_wnd = search_wnd.child_window(auto_id=s_auto_id, enabled_only=False, visible_only=False)
            if perform_select:
                try:
                    search_wnd.set_focus()
                except:
                    logging.exception('Error trying to set focus on search window.')
                    try:
                        top_wnd.restore.maximize()
                    except:
                        logging.exception('Error trying maximize top window.')

            return search_wnd
    except:
        logging.exception('Error searching for target window')
        return None