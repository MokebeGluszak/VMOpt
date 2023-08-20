import dataclasses
from typing import Dict, List

import pandas as pd

import zzz_enums as enums
from classes.log import log, log_header
from classes.repetition_info import RepetitionInfo


@dataclasses.dataclass
class RepetitionsChecker():
    repetition_type: enums.RepetitionType
    max_repetitions:int


    def __post_init__(self):
        self.banned_progs_dict: Dict[str] = {}
        if self.is_weekly:
            self.column_name = self.prog_column + 'Week'
        else:
            self.column_name = self.prog_column

        match self.repetition_type
            case enums.RepetitionType.BeforeTotal:
                self.prog_column = 'progBefore'
                self.is_weekly = False
            case enums.RepetitionType.AfterTotal:
                self.prog_column = 'progAfter'
                self.is_weekly = False
            case enums.RepetitionType.BeforeWeekly:
                self.prog_column = 'progBefore'
                self.is_weekly = True
            case enums.RepetitionType.AfterWeekly:
                self.prog_column = 'progAfter'
                self.is_weekly = True

        self.prog_column:str
        self.is_weekly:bool

    def add_entry(self, repetition_info:RepetitionInfo):
        match self.prog_column + str(self.is_weekly):
            case 'progBeforeFalse':
                prog_name = repetition_info.prog_before
            case 'progAfterFalse':
                prog_name = repetition_info.prog_after
            case 'progAfterTrue':
                prog_name = repetition_info.prog_after + repetition_info.week
            case 'progBeforeTrue':
                prog_name = repetition_info.prog_before + repetition_info.week
            case _:
                raise Exception('Invalid column_name and is_weekly combination')

        self.banned_progs_dict[prog_name] += 1

def get_repetitions_checkers( max_repetitions_total:int,max_repetitions_weekly:int, df:pd.DataFrame)->List[RepetitionsChecker]:
    checkers = []
    checkers.append (RepetitionsChecker(prog_column='progBefore', is_weekly=False, max_repetitions= max_repetitions_total))
    checkers.append (RepetitionsChecker(prog_column='progAfter', is_weekly=True, max_repetitions= max_repetitions_weekly))
    checkers.append (RepetitionsChecker(prog_column='progBefore', is_weekly=True, max_repetitions= max_repetitions_total))
    checkers.append (RepetitionsChecker(prog_column='progAfter', is_weekly=False, max_repetitions= max_repetitions_weekly))

    for checker in checkers:
        checker.banned_progs_dict = {prog: 0 for prog in df[checker.column_name].unique()}


    return checkers
