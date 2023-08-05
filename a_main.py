from b_check_consistency import check_optimisation_consistency
from c_filter_disallowed_items import filter_disallowed_items
from classes.optimisation_def import get_optimisation_def, OptimisationDef
from classes.result_folder import SgltResultFolder
from classes.file import get_file, File
from classes.schedule import Schedule, get_schedule
import zzz_enums as enums
from classes.log import log, log_header, print_log
from d_filter_banned_blocks import filter_banned_blocks

schedule:Schedule = get_schedule(enums.ScheduleType.OK)
optimisation_def:OptimisationDef = get_optimisation_def(enums.OptimisationDefType.OK)
filter_disallowed_items(schedule.df, optimisation_def.optimisation_items_all)
filter_banned_blocks(schedule.df, optimisation_def.banned_blockd_ids)
check_optimisation_consistency(schedule.df, optimisation_def.optimisation_items_all)
schedule.load_breaks()
print_log()