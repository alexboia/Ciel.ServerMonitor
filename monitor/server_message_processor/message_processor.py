from abc import ABC, abstractmethod
from pywinauto.controls.win32_controls import EditWrapper
from .processing_result import ProcessingResult

class MessageProcessor(ABC):
    @abstractmethod
    def process_text_lines(target_element: EditWrapper, prev_result: ProcessingResult) -> ProcessingResult:
        pass