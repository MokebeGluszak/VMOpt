import dataclasses
from typing import Set, Dict

import pandas as pd

import zzz_const as CONST
import zzz_enums as ENUM
from classes.file import File
from classes.folder import Folder, get_folder
from classes.sglt_project_cfg import SgltProjectCfg
from zzz_tools import build_path


@dataclasses.dataclass
class SlownikCfg:
    slownik_type: ENUM.SlownikType
    org_column: str
    alias_column: str
    caption: str = "Zapodawaj słownik"

    @property
    def get_aliases(self) -> Set[str]:
        cfg = SgltProjectCfg()
        match self.slownik_type:
            case ENUM.SlownikType.SUBCAMPAIGNS:
                raise NotImplementedError
                # aliases = cfg.get_subcampaign_hashes_set
            case ENUM.SlownikType.CHANNELS:
                aliases = set(cfg.channel_mapping_df["channel"].tolist())
                pass
            case ENUM.SlownikType.WOLNE_CZASY_LENGTHS:
                aliases = set(cfg.copy_indexes_df["CopyLength"].tolist())
                pass
            case _:
                raise NotImplementedError (f"SlownikType: {self.slownik_type} not implemented")
        return aliases

    @property
    def name(self):
        return self.slownik_type.value

    @property
    def get_aliases_folder(self) -> Folder:
        aliases_folder = get_folder(CONST.PATH_SLOWNIKI_ALIASES_FOLDER)
        return aliases_folder

    @property
    def get_existing_dict_folder(self) -> Folder:
        existing_dict_folder = get_folder(CONST.PATH_SLOWNIKI_EXISTING_DICTS_FOLDER)
        return existing_dict_folder

    @property
    def get_aliases_file_path(self) -> str:
        folder = self.get_aliases_folder
        file_name = "aliases " + self.name + ".txt"
        file_path = build_path(folder, file_name)
        return file_path

    @property
    def get_existing_dict_file_path(self) -> str:
        folder = self.get_existing_dict_folder
        file_name = "existing dict " + self.name + ".csv"
        file_path = build_path(folder, file_name)
        return file_path

    @property
    def get_existing_dict(self) -> Dict[str, str]:
        dict: Dict[str, str] = {}
        path = self.get_existing_dict_file_path
        df = pd.read_csv(path, sep=";", encoding="utf-8")

        for _, row in df.iterrows():
            value_org = row[self.org_column]
            alias = row[self.alias_column]
            # id, name, length = subcampaign_str.split("|")
            # subcampaign = Subcampaign(id, name, length)
            dict[value_org] = alias
        return dict

    def print_aliases(self) -> File:
        raise NotImplementedError
        # file_path = get_mod_values_file_path(slownik_name)
        # print_values_to_txt(mod_values, file_path)


def get_slownik_cfg(SlownikType: ENUM.SlownikType):
    match SlownikType:
        case ENUM.SlownikType.CHANNELS:
            slownik_cfg = SlownikCfg(SlownikType, "channel_org", "channel")
        case ENUM.SlownikType.SUBCAMPAIGNS:
            slownik_cfg = SlownikCfg(SlownikType, "subcampaign_org", "subcampaign_hash")
        case ENUM.SlownikType.WOLNE_CZASY_LENGTHS:
            slownik_cfg = SlownikCfg(SlownikType, "file_name", "length")
        case _:
            raise NotImplementedError(f"SlownikType: {SlownikType} not implemented")

    return slownik_cfg
