# This is a sample Python script.
from typing import Dict, List, Set

import pandas as pd

import c_process_booking as matching
import d_process_schedule as ps
import zzz_const as const
import zzz_enums as enum
import zzz_ordersTools as ot
from classes.booking import get_booking
from classes.schedule import get_schedule, Schedule
from classes.subcampaign import Subcampaign
from zzz_tools import export_df


def get_existing_subcampaign_dict() -> Dict[str, Subcampaign]:
    subcampaigns_dict: Dict[str, Subcampaign] = {}
    subcampaigns_df = pd.read_csv(const.PATH_DICT_SUBCAMPAIGNS, sep=";", encoding="utf-8")

    for _, row in subcampaigns_df.iterrows():
        subcampaign_org = row["subcampaign_org"]
        subcampaign_str = row["subcampaign_hash"]
        id, name, length = subcampaign_str.split("|")
        subcampaign = Subcampaign(id, name, length)
        subcampaigns_dict[subcampaign_org] = subcampaign
    return subcampaigns_dict

# Hardcoded user interaction
def get_subcampaigns_dict(subcampaign_orgs_booking: Set[str], subcampaigns_schedule: List[Subcampaign]) -> Dict[str, Subcampaign]:
    existing_dict = get_existing_subcampaign_dict()
    subcampaign_existing_dict: Subcampaign
    subcampaign_org_existing_dict:str
    subcampaign_hashes_schedule:List[str] = [subcampaign.get_hash for subcampaign in subcampaigns_schedule]
    valid_dict = {}

    # mg2023-07-13 jeżeli hasza z istniejącego dicta nie ma w schedulu to zmieniłą się lista subcampaignów, albo świadomie albo się zjebało, anyłej pozwalamy na to, tylko dla bezpieczeńśtwa przesłownikowac
    for subcampaign_org_existing_dict, subcampaign_existing_dict in existing_dict.items():
        if  subcampaign_existing_dict.get_hash  in subcampaign_hashes_schedule:
            valid_dict[subcampaign_org_existing_dict] = subcampaign_existing_dict
        else:
            pass

    #robimy listę subcampaignów_org istniejących w bukingu a nie w dict
    subcampaigns_org_booking_not_in_dict  = subcampaign_orgs_booking - set(valid_dict.keys())
    # teraz pokazujesz GUI i każesz przypisać subcampaigns_org_booking_not_in_dict do haszów z listy subcampaign_hashes_schedule i dodajesz do valid_dict
    ####zahardkodowane to co ma się robić w gui
    if len(subcampaigns_org_booking_not_in_dict) == 1:
        subcampaign_org_to_add =  list(subcampaigns_org_booking_not_in_dict)[0]
        valid_dict[subcampaign_org_to_add] = subcampaigns_schedule[0]
    else:
        raise NotImplementedError
    ####

    if not subcampaign_orgs_booking.issubset(valid_dict.keys()):
        raise NotImplementedError("po wykonaniu tej funkcji każdy subcampaign_org z bookingu musi być w valid_dict")
    return valid_dict

def get_schedule_with_booking(
    supplier: enum.Supplier,
    booking_quality: enum.BookingQuality,
    schedule_type: enum.ScheduleType,
) -> Schedule:
    # print(calculate_circle_data(5, CircleDataType.PERIMETER))


    schedule = get_schedule(schedule_type)
    schedule.booking = get_booking(supplier,  booking_quality=booking_quality)


    subcampaigns_dict = get_subcampaigns_dict(schedule.booking.get_subcampaings_orgs_set(), schedule.get_subcampaigns())
    ot.check_time_space_consistency(schedule.booking.df, schedule.df)
    matching.match_channel_breaks_step1_id(schedule.booking.get_unmatched_channel_breaks(), schedule.schedule_breaks)
    matching.match_channel_breaks_step2_timebands(schedule.booking.get_unmatched_channel_breaks(), schedule.get_timebands_dict())
    schedule.booking_report =   ps.process_booking(schedule.schedule_breaks, schedule.booking.channel_breaks, subcampaigns_dict)  # modyfikuje schedule brejki




        # t.export_df(schedule.df, "1a schedule_processed")
        # t.export_df(booking.df, "1b booking_processed")
        # # t.export_df(df_matching, "2 matching")
        # df_channelBreaks = booking.get_df()
        # t.export_df(df_channelBreaks, "channel breaks")
        # t.export_df(df_channelsMapping, "channels_mapping")
    return schedule


def main():
    supplier: enum.Supplier = enum.Supplier.POLSAT
    booking_quality: enum.BookingQuality = enum.BookingQuality.FUCKED_UP_DATES
    schedule_type: enum.ScheduleType = enum.ScheduleType.OK_4CHANNELS_1WANTED
    free_times_quality: enum.FreeTimesQuality = enum.FreeTimesQuality.OK

    do_export_debug_files:bool = True
    schedule:Schedule =  get_schedule_with_booking(supplier, booking_quality, schedule_type)
    schedule:Schedule = get_schedule_with_free_times(schedule, supplier, free_times_quality)
    if do_export_debug_files:
        export_df(schedule.booking.to_dataframe(enum.ExportFormat.ChannelBreak), "channel breaks")
        export_df(schedule.to_dataframe(enum.ExportFormat.ScheduleBreak_rozkminki), "schedule - rozkminki")

    print (schedule.booking_report)

if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
