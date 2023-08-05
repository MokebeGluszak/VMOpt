from b_check_consistency import check_optimisation_consistency
from c_filter_disallowed_items import filter_disallowed_items
from classes.optimisation_def import get_optimisation_def, OptimisationDef
from classes.result_folder import SgltResultFolder
from classes.file import get_file, File
from classes.schedule import Schedule, get_schedule
import zzz_enums as enums

schedule:Schedule = get_schedule(enums.ScheduleType.OK)
optimisation_def:OptimisationDef = get_optimisation_def(enums.OptimisationDefType.OK)
filter_disallowed_items(schedule.df, optimisation_def.optimisation_items_all)
check_optimisation_consistency(schedule.df, optimisation_def.optimisation_items_all)
schedule.load_breaks()
# schedule.load_breaks