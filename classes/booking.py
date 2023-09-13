import os
from typing import List, Set

import pandas as pd
import zzz_ordersTools as ot
import zzz_enums as enum
from classes.channel_break import ChannelBreak, get_channel_break
from classes.df_processor import get_df_processor
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.merger import get_merger
from zzz_tools import Collection
from zzz_tools import getTimebandId, check_cannon_columns


class Booking(iDataFrameable):
    def __init__(self, supplier: enum.Supplier, df: pd.DataFrame, channel_breaks: List[ChannelBreak]):
        self.supplier = supplier
        self.df = df
        self.channel_breaks = channel_breaks

    def to_dataframe(self, export_format: enum.ExportFormat) -> pd.DataFrame:
        df = pd.DataFrame(data=[x.serialize(export_format) for x in self.channel_breaks])

        return df

    @property
    def get_unmatched_channel_breaks(self):
        breaks = Collection()
        for channel_break in self.channel_breaks:
            if channel_break.match_level == enum.MatchLevel.NO_MATCH:
                breaks.add(channel_break, channel_break.break_info.block_id)
        return breaks

    @property
    def get_subcampaings_orgs_set(self) -> Set[str]:
        subcampaigns_orgs = set()
        for channel_break in self.channel_breaks:
            subcampaigns_org = channel_break.subcampaing_org
            subcampaigns_orgs.add(subcampaigns_org)
        return subcampaigns_orgs




def get_df_booking_org(supplier: enum.Supplier, file_path:str) -> pd.DataFrame:
    # ta procedura zwraca zunifikowanego df rozpatrzywszy dostawce


    if supplier == enum.Supplier.TVP:
        raise NotImplementedError("TVP booking not implemented")
        print(0 / 0)  # wywalić wczytywanie jako string
        df_booking_org = pd.read_excel(supplier.value, dtype=str)

    elif supplier == enum.Supplier.TVN:
        raise NotImplementedError("TVN booking not implemented")
        # df_booking_org = pd.read_csv(booking_file.value, sep=";", encoding="utf-8")
    #     dateTime = get_date_time_tvn(row["DATA"], row["PLANOWANA GODZ."])
    #     channel = row["KANAŁ"]
    #     ratecard = t.get_float(row["WARTOŚĆ SPOTU"])

    elif supplier == enum.Supplier.POLSAT:
        df_booking_org = get_df_processor(enum.DfProcessorType.BOOKING_POLSAT, file_path).get_df
    else:
        raise MyProgramException(f"Wrong supplier: {supplier}")

    return df_booking_org



def get_booking(
    supplier: enum.Supplier,
    booking_file_path:str,
) -> Booking:
    df_booking_org = get_df_booking_org(supplier, booking_file_path)

    df_booking = get_merger(
        "Merge channels",
        df_booking_org,
        ot.get_channels_mapping_df(),
        "channel_org",
        right_on="channel_possible_name",
        exception_type_unjoined=enum.ExceptionType.MERGER_ILLEGAL_CHANNELS_IN_BOOKING,
    ).return_merged_df()

    df_booking["tbId"] = df_booking.apply(
        lambda row: getTimebandId(row["channel"], row["dateTime"], 30, 15, 30), axis=1
    )

    check_cannon_columns(df_booking, enum.CannonColumnsSet.BookingProcessed, drop_excess_columns=True)
    channel_breaks = get_channel_breaks(df_booking)
    # t.msgBox("templarriuuuusz", f"channel_breaks: {len(channel_breaks)}")

    booking = Booking(supplier, df_booking, channel_breaks)
    return booking


def get_channel_breaks(df: pd.DataFrame) -> List[ChannelBreak]:
    channel_breaks = []
    for _, row in df.iterrows():
        channel_break = get_channel_break(row)
        channel_breaks.append(channel_break)
    return channel_breaks
