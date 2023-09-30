class ServerControlButtonSearchCriteria:
    def __init__(self, parent_auto_ids: list[str], btn_start_selector: str, btn_stop_selector: str) -> None:
        self._parent_auto_ids = parent_auto_ids
        self._btn_start_selector = btn_start_selector
        self._btn_stop_selector = btn_stop_selector

    def get_parent_auto_ids(self) -> str:
        return self._parent_auto_ids

    def get_btn_start_selector(self) -> str:
        return self._btn_start_selector

    def get_btn_stop_selector(self) -> str:
        return self._btn_stop_selector

