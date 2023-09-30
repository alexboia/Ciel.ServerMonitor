import os
import sys
import shutil
import logging

from ..helper.file_hasher import FileHash
from .assets_replacer_options import AssetsReplacerOptions

CIEL_ENT_ASSET_FILE_NAME = 'Ciel.Entities.dll'

class AssetsReplacer:
    def __init__(self, options: AssetsReplacerOptions) -> None:
        self._hasher = FileHash()
        self._options = options

    def replace_assets(self) -> None:
        self._replace_asset(CIEL_ENT_ASSET_FILE_NAME)

    def _replace_asset(self, file_name:str) -> None:
        try:
           self._do_replace_asset(file_name)
        except:
            logging.exception('Error procesing asset replacement')

    def _do_replace_asset(self, file_name:str) -> None:
        original_file_path:str = self._get_original_asset_file_path(file_name)
        backup_file_path:str = self._get_backup_asset_file_path(file_name)
        replacement_file_path:str = self._get_replacement_asset_file_path(file_name)

        if os.path.exists(original_file_path):
            source_hash = self._compute_file_hash(original_file_path)
            if source_hash != self._options.get_ciel_ent_file_hash():
                shutil.copy(original_file_path, backup_file_path)
        else:
            logging.debug('Original file not found. File not backed up')

        if os.path.exists(replacement_file_path):
            shutil.copy(replacement_file_path, original_file_path)
        else:
            logging.debug('Replacement file not found')

    def _get_original_asset_file_path(self, file_name:str) -> str:
        return os.path.join(self._options.get_ciel_dir(), file_name)

    def _get_backup_asset_file_path(self, file_name:str) -> str:
        return os.path.join(self._options.get_assets_backup_dir(), file_name)

    def _get_replacement_asset_file_path(self, file_name:str) -> str:
        return os.path.join(self._options.get_assets_bin_dir(), file_name)

    def _compute_file_hash(self, file_path:str) -> str:
        return self._hasher.compute_hash(file_path)

    def restore_assets(self) -> None:
        self._restore_asset(CIEL_ENT_ASSET_FILE_NAME)

    def _restore_asset(self, file_name:str) -> None:
        try:
            self._do_restore_asset(file_name)
        except:
            logging.exception('Error processing asset restore')

    def _do_restore_asset(self) -> None:
        original_file_path:str = self._get_original_asset_file_path(file_name)
        backup_file_path:str = self._get_backup_asset_file_path(file_name)

        if os.path.exists(backup_file_path):
            shutil.copy(backup_file_path, original_file_path)
            os.remove(backup_file_path)
        else:
            logging.debug('Backup file not found. File not restored')
