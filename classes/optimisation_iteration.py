import dataclasses
from datetime import datetime, timedelta
from typing import List, Set

import pandas as pd
from numpy import datetime64

import zzz_enums as enums
import classes.log as log
import numpy as np
from classes.optimisation_item import OptimisationItem, get_optimisation_item
from classes.quality_constraints_def import QualityConstraintsDef
from classes.quantity_constraint import QuantityConstraint
from classes.repetition_info import RepetitionInfo
from classes.repetitions_checker import RepetitionsChecker, get_repetitions_checkers
from classes.result_folder import export_file_path
from zzz_const import MODE_DEBUG


@dataclasses.dataclass
class OptimisationIteration:
    df_org: pd.DataFrame
    df: pd.DataFrame
    n_iteration: int
    optimisation_items: List[OptimisationItem]
    quality_constraints_def: QualityConstraintsDef
    desired_grp: float
    wanted_indexes: Set[int] = dataclasses.field(default_factory=set)
    constraint_column_names: List[str] = dataclasses.field(default_factory=list)
    repetition_checkers: List[RepetitionsChecker] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.df["available"] = 1
        self.constraint_column_names = [
            oi.quantity_constraint.column_name for oi in self.optimisation_items
        ]
        self.repetition_checkers =  get_repetitions_checkers(self.quality_constraints_def.maxRepetitionsTotal,self.quality_constraints_def.maxRepetitionsWeekly, self.df)




    def _recalculate_df_step1(self):
        bonuses: list[float] = [
            oi.weight_bonus_current for oi in self.optimisation_items
        ]

        self.df["bonusCurrent1"] = np.sum(
            self.df[self.constraint_column_names].values * bonuses, axis=1
        )
        self.df["grpOpt1"] = (
            self.df["bonusCurrent1"] * self.df["grp"] * (self.df["available"])
        )
        self.df["cppOpt1"] = self.df["eqNetPrice"] / self.df["grpOpt1"]

    def _recalculate_df_step2(self):
        # bonuses: list[float] = [
        #     oi.weight_bonus_current for oi in self.optimisation_items
        # ]

        # self.df['bonusCurrent'] = np.sum(self.df[self.constraint_column_names].values * bonuses, axis=1)
        self.df["grpOpt2"] = self.df["grp"] * (self.df["available"])
        self.df["cppOpt2"] = self.df["eqNetPrice"] / self.df["grpOpt2"]

    def _recalculate_df_step3(self):
        maluses: list[float] = [
            oi.weight_malus_current for oi in self.optimisation_items
        ]
        self.df["malusCurrent3"] = np.sum(
            self.df[self.constraint_column_names].values * maluses, axis=1
        )
        self.df["grpOpt3"] = (
            self.df["malusCurrent3"] * self.df["grp"] * (self.df["dropable"])
        )
        self.df["cppOpt3"] = self.df["eqNetPrice"] / self.df["grpOpt3"]

    def _get_indexes_banned_by_spot_interval(self, currentIndex: int) -> List[int]:
        current_datetime = self.df.loc[currentIndex, "xDateTime"]
        current_channel = self.df.loc[currentIndex, "channel"]
        min_spot_interval = self.quality_constraints_def.minSpotInterval

        lower_bound = current_datetime - timedelta(minutes=min_spot_interval) # type: ignore
        upper_bound = current_datetime + timedelta(minutes=min_spot_interval) # type: ignore

        def find_banned_indices(start_index: int, step: int) -> List[int]:
            banned_indices = []
            max_index = self.df.index.max()

            while 0 <= start_index < max_index:
                try:
                    check_date_time = self.df.loc[start_index + step, "xDateTime"]
                    check_channel = self.df.loc[start_index + step, "channel"]

                    if step < 0 and (check_date_time < lower_bound or check_channel != current_channel): # type: ignore
                        break
                    elif step > 0 and (check_date_time > upper_bound or check_channel != current_channel): # type: ignore
                        break
                    else:
                        banned_indices.append(start_index + step)
                except:
                    pass

                start_index += step

            return banned_indices

        banned_indices = find_banned_indices(currentIndex, -1) + find_banned_indices(currentIndex, 1)
        return banned_indices

    # def _get_indexes_banned_by_spot_interval(self, currentIndex: int):
    #     # Get the dateTime of the row at currentIndex
    #     # print (type(self.df.loc[currentIndex, 'xDateTime']))
    #     current_datetime: datetime = self.df.loc[currentIndex, "xDateTime"]  # type: ignore
    #     current_channel: str = self.df.loc[currentIndex, "channel"]  # type: ignore
    #     # Calculate the range for the search
    #     # if currentIndex == 11229:
    #     #     pass
    #     lower_bound: datetime = current_datetime - timedelta(minutes=self.quality_constraints_def.minSpotInterval)  # type: ignore
    #     upper_bound: datetime = current_datetime + timedelta(minutes=self.quality_constraints_def.minSpotInterval)  # type: ignore
    #     banned: List[int] = []
    #     # Find the start index by incrementing backwards until the difference is greater than 15 minutes
    #     start_index = currentIndex
    #     while start_index > 0:
    #         try:
    #             check_date_time = self.df.loc[start_index - 1, "xDateTime"]  # type: ignore
    #             check_channel: str = self.df.loc[start_index - 1, "channel"]  # type: ignore
    #             if check_date_time < lower_bound:
    #                 break
    #             elif check_channel != current_channel:
    #                 break
    #             else:
    #                 banned.append(start_index - 1)
    #         except:
    #             pass
    #         start_index -= 1
    #
    #     # Find the end index by incrementing forwards until the difference is greater than 15 minutes
    #     end_index = currentIndex
    #
    #
    #     # print(self.df.index.dtype)
    #     max_index = self.df.index.max()
    #     while end_index < max_index - 1:
    #         try:
    #             check_date_time = self.df.loc[end_index + 1, "xDateTime"]  # type: ignore
    #             check_channel: str = self.df.loc[end_index + 1, "channel"]  # type: ignore
    #             if check_date_time > upper_bound:
    #                 break
    #             elif check_channel != current_channel:
    #                 break
    #             else:
    #                 banned.append(end_index + 1)
    #         except:
    #             pass
    #         end_index += 1
    #
    #     return banned

    def _tag_unavailable(self, min_cpp_index: int):
        # to taguje tylko te kture zostały zbanowane przy dobraniu tego spota
        banned_indexes_interval: list[int] = self._get_indexes_banned_by_spot_interval(min_cpp_index) # type: ignore
        prog_before:str = self.df.loc[min_cpp_index, "progBefore"]# type: ignore
        prog_after:str = self.df.loc[min_cpp_index, "progAfter"]# type: ignore
        week:str = self.df.loc[min_cpp_index, "week"]# type: ignore
        repetition_info:RepetitionInfo = RepetitionInfo(prog_before, prog_after, week)
        banned_indexes_repetition:list[int] = self._get_indexes_banned_by_repetitions(repetition_info)
        # if len(banned_indexes_repetition) > 100:
        #     print (len(banned_indexes_repetition))



        banned_indexes_all = banned_indexes_interval + banned_indexes_repetition
        self.df.loc[banned_indexes_all, "available"] = 0
        if MODE_DEBUG:
            self.df.loc[banned_indexes_all, "bannedBy"] = min_cpp_index
            self.df.loc[banned_indexes_interval, "bannedReason"] = "interval"
            self.df.loc[banned_indexes_repetition, "bannedReason"] = "repetition"

    @property
    def get_cpp(self) -> float:
        return self.get_eqNetPrice / self.get_grp

    @property
    def get_grp(self) -> float:
        grp_sum = self.df.query("copyNumber == 1")["grp"].sum()
        return grp_sum

    @property
    def get_eqNetPrice(self) -> float:
        eqNetPrice_sum = self.df.query("copyNumber == 1")["eqNetPrice"].sum()
        return eqNetPrice_sum

    @property
    def get_info(self):
        grp_str = str(round(self.get_grp))
        cpp_str = str(round(self.get_cpp))
        info = "I: " + str(self.n_iteration) + " cpp: " + cpp_str + " grp: " + grp_str

        return info

    def __str__(self):
        return self.get_info

    def export_schedule(self):
        log.reset_timer
        optimised_df = self.df_org.copy()
        optimised_df.loc[optimised_df.index.isin(self.wanted_indexes), "copyNumber"] = 1
        optimised_df.to_excel(
            export_file_path(f"schedule optimisation{self.n_iteration}.xlsx")
        )
        # filtered_df = self.df[self.df['copyNumber'] == 1]
        # filtered_df.to_excel(export_file_path(f'selected breaks optimisation{self.n_optimisation}.xlsx'))
        log.log("Exporting schedule {self.n_optimisation} done", True)

    def get_constraints_fulfilled(self):
        fulfilled = all(oi.is_fulfilled for oi in self.optimisation_items)
        return fulfilled

    def change_constraints_fulfillment(
        self, min_cpp_index: int, block_operation: enums.BlockOperation
    ):
        grp: float = self.df.loc[min_cpp_index, "grp"]  # type: ignore
        is_ok_vector: List[bool] = self.df.loc[min_cpp_index, self.constraint_column_names].values.tolist()  # type: ignore
        n = 0
        # print (is_ok_vector)
        for is_ok in is_ok_vector:
            if is_ok:
                oi = self.optimisation_items[n]
                if block_operation == enums.BlockOperation.PickUp:
                    oi.grp += grp
                elif block_operation == enums.BlockOperation.Drop:
                    oi.grp -= grp

                if oi.grp > oi.quantity_constraint.min_grp:
                    oi.is_fulfilled = True
            n += 1
        pass

    def run_part1_fulfillConstraints(self, copy_number: int):
        log.reset_timer()
        self.df["order"] = 0
        constraints_fulfilled: bool = False
        n = 1
        while not constraints_fulfilled:
            self._recalculate_df_step1()
            min_cpp_index: int = self.df["cppOpt1"].idxmin()  # type: ignore

            self.pick_up_spot(min_cpp_index, copy_number, n)
            self.change_constraints_fulfillment( min_cpp_index, enums.BlockOperation.PickUp)
            # if n == 500:
            #     pass
            constraints_fulfilled = self.get_constraints_fulfilled()
            n += 1
            if self.df.loc[min_cpp_index, "cppOpt1"] == np.inf:
                raise Exception("No more breaks to fulfill constraints")
        log.log(f"Part 1 done, {n} iterations. {self.get_info}", True)

    def run_part2_fulfillTotal(self, copy_number):
        log.reset_timer()

        grp_sum = self.get_grp
        n = self.df.query(f"copyNumber == {copy_number}")["order"].max() + 1
        n_start = n
        while not grp_sum > self.desired_grp:
            self._recalculate_df_step2()
            min_cpp_index = self.df["cppOpt2"].idxmin()  # type: ignore
            if self.df.loc[min_cpp_index, "cppOpt2"] == np.inf:
                self.df.to_excel(export_file_path(f"part2 break.xlsx"))
                raise Exception("Not enough breaks to fulfill total grp")
            if min_cpp_index == 202:
                pass

            self.pick_up_spot(min_cpp_index, copy_number, n)  # type: ignore
            grp_sum += self.df.loc[min_cpp_index, "grp"]  # type: ignore

            n += 1

        log.log(f"Part 2 done, {n-n_start} breaks added. " + self.get_info, True)

    def run_part3_decrement(self, copy_number:int):
        log.reset_timer()
        grp_sum:float = self.get_grp
        n = 0

        self.df["dropable"] = self.df["copyNumber"].apply(
            lambda x: 1 if x == copy_number else 0
        )
        zrobić żeby brał najwyższe cpp ale nie licząc inf
        while grp_sum > self.desired_grp:
            n += 1
            self._recalculate_df_step3()
            max_cpp_index: int = int(self.df["cppOpt3"].idxmax())
            if self.df.loc[max_cpp_index, "cppOpt3"] == np.inf:
                raise Exception("Cannot limit grp to desired value without unfulfilling constraints")
            grp = self.df.loc[max_cpp_index, "grp"]
            try:
                self.wanted_indexes.remove(max_cpp_index)
            except KeyError:
                pass
            self.change_constraints_fulfillment(max_cpp_index, enums.BlockOperation.Drop)
            if self.get_constraints_fulfilled():
                self.drop_spot(max_cpp_index, copy_number)
                grp_sum -= grp # type: ignore
            else:
                self.drop_spot(max_cpp_index, copy_number)
                self.df.loc[max_cpp_index, "dropable"] = 0  # jak nie możesz usunąć to nie możesz
                self.wanted_indexes.remove(max_cpp_index)
                self.change_constraints_fulfillment(max_cpp_index, enums.BlockOperation.PickUp)

        if n > 0:  # jeśli coś usunąłeś to musisz dodać ostatni spota
            self.df.loc[max_cpp_index, "copyNumber"] = copy_number

        log.log(f"Part 3 done, {max(0, n-1)} breaks dropped. {self.get_info}", True)

    def pick_up_spot(self, index: int, copy_number: int, order: int):
        if self.df.loc[index, "copyNumber"] != 0:
            raise Exception(f"This spot ({index}) is already picked up")
        self.wanted_indexes.add(index)
        self._tag_unavailable(index)
        self.df.loc[index, "available"] = 0
        self.df.loc[index, "order"] = order
        self.df.loc[index, "copyNumber"] = copy_number


    def drop_spot(self, index:int, copy_number:int):
        if self.df.loc[index, "copyNumber"] != copy_number:
            raise Exception(f"This spot ({index}) is already dropped")
        else:
            self.df.loc[index, "dropable"] = 0  # jak go usunąłeś to nie możesz jeszcze raz
            self.df.loc[index, "copyNumber"] = 0

    def check_result(self, copy_number):
        filtered_df = self.df[self.df["copyNumber"] == copy_number]

        sorted_df = filtered_df.sort_values(by=["channel", "xDateTime"])
        sorted_df["time_diff"] = sorted_df.groupby("channel")["xDateTime"].diff()
