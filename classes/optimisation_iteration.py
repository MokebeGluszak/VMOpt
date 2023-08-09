import dataclasses
from datetime import datetime, timedelta
from typing import List

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
    wanted_ids: List[int] = dataclasses.field(default_factory=list)
    constraint_column_names: List[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.df['available'] = 1
        self.constraint_column_names =  [oi.quantity_constraint.column_name for oi in self.optimisation_items]
    def _recalculate_df_step1(self):
        bonuses: list[float] = [oi.weight_bonus_current for oi in self.optimisation_items]

        self.df['bonusCurrent'] = np.sum(self.df[self.constraint_column_names].values * bonuses, axis=1)
        self.df['grpOpt1'] = self.df['bonusCurrent'] * self.df['grp'] * (self.df['available'])
        self.df['cppOpt1'] = self.df['eqNetPrice'] / self.df['grpOpt1']


    def _recalculate_df_step2(self):
        bonuses: list[float] = [oi.weight_bonus_current for oi in self.optimisation_items]

        # self.df['bonusCurrent'] = np.sum(self.df[self.constraint_column_names].values * bonuses, axis=1)
        self.df['grpOpt2'] = self.df['grp'] * (self.df['available'])
        self.df['cppOpt2'] = self.df['eqNetPrice'] / self.df['grpOpt2']

    def _recalculate_df_step3(self):
        maluses: list[float] = [oi.weight_malus_current for oi in self.optimisation_items]
        self.df['malusCurrent'] = np.sum(self.df[self.constraint_column_names].values * maluses, axis=1)
        self.df['grpOpt3'] = self.df['malusCurrent'] * self.df['grp'] * (self.df['available'])
        self.df['cppOpt1'] = self.df['eqNetPrice'] / self.df['grpOpt1']

    def _get_indexes_banned_by_spot_interval(self, currentIndex: int):
        # Get the dateTime of the row at currentIndex
        # print (type(self.df.loc[currentIndex, 'xDateTime']))
        current_datetime:datetime = self.df.loc[currentIndex, 'xDateTime'] # type: ignore

        # Calculate the range for the search
        # if currentIndex == 11229:
        #     pass
        lower_bound:datetime = current_datetime - timedelta(minutes=self.quality_constraints_def.minSpotInterval)# type: ignore
        upper_bound:datetime = current_datetime + timedelta(minutes=self.quality_constraints_def.minSpotInterval)# type: ignore
        banned:List[int] = []
        # Find the start index by incrementing backwards until the difference is greater than 15 minutes
        start_index = currentIndex
        check_date_time:datetime = current_datetime
        while start_index > 0:
            try:
                check_date_time = self.df.loc[start_index - 1, 'xDateTime']# type: ignore
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
                check_date_time = self.df.loc[end_index + 1, 'xDateTime'] # type: ignore
                if check_date_time > upper_bound:
                    break
                else:
                    banned.append(end_index + 1)
            except:
                pass
            end_index += 1


        return banned

    def _tag_unavailable(self, min_cpp_index: int):
        banned_indexes = self._get_indexes_banned_by_spot_interval(min_cpp_index)
        self.df.loc[banned_indexes, 'available'] = 0

    @property
    def get_cpp(self)->float:
        return self.get_eqNetPrice / self.get_grp

    @property
    def get_grp(self)->float:
        grp_sum = self.df.query('copyNumber == 1')['grp'].sum()
        return grp_sum

    @property
    def get_eqNetPrice(self)->float:

        eqNetPrice_sum = self.df.query('copyNumber == 1')['eqNetPrice'].sum()
        return eqNetPrice_sum
    @property
    def get_info(self):
        info = "I: " + str(self.n_iteration) + " cpp: " + str(round(self.get_cpp)) + " grp: " + str(round(self.get_grp))

        return info

    def __str__(self):
        return self.get_info

    def export_schedule(self):


        log.reset_timer
        optimised_df = self.df_org.copy()
        optimised_df.loc[optimised_df.index.isin(self.wanted_ids), 'copyNumber'] = 1
        optimised_df.to_excel(export_file_path(f'schedule optimisation{self.n_iteration}.xlsx'))
        # filtered_df = self.df[self.df['copyNumber'] == 1]
        # filtered_df.to_excel(export_file_path(f'selected breaks optimisation{self.n_optimisation}.xlsx'))
        log.log("Exporting schedule {self.n_optimisation} done", True)

    def get_constraints_fulfilled(self):
        fulfilled = all(oi.is_fulfilled for oi in self.optimisation_items)
        return fulfilled

    def increment_constraints_fulfillment(self, min_cpp_index):
        grp = self.df.loc[min_cpp_index, 'grp']
        is_ok_vector:List[bool] =  self.df.loc[min_cpp_index, self.constraint_column_names].values.tolist()
        n = 0
        # print (is_ok_vector)
        for is_ok in is_ok_vector:
            if is_ok:
                oi = self.optimisation_items[n]
                oi.grp += grp
                if oi.grp > oi.quantity_constraint.min_grp:
                    oi.is_fulfilled = True
            n += 1
        pass
    def run_part1_fulfillConstraints(self, copy_number: int):
        log.reset_timer()
        self.df['order'] = 0
        constraints_fulfilled:bool = False
        n = 1
        while not constraints_fulfilled:
            self._recalculate_df_step1()
            min_cpp_index:int= self.df['cppOpt'].idxmin()# type: ignore
            self.pick_up_spot(min_cpp_index, copy_number, n)

            self.increment_constraints_fulfillment(min_cpp_index)
            # if n == 500:
            #     pass
            constraints_fulfilled = self.get_constraints_fulfilled()
            n +=1
            # print(n)
        log.log(f"Part 1 done, {n} iterations. {self.get_info}", True)

    def run_part2_fulfillTotal(self, copy_number):
        log.reset_timer()
        self.df['cpp_opt2'] = self.df['eqNetPrice'] / (self.df['grp'] * self.df['available'])
        self.df.sort_values(by=['cpp_opt2'], inplace=True)
        grp_sum = self.get_grp
        n = self.df.query(f'copyNumber == {copy_number}')['order'].max()+1

        while grp_sum < self.desired_grp:
            self._recalculate_df_step2()
            min_cpp_index:int= self.df['cppOpt2'].idxmin()# type: ignore

            self.pick_up_spot(min_cpp_index, copy_number,n)
            grp_sum += self.df.loc[min_cpp_index, 'grp']
            n += 1
            if n == len(self.df):
                raise Exception("Not enough breaks to fulfill total grp")

        log.log(f"Part 2 done, {n} breaks added. " + self.get_info , True)

    def pick_up_spot(self, index:int, copy_number:int, order:int):
        self.wanted_ids.append(index)
        self._tag_unavailable(index)
        self.df.loc[index, 'available'] = 0
        self.df.loc[index, 'order'] = order
        self.df.loc[index, 'copyNumber'] = copy_number

    def run_part3_decrement(self, copy_number):
        grp_sum = self.get_grp
        while grp_sum > self.desired_grp:
            self._recalculate_df_step2
            min_cpp_index:int= self.df['cppOpt3'].idxmin()
        increment_constraints_fulfillment


def get_optimisation_items(quantity_constraints: List[QuantityConstraint]) -> List[OptimisationItem]:
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
        desired_grp:float
) -> OptimisationIteration:
    ois = get_optimisation_items(optimisation_items)
    optimisation = OptimisationIteration( df_org, df.copy(),n_iteration, ois, quality_constraints_def, desired_grp)
    return optimisation
