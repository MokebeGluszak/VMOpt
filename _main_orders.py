import zzz_enums as ENUM
from classes.schedule import get_schedule
from f_generate_orders import generate_order_file


def generate_orders():
    supplier: ENUM.Supplier = ENUM.Supplier.POLSAT
    schedule_type: ENUM.ScheduleType = ENUM.ScheduleType.OK_4CHANNELS_1WANTED
    schedule = get_schedule(schedule_type)
    wanted_unbooked_breaks = schedule.get_breaks_by_status(True, False, supplier)
    generate_order_file(supplier, wanted_unbooked_breaks)


if __name__ == "__main__":
    generate_orders()