# interval
        not_fulfilled_interval = sorted_df[
            sorted_df["time_diff"]
            < pd.Timedelta(minutes=self.quality_constraints_def.minSpotInterval)
        ]
        if len(not_fulfilled_interval) > 0:
            raise Exception(f"There are spot with time interval not fulfilled")
# min grp
        not_fulfilled_min_grp = filtered_df[
            filtered_df["grp"] < self.quality_constraints_def.minGrp
        ]
        if not_fulfilled_min_grp.shape[0] > 0:
            raise Exception(f"There are spot with grp not fulfilled")

# repetitions
        df_selection:pd.DataFrame = filtered_df[filtered_df['copyNumber'] != 0]
        for repetitions_checker in self.repetition_checkers:
            repetitions_checker.check_repetitions(df_selection)




# # prog after total
#         prog_after_counts = filtered_df[filtered_df['progAfter'] != "UNKNOWN"]["progAfter"].value_counts()
#         not_fulfilled_prog_after_total = prog_after_counts[prog_after_counts > self.quality_constraints_def.maxRepetitionsTotal]
#         if len(not_fulfilled_prog_after_total) > 0:
#             raise Exception(f"ProgAfter total not fulfilled")
# # prog before total
#         prog_before_counts = filtered_df[filtered_df['progBefore'] != "UNKNOWN"]["progBefore"].value_counts()
#         not_fulfilled_prog_before_total = prog_before_counts[prog_before_counts > self.quality_constraints_def.maxRepetitionsTotal]
#         if len(not_fulfilled_prog_before_total) > 0:
#             raise Exception(f"ProgBefore total not fulfilled")
# #  prog after week
#         prog_after_week_counts = filtered_df[filtered_df['progAfter'] != "UNKNOWN"].groupby(["progAfter", "week"]).size()
#         not_fulfilled_prog_after_week = prog_after_week_counts[prog_after_week_counts > self.quality_constraints_def.maxRepetitionsWeekly]
#         if len(not_fulfilled_prog_after_week) > 0:
#             raise Exception(f"ProgAfter week not fulfilled")
# # prog before week
#         prog_before_week_counts = filtered_df[filtered_df['progBefore'] != "UNKNOWN"].groupby(["progBefore", "week"]).size()
#         not_fulfilled_prog_before_week = prog_before_week_counts[prog_before_week_counts > self.quality_constraints_def.maxRepetitionsWeekly]
#         if len(not_fulfilled_prog_before_week) > 0:
#             raise Exception(f"ProgBefore week not fulfilled")

    # grouped_counts = filtered_df[filtered_df['progBefore'] != "UNKNOWN"].groupby(["progBefore", "week"]).size()
    def _get_indexes_banned_by_repetitions(self, rep_info: RepetitionInfo):
        banned_ids:List[int] = []
        repetitions_checker:RepetitionsChecker
        for repetitions_checker in self.repetition_checkers:
            repetitions_checker.add_entry(rep_info)
            entry_name  =  rep_info.get_proper_entry_name(repetitions_checker.repetition_type)
            repetitions_count = repetitions_checker.prog_repetitions_dict[entry_name]
            if repetitions_count == repetitions_checker.max_repetitions: # jeżeli osiągnąłeś limit
                inc = self.df[self.df[repetitions_checker.column_name] == entry_name].index.tolist()         # co z jednej strony mają ten program/tydzień są banowani
                banned_ids = banned_ids + inc
        return banned_ids





def get_optimisation_items(
    quantity_constraints: List[QuantityConstraint],
) -> List[OptimisationItem]:
    ois = []
    for quantity_constraint in quantity_constraints:
        oi = get_optimisation_item(quantity_constraint)
        ois.append(oi)
    return ois


def get_optimisation_iteration(
    df_org: pd.DataFrame,
    df: pd.DataFrame,
    n_iteration: int,
    optimisation_items: List[QuantityConstraint],
    quality_constraints_def: QualityConstraintsDef,
    desired_grp: float,
) -> OptimisationIteration:
    ois = get_optimisation_items(optimisation_items)
    optimisation = OptimisationIteration(
        df_org, df.copy(), n_iteration, ois, quality_constraints_def, desired_grp
    )
    return optimisation
