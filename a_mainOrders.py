
import classes.log as log
import zzz_enums as enum
import zzz_const as const
from classes.booking import get_booking
from classes.folder import get_folder
from classes.free_times import get_free_times
from classes.matching_processor import MatchingProcessor
from classes.schedule import Schedule, get_schedule
from zzz_tools import export_df



def matching(schedule_path:str, supplier:enum.Supplier , booking_path:str):

    get_folder(const.PATH_SLOWNIKI_ALIASES_FOLDER).clear()
    schedule: Schedule = get_schedule(schedule_path)
    booking = get_booking(supplier, booking_path)
    # free_times = get_free_times(cfg.supplier, cfg.free_times_quality)
    matching_processor: MatchingProcessor = MatchingProcessor(schedule, booking, None)
    matching_processor.process_booking()
    matching_processor.process_free_times()
    # schedule: Schedule = get_schedule_with_free_times(schedule, supplier, free_times_quality)
    if const.MODE_DEBUG:
        export_df(matching_processor.booking.to_dataframe(enum.ExportFormat.ChannelBreak), "channel breaks")
        export_df(
            matching_processor.schedule.to_dataframe(enum.ExportFormat.ScheduleBreak_rozkminki), "schedule - rozkminki"
        )

    print(matching_processor.booking_report)


if __name__ == "__main__":

    matching(
        enum.ScheduleType.OK9_small.value,
        enum.Supplier.POLSAT,
        enum.BookingFile.PolsatOkRatecard.value
    )
