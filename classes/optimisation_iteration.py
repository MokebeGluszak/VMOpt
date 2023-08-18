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
from classes.result_folder import export_file_path


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
    banned_progs_dict_before_total: dict = dataclasses.field(default_factory=dict)
    banned_progs_dict_after_total: dict = dataclasses.field(default_factory=dict)
    banned_progs_dict_before_weekly: dict = dataclasses.field(default_factory=dict)
    banned_progs_dict_after_weekly: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.df["available"] = 1
        self.constraint_column_names = [
            oi.quantity_constraint.column_name for oi in self.optimisation_items
        ]



        self.banned_progs_dict_before_total = {prog: 0 for prog in self.df['progBefore'].unique()}
        self.banned_progs_dict_after_total = {prog: 0 for prog in self.df['progAfter'].unique()}
        self.banned_progs_dict_before_weekly = {prog: 0 for prog in self.df['progBeforeWeek'].unique()}
        self.banned_progs_dict_after_weekly = {prog: 0 for prog in self.df['progAfterWeek'].unique()}

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
        bonuses: list[float] = [
            oi.weight_bonus_current for oi in self.optimisation_items
        ]

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

    def _get_indexes_banned_by_spot_interval(self, currentIndex: int):
        # Get the dateTime of the row at currentIndex
        # print (type(self.df.loc[currentIndex, 'xDateTime']))
        current_datetime: datetime = self.df.loc[currentIndex, "xDateTime"]  # type: ignore

        # Calculate the range for the search
        # if currentIndex == 11229:
        #     pass
        lower_bound: datetime = current_datetime - timedelta(minutes=self.quality_constraints_def.minSpotInterval)  # type: ignore
        upper_bound: datetime = current_datetime + timedelta(minutes=self.quality_constraints_def.minSpotInterval)  # type: ignore
        banned: List[int] = []
        # Find the start index by incrementing backwards until the difference is greater than 15 minutes
        start_index = currentIndex
        check_date_time: datetime = current_datetime
        while start_index > 0:
            try:
                check_date_time = self.df.loc[start_index - 1, "xDateTime"]  # type: ignore
                if check_date_time < lower_bound:
                    break
                else:
                    banned.append(start_index - 1)
            except:
                pass
            start_index -= 1

        # Find the end index by incrementing forwards until the difference is greater than 15 minutes
        end_index = currentIndex
        check_date_time = current_datetime
        # print(self.df.index.dtype)
        max_index = self.df.index.max()
        while end_index < max_index - 1:
            try:
                check_date_time = self.df.loc[end_index + 1, "xDateTime"]  # type: ignore
                if check_date_time > upper_bound:
                    break
                else:
                    banned.append(end_index + 1)
            except:
                pass
            end_index += 1

        return banned

    def _tag_unavailable(self, min_cpp_index: int):
        # to taguje tylko te kture zostały zbanowane przy dobraniu tego spota
        banned_indexes_interval: list[int] = self._get_indexes_banned_by_spot_interval(min_cpp_index)
        banned_indexes_repetition:list[int] = self._get_indexes_banned_by_repetitions(min_cpp_index)

        banned_indexes_all = banned_indexes_interval + banned_indexes_repetition
        self.df.loc[banned_indexes_all, "available"] = 0

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
            self.change_constraints_fulfillment(
                min_cpp_index, enums.BlockOperation.PickUp
            )
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
            # self.pick_up_spot(min_cpp_index, copy_number,n)
            # grp_sum += self.df.loc[min_cpp_index, 'grp']# type: ignore
            self.pick_up_spot(min_cpp_index, copy_number, n)  # type: ignore
            grp_sum += self.df.loc[min_cpp_index, "grp"]  # type: ignore
            n += 1
            if n == len(self.df):
                raise Exception("Not enough breaks to fulfill total grp")
        log.log(f"Part 2 done, {n-n_start} breaks added. " + self.get_info, True)

    def run_part3_decrement(self, copy_number):
        log.reset_timer()
        grp_sum = self.get_grp
        n = 0

        self.df["dropable"] = self.df["copyNumber"].apply(
            lambda x: 1 if x == copy_number else 0
        )
        while grp_sum > self.desired_grp:
            n += 1
            self._recalculate_df_step3()
            min_cpp_index: int = int(self.df["cppOpt3"].idxmin())

            grp = self.df.loc[min_cpp_index, "grp"]
            try:
                self.wanted_indexes.remove(min_cpp_index)
            except KeyError:
                pass
            self.change_constraints_fulfillment(
                min_cpp_index, enums.BlockOperation.Drop
            )
            if self.get_constraints_fulfilled():
                self.df.loc[
                    min_cpp_index, "dropable"
                ] = 0  # jak go usunąłeś to nie możesz jeszcze raz
                self.df.loc[min_cpp_index, "copyNumber"] = 0
                grp_sum -= grp  # type: ignore
            else:
                self.df.loc[
                    min_cpp_index, "dropable"
                ] = 0  # jak nie możesz usunąć to nie możesz
                self.wanted_indexes.add(min_cpp_index)
                self.change_constraints_fulfillment(
                    min_cpp_index, enums.BlockOperation.PickUp
                )

        if n > 0:  # jeśli coś usunąłeś to musisz dodać ostatni spota
            self.df.loc[min_cpp_index, "copyNumber"] = 0

        log.log(f"Part 3 done, {n} breaks dropped. {self.get_info}", True)

    def pick_up_spot(self, index: int, copy_number: int, order: int):
        self.wanted_indexes.add(index)
        self._tag_unavailable(index)
        self.df.loc[index, "available"] = 0
        self.df.loc[index, "order"] = order
        self.df.loc[index, "copyNumber"] = copy_number

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
# prog after total
        prog_after_counts = filtered_df[filtered_df['progAfter'] != "UNKNOWN"]["progAfter"].value_counts()
        not_fulfilled_prog_after_total = prog_after_counts[prog_after_counts > self.quality_constraints_def.maxRepetitionsTotal]
        if len(not_fulfilled_prog_after_total) > 0:
            raise Exception(f"ProgAfter total not fulfilled")
