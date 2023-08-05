from typing import List

import pandas as pd

from classes.optimisation_item import OptimisationItem


def filter_disallowed_items(schedule_df:pd.DataFrame, optimisation_items:List[OptimisationItem]):
    info_str: str = "Processing disallowed items\n"
    count_start: int = len(schedule_df)
    for optimisation_item in optimisation_items:
        if not optimisation_item.allowed:
            count_before: int = len(schedule_df)
            schedule_df = schedule_df[schedule_df[optimisation_item.type.value] != optimisation_item.name]
            count_after: int = len(schedule_df)
            info_str = info_str + f"Removed {count_before - count_after} {optimisation_item.type} {optimisation_item.name} from schedule\n"
    info_str = info_str + f"\nTOTAL REMOVED BY DISALLOWED ITEMS:  {count_start - count_after}\n"
    print (info_str)