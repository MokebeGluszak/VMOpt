import dataclasses
import json
from typing import Dict, List

import pandas as pd

import zzz_const as CONST
import zzz_enums as ENUM
from classes.break_info import BreakInfo
from classes.df_processor import get_df_processor
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.merger import get_merger
from classes.schedule_break import ScheduleBreak
from classes.status_info import StatusInfo
from classes.subcampaign import Subcampaign
from classes.timeband import Timeband
from classes.wantedness_info import WantednessInfo
from zzz_ordersTools import SgltChannelMapping
from zzz_tools import check_cannon_columns, Collection, getTimebandId, get_substring_between_parentheses, export_df


def getProcessedScheduleDf(df_scheduleOrg: pd.DataFrame, df_channelsMapping: pd.DataFrame) -> pd.DataFrame:
    df_scheduleOrg.rename(columns={"channel": "channel_org"}, inplace=True)
    df_scheduleProcessed = get_merger(
        "Processed schedule",
        df_scheduleOrg,
        df_channelsMapping,
        "channel_org",
        right_on="channelPossibleName",
        exception_type_unjoined=ENUM.ExceptionType.MERGER_ILLEGAL_CHANNELS_IN_SCHEDULE,
    ).return_merged_df()

    df_scheduleProcessed["dateTime"] = pd.to_datetime(
        df_scheduleProcessed["xDate"] + " " + df_scheduleProcessed["xTime"]
    )

    df_scheduleProcessed["tbId1"] = df_scheduleProcessed.apply(
        lambda row: getTimebandId(row["channel"], row["dateTime"], 30, 0, 30), axis=1
    )
    df_scheduleProcessed["tbId2"] = df_scheduleProcessed.apply(
        lambda row: getTimebandId(row["channel"], row["dateTime"], 30, 0, 0), axis=1
    )
    # t.msgBox("Templariusz", f'{len(df)}')

    # value_vars = "tb1 tb2".split()
    # id_vars = df_scheduleProcessed.columns.difference(value_vars).tolist()
    # df2 = pd.melt(df_scheduleProcessed, id_vars=id_vars, value_vars=value_vars, var_name="tbType", value_name="tb")
    # df2["tbId"] = df2["tb"].dt.strftime("%Y-%m-%d %H%M") + "|" + df2["channel"]
    check_cannon_columns(df_scheduleProcessed, ENUM.CannonColumnsSet.ScheduleProcessedFull, drop_excess_columns=True)
    return df_scheduleProcessed

@dataclasses.dataclass
class Schedule(iDataFrameable):
    source_path: str
    df: pd.DataFrame
    schedule_breaks: Collection[ScheduleBreak]
    schedule_info: str

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

    @property
    def get_subcampaigns_dict(self) -> dict[Subcampaign]:
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




    def to_dataframe(self, export_format: ENUM.ExportFormat):
        x: ScheduleBreak
        # print (type(self.schedule_breaks.values)

        df = pd.DataFrame(data=[x.serialize(export_format) for x in self.schedule_breaks.values()])
        df["scheduleInfo"] = ""
        df.loc[0, "scheduleInfo"] = self.schedule_info  # Assign the string value to the first row of the new column

        return df

    def export(self) -> str:
        df = self.to_dataframe(ENUM.ExportFormat.ScheduleBreak_minerwa)
        export_path = export_df(df, "schedule - minerwa", file_type=ENUM.FileType.CSV)
        return export_path

    def get_breaks_by_status(self, wanted: bool, booked: bool, supplier: ENUM.Supplier) -> List[ScheduleBreak]:
        breaks = []
        for schedule_break in self.schedule_breaks.values():
            if schedule_break.break_info.block_id == 15107428739:
                print("debug")
            if schedule_break.status_info.get_is_wanted == wanted:
                if schedule_break.status_info.is_booked == booked:
                    break_supplier = schedule_break.break_info.get_supplier
                    if break_supplier == supplier.value:
                        breaks.append(schedule_break)
        return breaks


def get_wantedness_info_from_row(wantedness) -> WantednessInfo:
    is_wanted: bool
    subcampaign: int
    origin: ENUM.Origin

    if wantedness == "NotWanted":
        is_wanted = False
        subcampaign = -1
        origin = ENUM.Origin.NotWanted
    elif wantedness.startswith("Wanted"):
        is_wanted = True
        sub_string = get_substring_between_parentheses(wantedness)
        subcampaign = int(get_substring_between_parentheses(sub_string))
        origin_str = sub_string.split(",")[0].strip()
        origin = ENUM.Origin.get_from_str(origin_str)
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
    breaks = Collection()
    for index, row in df.iterrows():
        wantedness_info = get_wantedness_info_from_row(row["wantedness"])
        block_id = row["blockId"]
        break_info = BreakInfo(
            blockId=block_id,
            date_time=row["dateTime"],
            ratecard=row["ratecard"],
            channel=row["channel"],
        )

        is_booked = get_is_booked(row["bookedness"])

        status_info = StatusInfo(
            subcampaign_id=wantedness_info.subcampaign, origin=wantedness_info.origin, is_booked=is_booked
        )

        schedule_break = ScheduleBreak(
            break_info=break_info,
            status_info=status_info,
            tbId1=row["tbId1"],
            tbId2=row["tbId2"],
            programme=row["programme"],
            blockType_org=row["blockType_org"],
            blockType_mod=row["blockType_mod"],
            freeTime=row["freeTime"],
            grpTg_01=row["grpTg_01"],
            grpTg_02=row["grpTg_02"],
            grpTg_50=row["grpTg_50"],
            grpTg_98=row["grpTg_98"],
            grpTg_99=row["grpTg_99"],
            positionCode=row["positionCode"],
        )
        breaks.add(schedule_break, block_id)

    return breaks


def get_schedule(schedule_type: ENUM.ScheduleType) -> Schedule:
    path_schedule = CONST.get_path_schedule(schedule_type)
    df_scheduleOrg = get_df_processor(ENUM.DfProcessorType.SCHEDULE, path_schedule).get_df
    schedule_info = df_scheduleOrg["scheduleInfo"][0]
    df_scheduleProcessed = getProcessedScheduleDf(df_scheduleOrg, SgltChannelMapping.get_df)

    schedule_breaks = get_schedule_breaks(df_scheduleProcessed)


    schedule = Schedule(path_schedule, df_scheduleProcessed, schedule_breaks, schedule_info)
    return schedule
