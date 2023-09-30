class AssetsReplacerOptions:
    def __init__(self, ciel_dir:str, assets_bin_dir:str, assets_backup_dir: str, ciel_ent_file_hash:str) -> None:
        self._assets_bin_dir = assets_bin_dir
        self._asset_backup_dir = assets_backup_dir
        self._ciel_ent_file_hash = ciel_ent_file_hash
        self._ciel_dir = ciel_dir

    def get_assets_bin_dir(self) -> str:
        return self._assets_bin_dir

    def get_assets_backup_dir(self) -> str:
        return self._asset_backup_dir

    def get_ciel_ent_file_hash(self) -> str:
        return self._ciel_ent_file_hash

    def get_ciel_dir(self) -> str:
        return self._ciel_ent_file_hash