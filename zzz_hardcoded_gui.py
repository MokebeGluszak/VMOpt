from typing import Dict, Set, List

import pandas as pd

import zzz_const as CONST
from classes.subcampaign import Subcampaign


def get_existing_subcampaign_dict() -> Dict[str, Subcampaign]:
    subcampaigns_dict: Dict[str, Subcampaign] = {}
    subcampaigns_df = pd.read_csv(CONST.PATH_DICT_SUBCAMPAIGNS, sep=";", encoding="utf-8")

    for _, row in subcampaigns_df.iterrows():
        subcampaign_org = row["subcampaign_org"]
        subcampaign_str = row["subcampaign_hash"]
        id, name, length = subcampaign_str.split("|")
        subcampaign = Subcampaign(id, name, length)
        subcampaigns_dict[subcampaign_org] = subcampaign
    return subcampaigns_dict


def get_subcampaigns_dict(
    subcampaign_orgs_booking: Set[str], subcampaigns_schedule: List[Subcampaign]
) -> Dict[str, Subcampaign]:
    # Hardcoded user interaction
    existing_dict = get_existing_subcampaign_dict()
    subcampaign_existing_dict: Subcampaign
    subcampaign_org_existing_dict: str
    subcampaign_hashes_schedule: List[str] = [subcampaign.get_hash for subcampaign in subcampaigns_schedule]
    valid_dict = {}

    # mg2023-07-13 jeżeli hasza z istniejącego dicta nie ma w schedulu to zmieniłą się lista subcampaignów, albo świadomie albo się zjebało, anyłej pozwalamy na to, tylko dla bezpieczeńśtwa przesłownikowac
    for subcampaign_org_existing_dict, subcampaign_existing_dict in existing_dict.items():
        if subcampaign_existing_dict.get_hash in subcampaign_hashes_schedule:
            valid_dict[subcampaign_org_existing_dict] = subcampaign_existing_dict
        else:
            pass

    # robimy listę subcampaignów_org istniejących w bukingu a nie w dict
    subcampaigns_org_booking_not_in_dict = subcampaign_orgs_booking - set(valid_dict.keys())
    # teraz pokazujesz GUI i każesz przypisać subcampaigns_org_booking_not_in_dict do haszów z listy subcampaign_hashes_schedule i dodajesz do valid_dict
    ####zahardkodowane to co ma się robić w gui
    if len(subcampaigns_org_booking_not_in_dict) == 1:
        subcampaign_org_to_add = list(subcampaigns_org_booking_not_in_dict)[0]
        valid_dict[subcampaign_org_to_add] = subcampaigns_schedule[0]
    else:
        raise NotImplementedError
    ####

    if not subcampaign_orgs_booking.issubset(valid_dict.keys()):
        raise NotImplementedError("po wykonaniu tej funkcji każdy subcampaign_org z bookingu musi być w valid_dict")
    return valid_dict
