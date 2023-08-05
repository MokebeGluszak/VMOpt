from typing import List

import pandas as pd
from classes.optimisation_def import OptimisationDef
from classes.quantity_constraint import QuantityConstraint
from classes.log import  log, log_header

def check_optimisation_consistency(schedule_df:pd.DataFrame, optimisation_items:List[QuantityConstraint]):
    check_optimisation_items(schedule_df,optimisation_items)



def check_optimisation_items(schedule_df:pd.DataFrame , optimisation_items:List[QuantityConstraint] ):
    error_str:str = ''
    # log_header('Check optimisation items')
    for optimisation_item in optimisation_items:
        available_grp = schedule_df.loc[schedule_df[optimisation_item.type.value] == optimisation_item.name, 'grp'].sum()
        if available_grp < optimisation_item.min_grp:
            error_str = error_str + '\n' + f'Not enough grp for {optimisation_item.type.value} {optimisation_item.name}. Available: {available_grp}, required: {optimisation_item.min_grp}'

    if error_str != "":
        raise Exception(error_str)
    # log('OK')