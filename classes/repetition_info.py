import dataclasses

import zzz_enums as enums
from classes.log import log, log_header
from classes.repetitions_checker import RepetitionsChecker


@dataclasses.dataclass
class RepetitionInfo:
    prog_after: str
    prog_before: str
    week:str

    def __post_init__(self):
        self.prog_before_week = self.prog_before + self.week
        self.prog_after_week = self.prog_after + self.week

    def get_proper_prog_name(self, repetitions_checker:RepetitionsChecker):
        match repetitions_checker.column_name & repetitions_checker.is_weekly:
            case
