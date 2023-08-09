import zzz_enums as enums
from classes.log import log, log_header
import dataclasses
import random


from classes.quantity_constraint import QuantityConstraint


def get_optimisation_item(quantity_constraint):
    oi = OptimisationItem(quantity_constraint, random.random(), random.random(),  0, False)
    # oi = OptimisationItem(quantity_constraint, 0.5, 0, False)
    return oi

@dataclasses.dataclass
class OptimisationItem():
    quantity_constraint: QuantityConstraint
    weight_bonus: float
    weight_malus:float
    grp:float
    is_fulfilled:bool

    @property
    def weight_bonus_current(self):
        val:float
        if self.is_fulfilled:
            val = 0
        else:
            val = self.weight_bonus * (self.quantity_constraint.min_grp - self.grp) / float(self.quantity_constraint.min_grp)
        return val

    @property
    def weight_malus_current(self):
        val:float

        val = self.weight * (self.quantity_constraint.min_grp - self.grp) / float(self.quantity_constraint.min_grp)
        return val