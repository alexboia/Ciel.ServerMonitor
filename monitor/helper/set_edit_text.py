import ctypes
import locale
import six

from pywinauto import win32defines
from pywinauto.controls.win32_controls import EditWrapper

def set_edit_text_direct(target_element: EditWrapper, text: str) -> None:
    if six.PY3:
        send_text = text
    else:
        send_text = text.encode(locale.getpreferredencoding())

    send_buffer = ctypes.create_unicode_buffer(send_text, size=len(send_text) + 1)
    target_element.send_message(win32defines.WM_SETTEXT, 0, ctypes.byref(send_buffer))