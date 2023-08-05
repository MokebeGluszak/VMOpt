import json
from dataclasses import dataclass
from typing import List


import zzz_enums as enums
from classes.quality_constraints_def import  QualityConstraintsDef
from classes.quantity_constraint import QuantityConstraint


def get_optimisation_def(optimisation_def_type:enums.OptimisationDefType):
    with open(optimisation_def_type.value, 'r') as file:
        json_data = json.load(file)
    planning_objects_dict = json_data["Planing objects"]
    quality_constraints_dict = json_data["qualityConstraints"]

    quality_constraints_def = QualityConstraintsDef(
        quality_constraints_dict["maxRepetitionsWeekly"],
        quality_constraints_dict["maxRepetitionsTotal"],
        quality_constraints_dict["minSpotInterval"],
        quality_constraints_dict["minGrp"]
    )



    optimisation_def = OptimisationDef(
        desired_grp=json_data["DesiredGRP"],
        channels=[QuantityConstraint(ch['name'], ch['minGrp'], ch['allowed'], enums.QuantityConstraintType.CHANNEL) for ch in planning_objects_dict["channels"]],
        channelGroups=[QuantityConstraint(cg['name'], cg['minGrp'], cg['allowed'], enums.QuantityConstraintType.CHANNELGROUP) for cg in planning_objects_dict["channelGroups"]],
        timebands=[QuantityConstraint(tb['name'], tb['minGrp'], tb['allowed'], enums.QuantityConstraintType.TIMEBAND) for tb in planning_objects_dict["timebands"]],
        weeks=[QuantityConstraint(w['name'], w['minGrp'], w['allowed'], enums.QuantityConstraintType.WEEK) for w in planning_objects_dict["weeks"]],
        quality_constraints_def=quality_constraints_def,
        banned_blockd_ids=json_data["bannedBlockIds"]
    )
    return optimisation_def
@dataclass
class OptimisationDef():
    desired_grp:float
    channels: List[QuantityConstraint]
    channelGroups:List[QuantityConstraint]
    timebands:List[QuantityConstraint]
    weeks:List[QuantityConstraint]
    quality_constraints_def:QualityConstraintsDef
    banned_blockd_ids:List[str]
    @property
    def quantity_constraints_all(self)->List[QuantityConstraint]:
        return self.channels + self.channelGroups + self.timebands + self.weeks

    @property
    def quantity_constraints_valid(self)->List[QuantityConstraint]:
        return [item for item in self.quantity_constraints_all if item.min_grp > 0]
