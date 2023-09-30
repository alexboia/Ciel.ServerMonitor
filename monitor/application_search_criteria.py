class ApplicationSearchCriteria:
    def __init__(self, type:str, keyword:str):
        self._type = type
        self._keyword = keyword
        
    def get_type(self) -> str:
        return self._type
        
    def get_keyword(self) -> str:
        return self._keyword
        
    def is_exact_title_search(self) -> bool:
        return self._type == 'exact_title'
        
    def is_regexp_title_search(self) -> bool:
        return self._type == 'regexp_title'