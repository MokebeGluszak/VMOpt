from typing import List

import openpyxl as xl

import zzz_const as CONST
import zzz_enums as ENUM
from classes.schedule_break import ScheduleBreak


def generate_order_file(supplier: ENUM.Supplier, breaks_wanted_unbooked: List[ScheduleBreak]):
    wb = xl.load_workbook(CONST.PATH_ORDER_TEMPLATE_POLSAT)
