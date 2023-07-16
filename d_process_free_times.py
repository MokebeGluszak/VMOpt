import zzz_enums as ENUM
from classes.free_times import FreeTimes
from classes.schedule import  Schedule


def get_free_times(
    supplier: ENUM.Supplier,
    booking_quality: ENUM.BookingQuality,
)->FreeTimes:

    from zzz_ordersTools import get_booking_file_path
    free_times = FreeTimes
    path = get_booking_file_path(supplier, booking_quality)
    return free_times



def get_schedule_with_free_times(schedule, supplier:ENUM.Supplier, free_times_quality:ENUM.FreeTimesQuality)->Schedule:
    schedule_with_free_times:Schedule = schedule
    return schedule_with_free_times

