from b_check_consistency import check_optimisation_consistency
from classes.optimisation_iteration import get_optimisation_iteration

from classes.optimisation_def import get_optimisation_def, OptimisationDef
from classes.file import get_file, File
from classes.schedule import Schedule, get_schedule
import zzz_enums as enums
from classes.result_folder import export_file_path
from classes.log import log, log_header, print_log


schedule:Schedule = get_schedule(enums.ScheduleType.OK)
optimisation_def:OptimisationDef = get_optimisation_def(enums.OptimisationDefType.OK)
schedule.filter_banned_blocks( optimisation_def.banned_blockd_ids)
schedule.filter_disallowed_items(optimisation_def.quantity_constraints_all)
schedule.filter_min_grp(optimisation_def.quality_constraints_def.minGrp)
schedule.filter_0()
check_optimisation_consistency(schedule.df, optimisation_def.quantity_constraints_all)
schedule.tag_block_constraints(optimisation_def.quantity_constraints_valid)
for n_optimisation in range(1, 2):
    optimisation_iteration = get_optimisation_iteration(schedule.df, n_optimisation, optimisation_def.quantity_constraints_all)
schedule.df.to_excel(export_file_path('schedule.xlsx'), index=False)
print_log()