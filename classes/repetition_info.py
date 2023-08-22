import dataclasses

import zzz_enums as enums
from classes.log import log, log_header



@dataclasses.dataclass
class RepetitionInfo:
    prog_before: str
    prog_after: str
    week:str

    def __post_init__(self):
        self.prog_before_week = f'{self.prog_before}|{self.week}'
        self.prog_after_week = f'{self.prog_after}|{self.week}'


    def get_proper_entry_name(self, repetition_type:enums.RepetitionType)->str:
        prog_name:str
        match repetition_type:
            case enums.RepetitionType.BeforeTotal:
                prog_name = self.prog_before
            case enums.RepetitionType.AfterTotal:
                prog_name = self.prog_after
            case enums.RepetitionType.BeforeWeekly:
                prog_name = self.prog_before_week
            case enums.RepetitionType.AfterWeekly:
                prog_name = self.prog_after_week
            case _:
                log_header("RepetitionInfo.get_proper_prog_name")
        return prog_name
