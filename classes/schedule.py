import dataclasses
from typing import Dict, List

import pandas as pd

import zzz_const as CONST
import zzz_enums as enum
from classes.df_processor import get_df_processor
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.log import log_header, log
from classes.merger import get_merger
from classes.optimisation_def import OptimisationDef
from classes.quantity_constraint import QuantityConstraint
from classes.schedule_break import ScheduleBreak
from classes.status_info import StatusInfo
from classes.timeband import Timeband
# from classes.timeband import Timeband
from classes.wantedness_info import WantednessInfo
from zzz_tools import check_cannon_columns, getTimebandId, get_substring_between_parentheses, export_df, Collection


@dataclasses.dataclass
class Schedule(iDataFrameable):
    schedule_path: str
    df_org: pd.DataFrame
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

    def filter_disallowed_items(self, optimisation_items:List[QuantityConstraint]):
        log_header("Processing disallowed items")
        count_start: int = len(self.df)
        for optimisation_item in optimisation_items:
            if not optimisation_item.allowed:
                count_before: int = len(self.df)
                self.df = self.df[self.df[optimisation_item.type.value] != optimisation_item.name]
                count_after: int = len(self.df)
                log( f"Removed {count_before - count_after} {optimisation_item.type} {optimisation_item.name} from schedule")
        log (f"\nTotal removed by disallowed items:  {count_start - count_after} from {count_start} blocks")


    def filter_banned_blocks(self,  banned_blocks: list[str]):
        log_header("Filtering banned blocks")
        count_before = len(self.df)
        self.df = self.df[~self.df['blockId'].isin(banned_blocks)]
        count_after = len(self.df)
        log(f"Removed {count_before - count_after} banned blocks from {count_before}")


    def filter_0(self):
        log_header("Filtering 0 grp")
        count_before = len(self.df)
        self.df = self.df[self.df['grp'] > 0]
        count_after = len(self.df)
        log(f"Removed {count_before - count_after} blocks with grp =0 from {count_before}")


    def filter_min_grp(self,  min_grp: float):
        log_header("Filtering min grp")
        count_before = len(self.df)
        self.df = self.df[self.df['grp'] >= min_grp]
        count_after = len(self.df)
        log(f"Removed {count_before - count_after} blocks with less than {min_grp} grp from {count_before}")

    def tag_block_constraints(self, optimisation_items_valid:List[QuantityConstraint]):
        for optimisation_item in optimisation_items_valid:
            self.df[optimisation_item.column_name] = self.df[optimisation_item.type.value] == optimisation_item.name


    def run_filters(self, optimisation_def:OptimisationDef):
        self.filter_0()
        self.filter_banned_blocks(optimisation_def.banned_blockd_ids)
        self.filter_disallowed_items(optimisation_def.quantity_constraints_all)
        self.filter_min_grp(optimisation_def.quality_constraints_def.minGrp)

    @property
    def get_timebands_dict(self) -> Dict[str, Timeband]:
        timebands_dict: Dict[str, Timeband] = {}
        for schedule_break in self.schedule_breaks.values():
            if schedule_break.tbId1 in timebands_dict.keys():
                timeband1 = timebands_dict[schedule_break.tbId1]
            else:
                timeband1 = Timeband(schedule_break.tbId1)
                timebands_dict[schedule_break.tbId1] = timeband1

            timeband1.add_schedule_break(schedule_break)

            if schedule_break.tbId2 in timebands_dict.keys():
                timeband2 = timebands_dict[schedule_break.tbId2]
            else:
                timeband2 = Timeband(schedule_break.tbId2)
                timebands_dict[schedule_break.tbId2] = timeband2
            timeband2.add_schedule_break(schedule_break)
        return timebands_dict
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


def get_schedule(schedule_path:str, schedule_load_mode:enum.ScheduleLoadMode) -> Schedule:

    df_schedule_org = get_df_processor(enum.DfProcessorType.SCHEDULE, schedule_path).get_df
    load_breaks: bool

    match schedule_load_mode:
        case enum.ScheduleLoadMode.Optimisation:
            df_schedule_org.sort_values(by=['channel', 'xDateTime'], ascending=True, inplace=True)
            df_schedule_org.reset_index(inplace=True, drop=True)
            df_schedule = df_schedule_org.copy()
            df_schedule['available'] = 1
            df_schedule.reset_index()
            load_breaks = False
        case enum.ScheduleLoadMode.Booking:
            df_schedule = df_schedule_org.copy()
            load_breaks = True
        case _ :
            raise MyProgramException(f"Wrong schedule_load_mode: {schedule_load_mode}")
    schedule = Schedule(schedule_path, df_schedule_org , df_schedule)
    if load_breaks:
        schedule.load_breaks()
    return schedule


