from pywinauto.controls.win32_controls import EditWrapper
from ..helper.file_appender import FileAppender
from .log_message_processor_options import LogMessageProcessorOptions
from .message_processor import MessageProcessor
from .processing_result import ProcessingResult

class LogMessageProcessor(MessageProcessor):
    def __init__(self, options: LogMessageProcessorOptions) -> None:
        super().__init__()
        self._options = options
        self._appender = FileAppender(options.get_destination_file(), options.get_rotate_size_bytes())

    def process_text_lines(self, target_element: EditWrapper, prev_result: ProcessingResult) -> ProcessingResult:
        txt_to_append:str = None
        result:ProcessingResult = None

        if prev_result is not None:
            result = prev_result
            txt_to_append = prev_result.get_discarded_txt()
        else:
            all_text = target_element.text_block()
            result = ProcessingResult('', all_text)
            txt_to_append = all_text

        self._appender.append_text(txt_to_append)
        return result

