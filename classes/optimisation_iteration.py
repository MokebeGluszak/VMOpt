from typing import List

import pandas as pd

import zzz_enums as enums
from classes.log import log, log_header
import dataclasses

from classes.optiisation_item import OptimisationItem, get_optimisation_item
from classes.quantity_constraint import QuantityConstraint

@dataclasses.dataclass
class OptimisationIteration:
    df:pd.DataFrame
    id:int
    optimisation_items:List[QuantityConstraint]


def get_optimisation_items(quantity_constraints:List[QuantityConstraint])->List[OptimisationItem]:
    ois = []
    for quantity_constraint in quantity_constraints:
        oi = get_optimisation_item(quantity_constraint)
        ois.append(oi)
    return ois

def get_optimisation_iteration(df:pd.DataFrame, id:int, optimisation_items:List[QuantityConstraint])->OptimisationIteration:
    ois = get_optimisation_items(optimisation_items)
    optimisation = OptimisationIteration(df, id, ois)
    return optimisation





