import dataclasses
from typing import Dict, List

import pandas as pd

import zzz_enums as enums
from classes.log import log, log_header
from classes.repetition_info import RepetitionInfo
from zzz_tools import get_filtered_df


@dataclasses.dataclass
class RepetitionsChecker():
    repetition_type: enums.RepetitionType
    max_repetitions:int


    def __post_init__(self):
        self.prog_repetitions_dict: Dict[str, int] = {}

        match self.repetition_type:
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
            case _:
                raise Exception('Invalid repetition_type')

        if self.is_weekly:
            self.column_name = self.prog_column + 'Week'
        else:
            self.column_name = self.prog_column


    def add_entry(self, repetition_info:RepetitionInfo):

        match self.repetition_type:
            case enums.RepetitionType.BeforeTotal:
                prog_name = repetition_info.prog_before
                week = ""
            case enums.RepetitionType.AfterTotal:
                prog_name = repetition_info.prog_after
                week = ""
            case enums.RepetitionType.BeforeWeekly:
                prog_name = repetition_info.prog_before
                week = repetition_info.week
            case enums.RepetitionType.AfterWeekly:
                prog_name = repetition_info.prog_after
                week = repetition_info.week
            case _:
                raise Exception('Invalid column_name and is_weekly combination')
        # żaden program nie ma before pogoda wyjazdowa
        if prog_name != "UNKNOWN":
            if week == "":
                entry_name = prog_name
            else:
                entry_name = f"{prog_name}|{week}"
            self.prog_repetitions_dict[entry_name] += 1

    def check_repetitions(self, df_selection: pd.DataFrame):

        df_unknownFiltered = get_filtered_df(df_selection, [self.prog_column], values=['UNKNOWN'], operations="!=".split())
        repetitions_count = df_unknownFiltered.groupby([self.column_name]).size()
        max_repetitions = self.max_repetitions
        # max_repetitions = 1

        not_fulfilled = repetitions_count[repetitions_count > max_repetitions]
        if len(not_fulfilled) > 0:
            raise Exception(f"{self.repetition_type.value} repetition constraint not fulfilled")
def get_repetitions_checkers( max_repetitions_total:int,max_repetitions_weekly:int, df:pd.DataFrame)->List[RepetitionsChecker]:
    checkers = []
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.BeforeTotal, max_repetitions= max_repetitions_total))
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.AfterTotal, max_repetitions= max_repetitions_total))
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.BeforeWeekly, max_repetitions= max_repetitions_weekly))
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.AfterWeekly, max_repetitions= max_repetitions_weekly))

    for checker in checkers:
        checker.prog_repetitions_dict = {prog: 0 for prog in df[checker.column_name].unique()}

    print (checkers[1].prog_repetitions_dict['Pogoda Wyjazdowa /1'])
    return checkers
