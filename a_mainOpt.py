from builtins import NotImplementedError
from typing import List
import copy
from b_check_consistency import check_optimisation_consistency
from classes.optimisation_iteration import (
    get_optimisation_iteration,
    OptimisationIteration,
)

from classes.optimisation_def import get_optimisation_def, OptimisationDef
from classes.file import get_file, File
from classes.repetitions_checker import get_repetitions_checkers
from classes.schedule import Schedule, get_schedule
import zzz_enums as enums
from classes.result_folder import export_file_path
import classes.log as log
from zzz_const import MODE_DEBUG


# from zzz_optToolz import get_optimisation_info


def get_best_iteration(
    copy_number: int,
    schedule_type: enums.ScheduleType,
    optimisation_def_type: enums.OptimisationDefType,
    iterations_count: int,
    random_bonus: bool ,
) -> OptimisationIteration:

    schedule: Schedule = get_schedule(schedule_type)
    optimisation_def: OptimisationDef = get_optimisation_def(optimisation_def_type)
    schedule.run_filters(optimisation_def)
    check_optimisation_consistency(
        schedule.df, optimisation_def.quantity_constraints_all
    )
    schedule.df["progBeforeWeek"] = schedule.df["progBefore"] + "|" + schedule.df["week"]
    schedule.df["progAfterWeek"] = schedule.df["progAfter"] + "|" + schedule.df["week"]
    schedule.tag_block_constraints(optimisation_def.quantity_constraints_valid)
    log.log_header("Optimisation")
    iterations: List[OptimisationIteration] = []
    repetition_checkers = get_repetitions_checkers(optimisation_def.quality_constraints_def.maxRepetitionsTotal,optimisation_def.quality_constraints_def.maxRepetitionsWeekly, schedule.df)
    for n_iteration in range(1, 1 + iterations_count):
        df_copy = schedule.df.copy()
        repetition_checkers_copy = copy.deepcopy(repetition_checkers)

        optimisation_iteration: OptimisationIteration = get_optimisation_iteration(
            schedule.df_org,
            df_copy,
            copy_number,
            n_iteration,
            optimisation_def.quantity_constraints_valid,
            optimisation_def.quality_constraints_def,
            optimisation_def.desired_grp,
            repetition_checkers_copy,
            random_bonus,
        )

        if MODE_DEBUG:
            optimisation_iteration.run_optimisation()
        else:
            try:
                optimisation_iteration.run_optimisation()
            except Exception as e:
                log.log(f"Optimisation {n_iteration} failed: {e}")
        iterations.append(optimisation_iteration)
    complete_iterations = [x for x in iterations if x.complete]
    if len(complete_iterations)>0:
        iteration_best = min(iterations, key=lambda x: x.get_cpp)
        iteration_best.check_result(copy_number)
        log.log("Best: " + iteration_best.get_info)
    else:
        log.print_log()
        raise Exception("Cannot find desired solution")
    return iteration_best


if __name__ == "__main__":
    optimisation_iteration: OptimisationIteration = get_best_iteration(
        copy_number=1,
        schedule_type=enums.ScheduleType.OK9,
        optimisation_def_type=enums.OptimisationDefType.OK,
        iterations_count=5,
        random_bonus=True
    )
    optimisation_iteration.export_schedule()
    log.print_log()
