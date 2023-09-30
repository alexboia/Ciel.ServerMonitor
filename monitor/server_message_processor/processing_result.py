class ProcessingResult:
    def __init__(self, discarded_txt: str, remaining_txt: str) -> None:
        self._discarded_txt = discarded_txt
        self._remaining_txt = remaining_txt

    def get_discarded_txt(self) -> str:
        return self._discarded_txt

    def get_remaining_txt(self) -> str:
        return self._remaining_txt