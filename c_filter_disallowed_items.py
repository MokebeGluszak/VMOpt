from typing import List

import pandas as pd

from classes.optimisation_item import OptimisationItem
from classes.log import log, log_header

def filter_disallowed_items(schedule_df:pd.DataFrame, optimisation_items:List[OptimisationItem]):
    log_header("Processing disallowed items")
    count_start: int = len(schedule_df)
    for optimisation_item in optimisation_items:
        if not optimisation_item.allowed:
            count_before: int = len(schedule_df)
            schedule_df = schedule_df[schedule_df[optimisation_item.type.value] != optimisation_item.name]
            count_after: int = len(schedule_df)
            log( f"Removed {count_before - count_after} {optimisation_item.type} {optimisation_item.name} from schedule")
    log (f"\nTotal removed by dissaloved items:  {count_start - count_after}")
