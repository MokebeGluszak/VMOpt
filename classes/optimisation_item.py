import dataclasses
import zzz_enums as enums

@dataclasses.dataclass
class OptimisationItem:
    name:str
    min_grp:float
    allowed:bool
    type:enums.OptimisationItemType