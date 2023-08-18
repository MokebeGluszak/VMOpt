from builtins import NotImplementedError
from typing import List

from b_check_consistency import check_optimisation_consistency
from classes.optimisation_iteration import (
    get_optimisation_iteration,
    OptimisationIteration,
)

from classes.optimisation_def import get_optimisation_def, OptimisationDef
from classes.file import get_file, File
from classes.schedule import Schedule, get_schedule
import zzz_enums as enums
from classes.result_folder import export_file_path
import classes.log as log

# from zzz_optToolz import get_optimisation_info


def get_best_iteration(
    copy_number: int,
    schedule_type: enums.ScheduleType,
    optimisation_def_type: enums.OptimisationDefType,
    iterations_count: int = 1,
) -> OptimisationIteration:
    schedule: Schedule = get_schedule(schedule_type)
    optimisation_def: OptimisationDef = get_optimisation_def(optimisation_def_type)
    schedule.run_filters(optimisation_def)
    check_optimisation_consistency(
        schedule.df, optimisation_def.quantity_constraints_all
    )
    schedule.df["progBeforeWeek"] = schedule.df["progBefore"] + schedule.df["week"]
    schedule.df["progAfterWeek"] = schedule.df["progAfter"] + schedule.df["week"]
    schedule.tag_block_constraints(optimisation_def.quantity_constraints_valid)
    log.log_header("Optimisation")
    iterations: List[OptimisationIteration] = []
    for n_optimisation in range(1, 1 + iterations_count):
        optimisation_iteration: OptimisationIteration = get_optimisation_iteration(
            schedule.df_org,
            schedule.df,
            n_optimisation,
            optimisation_def.quantity_constraints_valid,
            optimisation_def.quality_constraints_def,
            optimisation_def.desired_grp,
        )
        optimisation_iteration.run_part1_fulfillConstraints(copy_number)
        optimisation_iteration.run_part2_fulfillTotal(copy_number)
        optimisation_iteration.run_part3_decrement(copy_number)
        optimisation_iteration.check_result(copy_number)
        iterations.append(optimisation_iteration)
    iteration_best = min(iterations, key=lambda x: x.get_cpp)
    iteration_best.check_result(copy_number)
    log.log("Best: " + iteration_best.get_info)
    return iteration_best


if __name__ == "__main__":
    optimisation_iteration: OptimisationIteration = get_best_iteration(
        copy_number=1,
        schedule_type=enums.ScheduleType.OK,
        optimisation_def_type=enums.OptimisationDefType.OK,
        iterations_count=3,
    )
    optimisation_iteration.export_schedule()
    log.print_log()