# prog before total
        prog_before_counts = filtered_df[filtered_df['progBefore'] != "UNKNOWN"]["progBefore"].value_counts()
        not_fulfilled_prog_before_total = prog_before_counts[prog_before_counts > self.quality_constraints_def.maxRepetitionsTotal]
        if len(not_fulfilled_prog_before_total) > 0:
            raise Exception(f"ProgBefore total not fulfilled")
#  prog after week
        prog_after_week_counts = filtered_df[filtered_df['progAfter'] != "UNKNOWN"].groupby(["progAfter", "week"]).size()
        not_fulfilled_prog_after_week = prog_after_week_counts[prog_after_week_counts > self.quality_constraints_def.maxRepetitionsWeekly]
        if len(not_fulfilled_prog_after_week) > 0:
            raise Exception(f"ProgAfter week not fulfilled")
# prog before week
        prog_before_week_counts = filtered_df[filtered_df['progBefore'] != "UNKNOWN"].groupby(["progBefore", "week"]).size()
        not_fulfilled_prog_before_week = prog_before_week_counts[prog_before_week_counts > self.quality_constraints_def.maxRepetitionsWeekly]
        if len(not_fulfilled_prog_before_week) > 0:
            raise Exception(f"ProgBefore week not fulfilled")

    # grouped_counts = filtered_df[filtered_df['progBefore'] != "UNKNOWN"].groupby(["progBefore", "week"]).size()
    def _get_indexes_banned_by_repetitions(self, min_cpp_index):
        prog_before = self.df.loc[min_cpp_index, "progBefore"]
        prog_after = self.df.loc[min_cpp_index, "progAfter"]
        week = self.df.loc[min_cpp_index, "week"]
        prog_before_week = prog_before + week
        prog_after_week = prog_after + week
        self.banned_progs_dict_before_total[prog_before] = self.banned_progs_dict_before_total[prog_before] +1
        self.banned_progs_dict_after_total[prog_after] = self.banned_progs_dict_after_total[prog_after] +1
        self.banned_progs_dict_before_weekly[prog_before_week] = self.banned_progs_dict_before_weekly[prog_before_week] +1
        self.banned_progs_dict_after_weekly[prog_after_week] = self.banned_progs_dict_after_weekly[prog_after_week] +1

        banned_ids = []
        inc = []
        if prog_before != "UNKNOWN":
            if self.banned_progs_dict_before_total[prog_before] == self.quality_constraints_def.maxRepetitionsTotal:
                inc = self.df[self.df["progBefore"] == prog_before].index.tolist()
                banned_ids = banned_ids + inc
            if self.banned_progs_dict_before_weekly[prog_before_week] == self.quality_constraints_def.maxRepetitionsWeekly:
                prog_before_week = prog_before + week
                inc = self.df[self.df["progBeforeWeek"] == prog_before_week].index.tolist()
                banned_ids = banned_ids + inc

        if prog_after != "UNKNOWN":
            if self.banned_progs_dict_after_total[prog_after] == self.quality_constraints_def.maxRepetitionsTotal:
                inc = self.df[self.df["progAfter"] == prog_after].index.tolist()
                banned_ids = banned_ids + inc

            if self.banned_progs_dict_after_weekly[prog_after_week] == self.quality_constraints_def.maxRepetitionsWeekly:
                prog_after_week = prog_after + week
                inc = self.df[self.df["progAfterWeek"] == prog_after_week].index.tolist()
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
