from typing import List

import pandas as pd
from classes.optimisation_def import OptimisationDef
from classes.optimisation_item import OptimisationItem


def check_optimisation_consistency(schedule_df:pd.DataFrame, optimisation_items:List[OptimisationItem]):
    check_optimisation_items(schedule_df,optimisation_items)



def check_optimisation_items(schedule_df:pd.DataFrame , optimisation_items:List[OptimisationItem] ):
    error_str:str = ''
    for optimisation_item in optimisation_items:
        available_grp = schedule_df.loc[schedule_df[optimisation_item.type.value] == optimisation_item.name, 'grp'].sum()
        if available_grp < optimisation_item.min_grp:
            error_str = error_str + '\n' + f'Not enough grp for {optimisation_item.type.value} {optimisation_item.name}. Available: {available_grp}, required: {optimisation_item.min_grp}'

    if error_str != "":
        raise Exception(error_str)