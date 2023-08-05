import zzz_enums as enums
from classes.log import log, log_header
from dataclasses import dataclass
@dataclass
class QualityConstraintsDef():
    maxRepetitionsWeekly:int
    maxRepetitionsTotal:int
    minSpotInterval:int
    minGrp:float
