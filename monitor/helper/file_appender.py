import math
import os
import datetime
import re
from io import TextIOWrapper

PLACEHOLDER_DATE = '$datetime$'
PLACEHOLDER_ROTATION_INDEX = '$rindex$'

DEFAULT_SIZE_BYTES:int = 5242880
DEFAULT_ENCODING:str = 'utf-8'

class FileAppender:
    def __init__(self, file_path:str, max_size_bytes:int = DEFAULT_SIZE_BYTES, encoding:str = DEFAULT_ENCODING) -> None:
        self._file_path = file_path
        self._max_size_bytes = max_size_bytes
        self._encoding = encoding

    def append_text(self, txt_to_append:str) -> None:
        file_pointer:TextIOWrapper = None

        try:
            if txt_to_append is not None and len(txt_to_append) > 0:
                self._ensure_location()
                file_path:str = self._determine_actual_file_path()

                if not self._file_exists(file_path):
                    file_pointer = open(file_path, 'w', encoding=self._encoding, newline='')
                else:
                    file_pointer = open(file_path, 'a', encoding=self._encoding, newline='')

                file_pointer.write(txt_to_append)
                file_pointer.flush()
        finally:
            if file_pointer is not None:
                file_pointer.close()

    def _ensure_location(self) -> None:
        dir_path = self._get_dir_path()
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

    def _determine_actual_file_path(self) -> str:
        r_index:int = self._determine_latest_log_file_rotation_index()
        if r_index == 0:
            r_index += 1

        actual_file_path:str = self._get_file_path_for_roration_index(r_index)
        actual_file_size:int = self._get_file_size_bytes(actual_file_path)

        if actual_file_size >= self._max_size_bytes:
            return self._get_file_path_for_roration_index(r_index + 1)
        else:
            return actual_file_path

    def _determine_latest_log_file_rotation_index(self) -> int:
        dir_path:str = self._get_dir_path()
        dir_files:list[str] = os.listdir(dir_path) or []
        
        max_r_index: int = 0
        search_file_name_regex:str = self._build_search_file_regex()

        for f in dir_files:
            match = re.search(search_file_name_regex, f)
            if match is not None:
                r_index:str = match.group('rindex')
                if r_index:
                    r_index_int: int = int(r_index)
                    max_r_index = max(max_r_index, r_index_int)

        return max_r_index


    def _build_search_file_regex(self) -> str:
        file_name:str = self._get_raw_file_name_for_current_date()
        search_file_name_regex:str = file_name.replace(PLACEHOLDER_ROTATION_INDEX, 
            '(?P<rindex>[0-9]{4})')

        search_file_name_regex = search_file_name_regex.replace('.log', 
            '(\S+)log')
        search_file_name_regex = search_file_name_regex.replace('.txt', 
            '(\S+)txt')
        search_file_name_regex = search_file_name_regex.replace('.dat', 
            '(\S+)dat')

        return search_file_name_regex


    def _get_current_date_identifier(self) -> str:
        return datetime.datetime.now().strftime("%Y%m%d")

    def _get_file_path_for_roration_index(self, r_index) -> str:
        file_name:str = self._get_raw_file_name_for_current_date()
        padded_r_index:str = str(r_index).zfill(4)
        actual_file_name:str = file_name.replace(PLACEHOLDER_ROTATION_INDEX, padded_r_index)
        return os.path.join(self._get_dir_path(), actual_file_name)

    def _get_raw_file_name_for_current_date(self) -> str:
        file_name:str = self._get_raw_file_name()
        return file_name.replace(PLACEHOLDER_DATE, self._get_current_date_identifier())

    def _get_raw_file_name(self) -> str:
        return os.path.basename(self._file_path)

    def _get_dir_path(self) -> str:
        return os.path.dirname(self._file_path)

    def _get_file_size_bytes(self, file_path:str) -> int:
        if not self._file_exists(file_path):
            return 0

        file_stat = os.stat(file_path)
        return file_stat.st_size

    def _file_exists(self, file_path:str) -> bool:
        return os.path.isfile(file_path)
