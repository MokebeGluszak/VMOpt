import pandas as pd
from typing import Union
import classes.log as log
from classes.schedule import get_schedule
import zzz_enums as enums

# def get_df_max_index_copy(
#     df: pd.DataFrame,
#     column: str,
#     filter_column: str,
#     filter_value: Union[int, float]
# ) -> Union[int, None]:
#     if df.empty:
#         return -1  # Return -1 if the DataFrame is empty
#
#     # Apply the filter condition to the DataFrame
#     filtered_df = df[df[filter_column] == filter_value]
#
#     if filtered_df.empty:
#         return -1  # Return -1 if the filtered DataFrame is empty
#
#     max_index = filtered_df[column].idxmax()  # Get the index of the maximum value in the specified column
#     return max_index
#
#
# def get_df_max_index_noCopy(
#     df: pd.DataFrame,
#     column: str,
#     filter_column: str,
#     filter_value: Union[int, float]
# ) -> Union[int, None]:
#     if df.empty:
#         return -1  # Return -1 if the DataFrame is empty
#
#     max_index = None
#     max_value = float('-inf')  # Initialize max_value with negative infinity
#
#     for index, row in df.iterrows():
#         if row[filter_column] == filter_value and row[column] > max_value:
#             max_index = index
#             max_value = row[column]
#
#     if max_index is not None:
#         return max_index
#     else:
#         return -1  # Return -1 if no matching row is found or if the DataFrame is empty
#
#
# def get_df_max_index_numpy(
#     df: pd.DataFrame,
#     column: str,
#     filter_column: str,
#     filter_value: Union[int, float]
# ) -> Union[int, None]:
#     if df.empty:
#         return -1  # Return -1 if the DataFrame is empty
#
#     # Convert the DataFrame to a Numpy array for faster computation
#     data = df.to_numpy()
#
#     max_index = None
#     max_value = float('-inf')  # Initialize max_value with negative infinity
#
#     # Iterate through the Numpy array
#     for index, row in enumerate(data):
#         if row[df.columns.get_loc(filter_column)] == filter_value and row[df.columns.get_loc(column)] > max_value:
#             max_index = index
#             max_value = row[df.columns.get_loc(column)]
#
#     if max_index is not None:
#         return max_index
#     else:
#         return -1  # Return -1 if no matching row is found or if the DataFrame is empty
#
#
# schedule = get_schedule(enums.ScheduleType.BIG)
# log.reset_timer
# log.log_header("Test")
# for n in range(1, 100):
#     id = get_df_max_index_numpy(schedule.df, "ratecard", "channel", "Polsat")
#     # id = get_df_max_index_copy(schedule.df, "ratecard", "channel", "Polsat")
#     # id = get_df_max_index_noCopy(schedule.df, "ratecard", "channel", "Polsat")
# log.log(f"{n} iterations")
# log.print_log()