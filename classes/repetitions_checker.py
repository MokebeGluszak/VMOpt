import dataclasses
from typing import Dict, List

import pandas as pd

import zzz_enums as enums
from classes.log import log, log_header
from classes.repetition_info import RepetitionInfo
# from zzz_optToolz import clear_string
from zzz_tools import get_filtered_df





@dataclasses.dataclass
class RepetitionsChecker():
    repetition_type: enums.RepetitionType
    max_repetitions:int
    _prog_repetitions_dict:Dict[str, int] = dataclasses.field(init=False, default_factory=dict)

    def __post_init__(self):

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

    @property
    def prog_repetitions_dict(self):
        return self._prog_repetitions_dict

    @prog_repetitions_dict.setter
    def prog_repetitions_dict(self, value):
        self._prog_repetitions_dict = value
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
        # prog_name_cleared = clear_string(prog_name)
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



def get_repetitions_checkers(max_repetitions_total:int, max_repetitions_weekly:int, df:pd.DataFrame)->List[RepetitionsChecker]:
    # tu jest błąd ktury zapewne nigdy się nie objawi - w tym df są odfiltrowane te brejki któe są wyłączone. i one nie wliczają się do repetitions nawet jakby były wybrane (nie wiem, ktoś ręcnzie wybrał a potem zabanował tydzień)
    checkers = []
    prog_repetitions_dict:Dict[str, int]
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.AfterTotal, max_repetitions= max_repetitions_total))
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.BeforeTotal, max_repetitions= max_repetitions_total))
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.BeforeWeekly, max_repetitions= max_repetitions_weekly))
    checkers.append (RepetitionsChecker(repetition_type=enums.RepetitionType.AfterWeekly, max_repetitions= max_repetitions_weekly))

    for checker in checkers:
        checker.prog_repetitions_dict = get_repetitions_dict(df, checker.column_name)
    return checkers


def get_repetitions_dict(df: pd.DataFrame, prog_column_name:str):
    # dict:Dict[str, int] = df.groupby(prog_column_name)['copyNumber'].apply(lambda x: (x > 0).sum()).to_dict()
    dict: Dict[str, int] = df.groupby(prog_column_name)['copyNumber'].apply(lambda x: 0).to_dict() # repetitions na każdą kopię osobno
    return dict