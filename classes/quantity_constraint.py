import dataclasses
import zzz_enums as enums

@dataclasses.dataclass
class QuantityConstraint:
    name:str
    min_grp:float
    allowed:bool
    type:enums.QuantityConstraintType
    @property
    def column_name(self):
        name = self.type.value + "_" + self.name
        return name