from typing import List

import openpyxl as xl

import zzz_const as CONST
import zzz_enums as ENUM
from classes.schedule import get_schedule
from classes.schedule_break import ScheduleBreak


def generate_order_file(supplier: ENUM.Supplier, breaks_wanted_unbooked: List[ScheduleBreak]):
    wb = xl.load_workbook(CONST.PATH_ORDER_TEMPLATE_POLSAT)


def main():
    supplier: ENUM.Supplier = ENUM.Supplier.POLSAT
    schedule_type: ENUM.ScheduleType = ENUM.ScheduleType.OK_4CHANNELS_1WANTED
    schedule = get_schedule(schedule_type)
    wanted_unbooked_breaks = schedule.get_breaks_by_status(True, False, supplier)
    generate_order_file(supplier, wanted_unbooked_breaks)


if __name__ == "__main__":
    main()
