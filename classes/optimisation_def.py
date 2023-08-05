import json
from dataclasses import dataclass
from typing import List

from classes.optimisation_item import OptimisationItem
import zzz_enums as enums

def get_optimisation_def(optimisation_def_type:enums.OptimisationDefType):
    with open(optimisation_def_type.value, 'r') as file:
        json_data = json.load(file)
    planning_objects_dict = json_data["Planing objects"]
    # Create an instance of OptimisationDef
    optimisation_def = OptimisationDef(
        desired_grp=json_data["DesiredGRP"],
        channels=[OptimisationItem(ch['name'], ch['minGrp'],ch['allowed'], enums.OptimisationItemType.CHANNEL) for ch in planning_objects_dict["channels"]],
        channelGroups=[OptimisationItem(cg['name'], cg['minGrp'],cg['allowed'], enums.OptimisationItemType.CHANNELGROUP) for cg in planning_objects_dict["channelGroups"]],
        timebands=[OptimisationItem(tb['name'], tb['minGrp'],tb['allowed'], enums.OptimisationItemType.TIMEBAND) for tb in planning_objects_dict["timebands"]],
        weeks=[OptimisationItem(w['name'], w['minGrp'], w['allowed'], enums.OptimisationItemType.WEEK) for w in planning_objects_dict["weeks"]]
    )
    return optimisation_def
@dataclass
class OptimisationDef():
    desired_grp:float
    channels: List[OptimisationItem]
    channelGroups:List[OptimisationItem]
    timebands:List[OptimisationItem]
    weeks:List[OptimisationItem]

    @property
    def optimisation_items_all(self):
        return self.channels + self.channelGroups + self.timebands + self.weeks