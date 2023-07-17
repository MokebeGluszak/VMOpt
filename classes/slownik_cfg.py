import dataclasses
from typing import Set, Dict

import pandas as pd

import zzz_enums as ENUM
from zzz_tools import get_mod_values_file_path, get_values_from_txt, setize


@dataclasses.dataclass
class SlownikCfg():
    slownik_type: ENUM.SlownikType
    org_column: str
    mod_column: str
    caption:str = "Zapodawaj słownik"



    @property
    def get_mod_values(self) -> Set[str]:
        file_path = get_mod_values_file_path(self.name)
        values = get_values_from_txt(file_path)
        mod_values = setize(values)
        return  mod_values

    @property
    def name(self):
        return self.slownik_type.value
    @property
    def get_existing_dict(path, column_org:str, column_mod:str) -> Dict[str, str]:
        dict: Dict[str, str] = {}
        df = pd.read_csv(path, sep=";", encoding="utf-8")

        for _, row in df.iterrows():
            value_org = row[column_org]
            value_mod = row[column_mod]
            # id, name, length = subcampaign_str.split("|")
            # subcampaign = Subcampaign(id, name, length)
            dict[value_org] = value_mod
        return dict

def get_slownik_cfg(SlownikType:ENUM.SlownikType):
    match SlownikType:
        case ENUM.SlownikType.CHANNELS:
            slownik_cfg = SlownikCfg(SlownikType, "channel_org", "channel")
        case ENUM.SlownikType.SUBCAMPAIGNS:
            slownik_cfg = SlownikCfg(SlownikType, "subcampaign_org", "subcampaign_hash")
        case ENUM.SlownikType.WOLNE_CZASY_LENGTHS:
            slownik_cfg = SlownikCfg(SlownikType, "length_org", "length")
        case _:
            raise NotImplementedError(f"SlownikType: {SlownikType} not implemented")

    return slownik_cfg