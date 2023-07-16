import json
import os
import re
from datetime import datetime
from typing import List, Dict

import pandas as pd
from openpyxl.compat.singleton import Singleton

import zzz_const as CONST
import zzz_enums as ENUM
import zzz_strings as STR
from classes.break_info import BreakInfo
from classes.exceptions import MyProgramException
from classes.merger import get_merger
from classes.schedule_break import ScheduleBreak
from classes.status_info import StatusInfo
from classes.timeband import Timeband
from classes.tv.channel import Channel
from classes.tv.channel_group import ChannelGroup
from classes.tv.supplier import Supplier
from zzz_tools import is_enum_value


def get_date_time_tvp(xDate: str, xHour: str, xMinute: str) -> datetime:
    if re.match("\d{4}-\d{2}-\d{2}$", xDate):
        date_safe = xDate
    elif re.match("\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$", xDate):
        date_safe = xDate.split(" ")[0]
    else:
        raise ValueError(f"Wrong date format: {xDate}")

    date_string = f"{date_safe} {xHour.zfill(2)}:{xMinute.zfill(2)}:00"
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    if not isinstance(dt, datetime):
        raise ValueError(f"Wrong date format: {xDate} {xHour} {xMinute}")
    return dt


def get_date_time_tvn(xDate: str, xTime: str) -> datetime:
    if re.match(r"^\d{4}-\d{2}-\d{2}$", xDate):
        date = datetime.strptime(xDate, "%Y-%m-%d")
    else:
        raise ValueError(f"Wrong date format: {xDate}")

    if re.match(r"^\d{2}:\d{2}:\d{2}$", xTime):
        time = datetime.strptime(xTime, "%H:%M").time()
    else:
        raise ValueError(f"Wrong time format: {xTime}")

    dt = datetime.combine(date.date(), time)

    if not isinstance(dt, datetime):
        raise ValueError(f"Wrong date format: {xDate} {xTime}")
    return dt


def get_date_time_polsat(xDate, xTime) -> datetime:
    dt = datetime.combine(xDate, xTime)

    if not isinstance(dt, datetime):
        raise ValueError(f"Wrong date format: {xDate} {xTime}")
    return dt


def get_suppliers(json_path: str) -> List[Supplier]:
    with open(json_path, "r") as f:
        data = json.load(f)

    suppliers = []

    for supplier_data in data["suppliers"]:
        channel_groups = []
        for group_data in supplier_data["channelGroups"]:
            channels = []
            for channel_data in group_data["channels"]:
                channel = Channel(channel_data["name"], channel_data["possibleNames"])
                channels.append(channel)
            group = ChannelGroup(group_data["name"], channels)
            channel_groups.append(group)
        supplier = Supplier(supplier_data["name"], channel_groups)
        suppliers.append(supplier)
    return suppliers


def get_channels_mapping_df() -> pd.DataFrame:
    with open(CONST.PATH_JSON_CHANNELS, "r") as file:
        json_channels = json.load(file)

    suppliers = []
    channel_groups = []
    channels = []
    possible_names = []

    for supplier in json_channels["supplier"]:
        if not is_enum_value(supplier["name"], ENUM.Supplier):
            raise MyProgramException(f"Wrong supplier: {supplier}")
        for channel_group in supplier["channelGroup"]:
            for channel in channel_group["channel"]:
                for name in channel["channelPossibleName"]:
                    suppliers.append(supplier["name"])
                    channel_groups.append(channel_group["name"])
                    channels.append(channel["name"])
                    possible_names.append(name)

    # Create a DataFrame
    df = pd.DataFrame(
        {
            "supplier": suppliers,
            "channelGroup": channel_groups,
            "channel": channels,
            "channelPossibleName": possible_names,
        }
    )
    return df


class SgltChannelMapping(metaclass=Singleton):
    df: pd.DataFrame

    @classmethod
    @property
    def get_df(cls) -> pd.DataFrame:
        if not hasattr(cls, "df") or (hasattr(cls, "df") and cls.df is None):
            cls.df = get_channels_mapping_df()
        return cls.df

    @classmethod
    @property
    def get_channel_supplier_dict(cls) -> Dict[str, str]:
        if not hasattr(cls, "channel_supplier_dict") or (hasattr(cls, "channel_supplier_dict") and cls.channel_supplier_dict is None):
            cls.channel_supplier_dict = cls.get_df.set_index("channel")["supplier"].to_dict()
        return cls.channel_supplier_dict

def get_copy_indexes_df() -> pd.DataFrame:
    json_copyLengths_path = CONST.PATH_JSON_COPY_INDEXES

    with open(json_copyLengths_path, "r") as f:
        data = json.load(f)

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data["CopyLengths"])
    return df


