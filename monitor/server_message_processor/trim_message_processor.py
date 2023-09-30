import logging
from pywinauto.controls.win32_controls import EditWrapper
from .trim_message_processor_options import TrimMessageProcessorOptions
from .message_processor import MessageProcessor
from .processing_result import ProcessingResult
from ..helper.set_edit_text import set_edit_text_direct

class TrimMessageProcessor(MessageProcessor):
    def __init__(self, options:TrimMessageProcessorOptions) -> None:
        super().__init__()
        self._options = options

    def process_text_lines(self, target_element: EditWrapper, prev_result: ProcessingResult) -> ProcessingResult:       
        def __trim_line(l:str)->str:
            return l.rstrip().replace('\n', '').replace('\r', '')

        result:ProcessingResult = None
        line_count:int = target_element.line_count()
        
        if line_count >= self._options.get_max_line_count():
            all_lines:list[str] = target_element.texts()

            discard_line_count:int = (line_count - self._options.get_leave_line_count())
            text_to_discard:str = '\r\n'.join(list(map(__trim_line, all_lines[0:discard_line_count])))

            keep_line_count:int = self._options.get_leave_line_count()
            text_to_keep:str = '\r\n'.join(list(map(__trim_line, all_lines[-keep_line_count:])))

            try:
                target_element.set_edit_text(text_to_keep)
                result = ProcessingResult(text_to_discard, text_to_keep)
                logging.debug('Successfully set text using .set_edit_text()')
            except:
                logging.exception('Error setting text via .set_edit_text(). Attempting direct...')
                set_edit_text_direct(target_element, '')
                result = ProcessingResult(text_to_discard + text_to_keep, '')
                logging.debug('Successfully set text using direct call')
        else:
            result = ProcessingResult('', target_element.text_block())

        return result