class TrimMessageProcessorOptions:
    def __init__(self, max_line_count:int, leave_line_count:int):
        self._max_line_count = max_line_count
        self._leave_line_count = leave_line_count

    def get_max_line_count(self) -> int:
        return self._max_line_count

    def get_leave_line_count(self) -> int:
        return self._leave_line_count