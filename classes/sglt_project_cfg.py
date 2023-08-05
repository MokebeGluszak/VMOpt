import dataclasses
import functools
import json
from typing import Set

import pandas

import zzz_const as CONST
import zzz_enums as ENUM
from classes.exceptions import MyProgramException
from zzz_tools import singleton





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
        if self.schedule_info == "":
            raise MyProgramException("Zjebana ramuwka, nie ma scheduel info")