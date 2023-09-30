class LogMessageProcessorOptions:
    def __init__(self, destination_file: str, rotate_size_bytes:int) -> None:
        self._destination_file = destination_file
        self._rotate_size_bytes = rotate_size_bytes

    def get_destination_file(self) -> str:
        return self._destination_file

    def get_rotate_size_bytes(self) -> int:
        return self._rotate_size_bytes