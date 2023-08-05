from dataclasses import dataclass
from typing import Dict, Set

import pandas as pd

import zzz_enums as ENUM
import zzz_hardcoded_gui as HGUI
from classes.slownik_cfg import get_slownik_cfg
from zzz_tools import merge_dicts


@dataclass
class Slownik:
    orgs: Set[str]
    aliases: Set[str]
    dict: Dict[str, str]


def get_slownik(slownik_cfg_type: ENUM.SlownikType, df: pd.DataFrame) -> Slownik:
    slownik_cfg = get_slownik_cfg(slownik_cfg_type)

    orgs_set = set(df[slownik_cfg.org_column].unique())
    aliases_set = slownik_cfg.get_aliases

    existing_dict = slownik_cfg.get_existing_dict

    # robimy listę subcampaignów_org istniejących w bukingu a nie w dict
    orgs_to_slownikize_set = orgs_set - set(existing_dict.keys())
    # teraz pokazujesz GUI i każesz przypisać subcampaigns_org_booking_not_in_dict do haszów z listy subcampaign_hashes_schedule i dodajesz do valid_dict
    ####zahardkodowane to co ma się robić w gui
    complement_dict = HGUI.get_complement_dict("Przesłownikuj chuju", orgs_to_slownikize_set, aliases_set)

    processed_dict = merge_dicts(existing_dict, complement_dict)

    if not orgs_set.issubset(processed_dict.keys()):
        raise NotImplementedError("po wykonaniu tej funkcji każdy subcampaign_org z bookingu musi być w valid_dict")
    else:
        slownik = Slownik(orgs_set, aliases_set, processed_dict)
    return slownik