def get_booking_file_path(supplier: ENUM.Supplier, booking_quality: ENUM.BookingQuality) -> str:
    folder = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source"
    case = supplier.value + booking_quality.value
    if case == ENUM.Supplier.POLSAT.value + ENUM.BookingQuality.OK.value:
        file = "2 booking polsat no pato2023-04-22 1052.xlsx"
    elif case == ENUM.Supplier.POLSAT.value + ENUM.BookingQuality.ABSENT_CHANNELS.value:
        file = "2 booking polsat no pato2023-04-22 1052 -brakujące stacje.xlsx"
    elif case == ENUM.Supplier.POLSAT.value + ENUM.BookingQuality.ILLEGAL_CHANNELS.value:
        file = "2 booking polsat no pato2023-04-22 1052 -zjebane stacje.xlsx"
    elif case == ENUM.Supplier.POLSAT.value + ENUM.BookingQuality.FUCKED_UP_DATES.value:
        file = "2 booking polsat no pato2023-04-22 1052 - zjebane daty.xlsx"
    else:
        raise MyProgramException(f"Wrong supplier: {supplier} / booking_quality: {booking_quality}")
    # elif supplier == GluSupplier.TVN:
    #     file = "2 booking 2022-10-06 114034 TVN no pato.txt"
    # elif Supplier == GluSupplier.TVP:
    #     file = "2 booking 2022-10-06 113747 TVP 1z2.xls"
    return os.path.join(folder, file)

def get_free_times_folder_path(supplier: ENUM.Supplier, free_times_quality: ENUM.FreeTimesQuality) -> str:
    folder = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\zrobić porządki"

    case = supplier.value + free_times_quality.value
    if case == ENUM.Supplier.POLSAT.value + ENUM.FreeTimesQuality.OK.value:
        subfolder = "7. FreeTimesPolsat"
    else:
        raise MyProgramException(f"Wrong supplier: {supplier} / booking_quality: {free_times_quality}")
    # elif supplier == GluSupplier.TVN:
    #     file = "2 booking 2022-10-06 114034 TVN no pato.txt"
    # elif Supplier == GluSupplier.TVP:
    #     file = "2 booking 2022-10-06 113747 TVP 1z2.xls"
    return os.path.join(folder, subfolder)


def check_time_space_consistency(df_booking: pd.DataFrame, df_schedule: pd.DataFrame):
    get_merger(
        "check_time_space_consistency",
        df_booking,
        df_schedule,
        "channel",
        "channel",
        exception_type_unjoined=ENUM.ExceptionType.MERGER_ABSENT_CHANNELS,
    ).return_merged_df()

    min_date_booking = df_booking["dateTime"].min()
    max_date_booking = df_booking["dateTime"].max()
    min_date_schedule = df_schedule["dateTime"].min()
    max_date_schedule = df_schedule["dateTime"].max()

    dates_ok: bool = False
    if max_date_booking <= max_date_schedule:
        if min_date_booking >= min_date_schedule:
            dates_ok = True

    if not dates_ok:
        raise MyProgramException(
            f"Dates are not consistent:\n "
            f"Booking: {min_date_booking} to  {max_date_booking} \n "
            f"Schedule: {min_date_schedule} to {max_date_schedule}"
        )


def get_empty_timeband() -> Timeband:
    timeband = Timeband(STR.IRELEVANT)
    return timeband


def get_empty_break_info() -> BreakInfo:
    break_info = BreakInfo(0, CONST.FAKE_DATE, CONST.FAKE_INT, STR.IRELEVANT)
    return break_info


def get_empty_schedule_break(break_info: BreakInfo) -> ScheduleBreak:
    schedule_break = ScheduleBreak(
        break_info,
        get_empty_status_info(),
        STR.IRELEVANT,
        STR.IRELEVANT,
        STR.IRELEVANT,
        STR.IRELEVANT,
        STR.IRELEVANT,
        999,
        0,
        0,
        0,
        0,
        0,
        50,
    )
    return schedule_break


def get_empty_status_info() -> StatusInfo:
    status_info: StatusInfo = StatusInfo(subcampaign_id=-1, origin=ENUM.Origin.NotWanted, is_booked=False)
    return status_info


def get_schedule_break_from_channel_break(break_info: BreakInfo) -> ScheduleBreak:
    schedule_break = ScheduleBreak(
        break_info,
        get_empty_status_info(),
        STR.IRELEVANT,
        STR.IRELEVANT,
        STR.ADDED_BY_STATION,
        STR.UNKNOWN,
        STR.UNKNOWN,
        999,
        STR.BOOKEDNESS_NOT_BOOKED,
        0,
        0,
        0,
        0,
        0,
        50,
    )
    return schedule_break


def get_subcampaigns_dict(copiesOrg: List[str], copies: List[str]) -> Dict[str, str]:
    existing_dict: Dict[str, str]
