from typing import List, Set

import pandas as pd

import zzz_enums as ENUM
from classes.channel_break import ChannelBreak, get_channel_break
from classes.dfProcessor import get_df_processor
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.merger import get_merger
from zzz_ordersTools import SgltChannelMapping
from zzz_tools import Collection
from zzz_tools import getTimebandId, check_cannon_columns


class Booking(iDataFrameable):
    def __init__(self, supplier: ENUM.Supplier, df: pd.DataFrame, channel_breaks: List[ChannelBreak]):
        self.supplier = supplier
        self.df = df
        self.channel_breaks = channel_breaks

    def to_dataframe(self, export_format: ENUM.ExportFormat) -> pd.DataFrame:
        df = pd.DataFrame(data=[x.serialize(export_format) for x in self.channel_breaks])

        return df

    def get_unmatched_channel_breaks(self):
        breaks = Collection()
        for channel_break in self.channel_breaks:
            if channel_break.match_level == ENUM.MatchLevel.NO_MATCH:
                breaks.add(channel_break, channel_break.break_info.block_id)
        return breaks

    def get_subcampaings_orgs_set(self) -> Set[str]:
        subcampaigns_orgs = []
        for channel_break in self.channel_breaks:
            subcampaigns_org = channel_break.subcampaing_org
            subcampaigns_orgs.append(subcampaigns_org)
        return set(subcampaigns_orgs)

def get_booking(
    supplier: ENUM.Supplier,
    booking_quality: ENUM.BookingQuality,
) -> Booking:
    from zzz_ordersTools import get_booking_path

    path = get_booking_path(supplier, booking_quality)

    if supplier == ENUM.Supplier.TVP:
        print(0 / 0)  # wywalić wczytywanie jako string
        df_booking_org = pd.read_excel(path, dtype=str)

    elif supplier == ENUM.Supplier.TVN:
        df_booking_org = pd.read_csv(path, sep=";", encoding="utf-8")
    #     dateTime = get_date_time_tvn(row["DATA"], row["PLANOWANA GODZ."])
    #     channel = row["KANAŁ"]
    #     ratecard = t.get_float(row["WARTOŚĆ SPOTU"])

    elif supplier == ENUM.Supplier.POLSAT:
        df_booking_org = get_df_processor(ENUM.DfProcessorType.BOOKING_POLSAT, path).get_df
    else:
        raise MyProgramException(f"Wrong supplier: {supplier}")

    df_booking = get_merger(
        "Merge channels",
        df_booking_org,
        SgltChannelMapping.get_df,
        "channelOrg",
        right_on="channelPossibleName",
        exception_type_unjoined=ENUM.ExceptionType.MERGER_ILLEGAL_CHANNELS_IN_BOOKING,
    ).return_merged_df()

    df_booking["tbId"] = df_booking.apply(
        lambda row: getTimebandId(row["channel"], row["dateTime"], 30, 15, 30), axis=1
    )

    check_cannon_columns(df_booking, ENUM.CannonColumnsSet.BookingProcessed, drop_excess_columns=True)
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
