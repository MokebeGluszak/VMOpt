import zzz_enums as ENUM
from classes.booking import get_booking
from classes.free_times import get_free_times
from classes.matching_processor import MatchingProcessor

from classes.schedule import Schedule, get_schedule

from zzz_tools import export_df


def matching():
    supplier: ENUM.Supplier = ENUM.Supplier.POLSAT
    booking_quality: ENUM.BookingQuality = ENUM.BookingQuality.FUCKED_UP_DATES
    schedule_type: ENUM.ScheduleType = ENUM.ScheduleType.OK_4CHANNELS_1WANTED
    free_times_quality: ENUM.FreeTimesQuality = ENUM.FreeTimesQuality.OK
    do_export_debug_files: bool = True

    schedule: Schedule = get_schedule(schedule_type)
    booking = get_booking(supplier, booking_quality)
    free_times = get_free_times(supplier, free_times_quality)
    matching_processor:MatchingProcessor = MatchingProcessor(schedule, booking, free_times)
    matching_processor.process_booking()
    matching_processor.process_free_times()
    # schedule: Schedule = get_schedule_with_free_times(schedule, supplier, free_times_quality)
    if do_export_debug_files:
        export_df(matching_processor.booking.to_dataframe(ENUM.ExportFormat.ChannelBreak), "channel breaks")
        export_df(matching_processor.schedule.to_dataframe(ENUM.ExportFormat.ScheduleBreak_rozkminki), "schedule - rozkminki")

    print(matching_processor.booking_report)


if __name__ == "__main__":
    matching()
