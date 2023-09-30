import hashlib
from pathlib import Path
import sys

class FileHash:
    def compute_hash(self, file_path:str) -> str:
        file_pointer: Path = Path(file_path)
        if file_pointer.exists():
            return hashlib.sha1(file_pointer.read_bytes()).hexdigest().lower()
        else:
            return None

    def check_hash(self, file_path:str, test_hash:str) -> bool:
        computed_hash:str = self.compute_hash(file_path)
        return computed_hash == test_hash