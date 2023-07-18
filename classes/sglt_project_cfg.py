import dataclasses
import functools
import json
from typing import Set

import pandas

import zzz_const as CONST
import zzz_enums as ENUM
from classes.exceptions import MyProgramException
from classes.subcampaign import Subcampaign
from zzz_ordersTools import get_channels_mapping_df, get_copy_indexes_df


def singleton(cls):
    instance = None

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper
@singleton
@dataclasses.dataclass
class SgltProjectCfg:
    supplier: ENUM.Supplier
    booking_quality: ENUM.BookingQuality
    schedule_type: ENUM.ScheduleType
    free_times_quality: ENUM.FreeTimesQuality
    do_export_debug_files: bool
    channel_mapping_df: pandas.DataFrame
    copy_indexes_df: pandas.DataFrame
    schedule_path: str
    schedule_info: str
    subcampaigns: Set[str]
    __instance = None

    def __init__(self):
        from classes.df_processor import get_df_processor
        self.supplier: ENUM.Supplier = ENUM.Supplier.POLSAT
        self.booking_quality: ENUM.BookingQuality = ENUM.BookingQuality.FUCKED_UP_DATES
        self.schedule_type: ENUM.ScheduleType = ENUM.ScheduleType.OK_4CHANNELS_1WANTED
        self.free_times_quality: ENUM.FreeTimesQuality = ENUM.FreeTimesQuality.OK
        self.do_export_debug_files: bool = True
        self.channel_mapping_df =  get_channels_mapping_df()
        self.copy_indexes_df = get_copy_indexes_df()
        self.schedule_path = CONST.get_path_schedule(self.schedule_type)
        self.schedule_info = get_df_processor( ENUM.DfProcessorType.SCHEDULE_INFO, self.schedule_path).get_df.iloc[0,0]
        if self.schedule_info == "":
            raise MyProgramException("Zjebana ramuwka, nie ma scheduel info")
        self.subcampaigns = self._get_subcampaigns_dict

    @property
    def _get_subcampaigns_dict(self) -> dict[Subcampaign]:
        shedule_info_json = json.loads(self.schedule_info)
        subcampaign_json = shedule_info_json["campaingNames"]
        subcampaigns = {}
        for subcampaigns_json in subcampaign_json:
            value = subcampaigns_json["value"]
            copy_name = subcampaigns_json["name"]
            length = subcampaigns_json["length"]
            subcampaign = Subcampaign(value, copy_name, length)
            subcampaigns[subcampaign.get_hash] = subcampaign
        return subcampaigns

    @property
    def get_subcampaign_hashes_set(self) -> set[str]:
        _set =  set(self.subcampaigns.keys())
        return _set