import zzz_const as CONST
import zzz_enums as ENUM
from classes.booking import get_booking
from classes.folder import get_folder
from classes.free_times import get_free_times
from classes.matching_processor import MatchingProcessor
from classes.schedule import Schedule, get_schedule
from classes.sglt_project_cfg import SgltProjectCfg
from zzz_tools import export_df


def matching():

    cfg = SgltProjectCfg()
    get_folder(CONST.PATH_SLOWNIKI_ALIASES_FOLDER).clear()
    schedule: Schedule = get_schedule( cfg.schedule_type)
    booking = get_booking(cfg.supplier, cfg.booking_quality)
    free_times = get_free_times(cfg.supplier, cfg.free_times_quality)
    matching_processor: MatchingProcessor = MatchingProcessor(schedule, booking, free_times)
    matching_processor.process_booking()
    matching_processor.process_free_times()
    # schedule: Schedule = get_schedule_with_free_times(schedule, supplier, free_times_quality)
    if cfg.do_export_debug_files:
        export_df(matching_processor.booking.to_dataframe(ENUM.ExportFormat.ChannelBreak), "channel breaks")
        export_df(
            matching_processor.schedule.to_dataframe(ENUM.ExportFormat.ScheduleBreak_rozkminki), "schedule - rozkminki"
        )

    print(matching_processor.booking_report)


if __name__ == "__main__":
    matching()
