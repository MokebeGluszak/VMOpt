import json
from dataclasses import dataclass
from typing import List

from classes.optimisation_item import OptimisationItem
import zzz_enums as enums
from classes.quality_constraints_def import  QualityConstraintsDef
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
        channels=[OptimisationItem(ch['name'], ch['minGrp'],ch['allowed'], enums.OptimisationItemType.CHANNEL) for ch in planning_objects_dict["channels"]],
        channelGroups=[OptimisationItem(cg['name'], cg['minGrp'],cg['allowed'], enums.OptimisationItemType.CHANNELGROUP) for cg in planning_objects_dict["channelGroups"]],
        timebands=[OptimisationItem(tb['name'], tb['minGrp'],tb['allowed'], enums.OptimisationItemType.TIMEBAND) for tb in planning_objects_dict["timebands"]],
        weeks=[OptimisationItem(w['name'], w['minGrp'], w['allowed'], enums.OptimisationItemType.WEEK) for w in planning_objects_dict["weeks"]],
        quality_constraints_def=quality_constraints_def,
        banned_blockd_ids=json_data["bannedBlockIds"]
    )
    return optimisation_def
@dataclass
class OptimisationDef():
    desired_grp:float
    channels: List[OptimisationItem]
    channelGroups:List[OptimisationItem]
    timebands:List[OptimisationItem]
    weeks:List[OptimisationItem]
    quality_constraints_def:QualityConstraintsDef
    banned_blockd_ids:List[str]
    @property
    def optimisation_items_all(self):
        return self.channels + self.channelGroups + self.timebands + self.weeks