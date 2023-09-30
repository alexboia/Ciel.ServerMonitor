class ServerMessageMonitorOptions:
    def __init__(self, poll_seconds:int) -> None:
        self._poll_seconds = poll_seconds

    def get_poll_seconds(self) -> int:
        return self._poll_seconds