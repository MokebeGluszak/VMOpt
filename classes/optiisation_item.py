import zzz_enums as enums
from classes.log import log, log_header
import dataclasses
import random


from classes.quantity_constraint import QuantityConstraint


def get_optimisation_item(quantity_constraint):
    oi = OptimisationItem(quantity_constraint, random.random, 0, False)
    return oi

@dataclasses.dataclass
class OptimisationItem():
    quantity_constraint: QuantityConstraint
    weight: float
    grp:float
    is_complete:bool