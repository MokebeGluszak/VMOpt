import dataclasses
from typing import Dict, List

import pandas as pd

import zzz_const as CONST
import zzz_enums as enum
from classes.df_processor import get_df_processor
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.merger import get_merger
from classes.schedule_break import ScheduleBreak
from classes.sglt_project_cfg import SgltProjectCfg
from classes.status_info import StatusInfo
# from classes.timeband import Timeband
from classes.wantedness_info import WantednessInfo
from zzz_tools import check_cannon_columns, getTimebandId, get_substring_between_parentheses, export_df, Collection


@dataclasses.dataclass
class Schedule(iDataFrameable):
    schedule_type: enum.ScheduleType
    df: pd.DataFrame

    def load_breaks(self):
        self.schedule_breaks = get_schedule_breaks(self.df)

    def to_dataframe(self, export_format: enum.ExportFormat):
        x: ScheduleBreak
        # print (type(self.schedule_breaks.values)

        df = pd.DataFrame(data=[x.serialize(export_format) for x in self.schedule_breaks.values()])
        df["scheduleInfo"] = ""
        # df.loc[0, "scheduleInfo"] = self.schedule_info  # Assign the string value to the first row of the new column

        return df

    def export(self) -> str:
        df = self.to_dataframe(enum.ExportFormat.ScheduleBreak_minerwa)
        export_path = export_df(df, "schedule - minerwa", file_type=enum.FileType.CSV)
        return export_path


def get_wantedness_info_from_row(wantedness) -> WantednessInfo:
    is_wanted: bool
    subcampaign: int
    origin: enum.Origin

    if wantedness == "NotWanted":
        is_wanted = False
        subcampaign = -1
        origin = enum.Origin.NotWanted
    elif wantedness.startswith("Wanted"):
        is_wanted = True
        sub_string = get_substring_between_parentheses(wantedness)
        subcampaign = int(get_substring_between_parentheses(sub_string))
        origin_str = sub_string.split(",")[0].strip()
        origin = enum.Origin.get_from_str(origin_str)
    else:
        raise MyProgramException(f"Wrong wantedness: {wantedness}")

    wantedness_info: WantednessInfo = WantednessInfo(is_wanted=is_wanted, subcampaign=subcampaign, origin=origin)
    return wantedness_info


def get_is_booked(boookedness: str) -> bool:
    is_booked: bool
    if boookedness == "Booked":
        is_booked = True
    elif boookedness == "NotBooked":
        is_booked = False
    else:
        raise MyProgramException(f"Wrong bookedness: {boookedness}")
    return is_booked


def get_schedule_breaks(df: pd.DataFrame) -> Collection:
    breaks:Collection = Collection()
    for index, row in df.iterrows():
        schedule_break: ScheduleBreak = ScheduleBreak(**row.to_dict())
        breaks.add(schedule_break, schedule_break.blockId)

    return breaks


def get_schedule(schedule_type: enum.ScheduleType) -> Schedule:

    df_schedule = get_df_processor(enum.DfProcessorType.SCHEDULE, schedule_type.value).get_df



    schedule = Schedule(schedule_type, df_schedule)
    return schedule
