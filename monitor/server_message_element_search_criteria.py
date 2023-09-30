class ServerMessageElementSearchCriteria:
    def __init__(self, parent_auto_ids: list[str], final_selector: str) -> None:
        self._parent_auto_ids = parent_auto_ids
        self._final_selector = final_selector

    def get_parent_auto_ids(self) -> list[str]:
        return self._parent_auto_ids

    def get_final_selector(self) -> str:
        return self._final_selector