import collections
import datetime
import datetime as dt
import functools
import os
import tkinter as tk
from enum import Enum
from typing import List, Union, Any, Set, Type, Dict

import pandas as pd

import zzz_const as CONST
import zzz_enums as enum
from classes.exceptions import MyProgramException
from classes.file import File, get_file
from classes.folder import get_folder



class GluDfDebugMode(Enum):
    Nothing = "Nothing"
    ShowFilePath = "ShowFilePath"
    ShowFolderPath = "ShowFolderPath"
    PrintFolderPath = "PrintFolderPath"
    OpenExcel = "OpenExcel"


class MsgboxBoxButtons(Enum):
    OK = 0x00000000
    OK_CANCEL = 0x00000001
    ABORT_RETRY_IGNORE = 0x00000002
    YES_NO_CANCEL = 0x00000003
    YES_NO = 0x00000004
    RETRY_CANCEL = 0x00000005

def singleton(cls):
    instance = None

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper
class MsgBoxIcon(Enum):
    NONE = 0x00000000
    INFORMATION = 0x00000040
    QUESTION = 0x00000020
    WARNING = 0x00000030
    ERROR = 0x00000010


class MsgBoxResult(Enum):
    OK = 1
    CANCEL = 2
    ABORT = 3
    RETRY = 4
    IGNORE = 5
    YES = 6
    NO = 7
def get_cannon_columns_set(cannon_columns_set: enum.CannonColumnsSet) -> Set[str]:
    set_booking_org = set("blockId dateTime channel_org ratecard".split())
    set_booking_processed = set_booking_org | set("channel supplier channelGroup tbId subcampaign_org".split())
    set_scheduleMatching = set("blockId dateTime channel ratecard wantedness tbId1 tbId2 bookedness".split())
    set_scheduleOrg = set(
        "blockId	channel	programme blockType_org	blockType_mod xDate	xTime ratecard freeTime	week timeband wantedness bookedness	eqPriceNet grpTg_01 grpTg_02 grpTg_50 grpTg_98 grpTg_99 positionCode".split()
    )
    set_scheduleFull = set(set_scheduleOrg | set_scheduleMatching)

    my_set: set[str]

    if cannon_columns_set == enum.CannonColumnsSet.ScheduleOrg:
        my_set = set_scheduleOrg
    elif cannon_columns_set == enum.CannonColumnsSet.BookingProcessed:
        my_set = set_booking_processed
    elif cannon_columns_set == enum.CannonColumnsSet.ScheduleMatching:
        my_set = set_scheduleMatching
    elif cannon_columns_set == enum.CannonColumnsSet.ScheduleProcessedFull:
        my_set = set_scheduleFull
    elif cannon_columns_set == enum.CannonColumnsSet.Matching:
        my_set = set_booking_processed | set_scheduleMatching
    elif cannon_columns_set == enum.CannonColumnsSet.DoNotCheck:
        my_set = set()
    else:
        raise ValueError(f"Wrong cannon columns set: {cannon_columns_set}")

    return my_set


def get_substring_between_parentheses(input_str):
    start_index = input_str.find("(") + 1  # Find the index of the opening parenthesis and add 1 to skip it
    end_index = input_str.rfind(")")  # Find the index of the closing parenthesis

    inner_str = input_str[start_index:end_index]
    return inner_str


def inputBox(prompt, default_value=""):
    window = tk.Tk()
    window.title("Input Box")

    # Create the label and input field
    label = tk.Label(window, text=prompt)
    label.pack()

    input_var = tk.StringVar(value=default_value)
    input_field = tk.Entry(window, textvariable=input_var)
    input_field.pack(fill="x")
    input_field.update()
    input_field.config(width=input_field.winfo_width())

    # Select the text in the input field
    input_field.selection_range(0, "end")

    # Create the OK button
    def get_input():
        input_value = input_var.get()
        window.destroy()
        return input_value

    ok_button = tk.Button(window, text="OK", command=get_input)
    ok_button.pack()

    # Make the window modal
    window.focus_set()
    window.grab_set()
    input_field.focus_set()
    window.wait_window()

    # Return the user input
    return input_var.get()


def msgBox(
    text,
    title="McGluszak MacroIndustries",
    buttons: MsgboxBoxButtons = MsgboxBoxButtons.OK,
    icon: MsgBoxIcon = MsgBoxIcon.NONE,
):
    import ctypes as ct

    return ct.windll.user32.MessageBoxW(0, text, title, buttons.value | icon.value)


def confirm(text, title="McGluszak MacroIndustries"):
    return msgBox(text, title, MsgboxBoxButtons.YES_NO, MsgBoxIcon.QUESTION) == MsgBoxResult.YES.value


def getRoundedDownTime(
    dateTime: dt.datetime, numberOfMinutes: int, offsetDownBeforeROund: int, offsetDownAfterRound: int
):
    rdt = dateTime
    rdt = rdt - dt.timedelta(minutes=offsetDownBeforeROund)
    rdt = rdt - dt.timedelta(minutes=rdt.minute % numberOfMinutes, seconds=rdt.second, microseconds=rdt.microsecond)
    rdt = rdt - dt.timedelta(minutes=offsetDownAfterRound)
    return rdt


def getTimebandId(
    channel: str, dateTime: dt.datetime, numberOfMinutes: int, offsetDownBeforeROund: int, offsetDownAfterRound: int
):
    rdt = getRoundedDownTime(dateTime, numberOfMinutes, offsetDownBeforeROund, offsetDownAfterRound)
    return f"{channel}|{rdt.strftime('%Y-%m-%d %H%M')}"


def open_excel_workbook(file_path):
    import win32com.client

    try:
        # Try to get the running Excel instance
        excel = win32com.client.GetActiveObject("Excel.Application")
    except:
        # If no Excel instance is running, create one
        excel = win32com.client.Dispatch("Excel.Application")
    workbook = excel.Workbooks.Open(file_path)
    excel.Visible = True


def process_df_debug(df_debug_mode: GluDfDebugMode, file_path: str, df_caption, debug_msg_base: str) -> None:
    msg = debug_msg_base.replace("_1_", df_caption)
    folder_path = os.path.dirname(file_path)
    if df_debug_mode == GluDfDebugMode.ShowFilePath:
        inputBox(msg, default_value=file_path)
    elif df_debug_mode == GluDfDebugMode.ShowFolderPath:
        inputBox(msg, default_value=folder_path)
    elif df_debug_mode == GluDfDebugMode.PrintFolderPath:
        print(msg + "/n" + folder_path)
    elif df_debug_mode == GluDfDebugMode.OpenExcel:
        open_excel_workbook(file_path)
    elif df_debug_mode == GluDfDebugMode.Nothing:
        pass
    else:
        raise MyProgramException(f"Unknown df_debug_mode {df_debug_mode}")


def export_df(
    df: pd.DataFrame,
    df_caption: str,
    file_type: enum.FileType = enum.FileType.XLSX,
    add_now_str: bool = True,
    sheet_name: str = "Sheet1",
    df_debug_mode: GluDfDebugMode = GluDfDebugMode.Nothing,
    debug_msg_base: str = "df '_1_' saved at:",
    export_folder_path: str = "",
    export_index: bool = False,
    column_sep: str = ";",
    decimal_sep: str = ",",
) -> str:

    if export_folder_path == "":
        from classes.result_folder import sgltResultFolder
        export_folder = sgltResultFolder.folder
    else:
        export_folder = get_folder(export_folder_path)

    if add_now_str:
        now_str = " " + get_now_str()
    else:
        now_str = ""

    file_name = df_caption + now_str + file_type.value
    file_path = os.path.join(export_folder.path, file_name)
    if file_type == enum.FileType.CSV:
        df.to_csv(file_path, index=export_index, sep=column_sep, decimal=decimal_sep, encoding="utf-8-sig")
    elif file_type == enum.FileType.XLSX:
        df.to_excel(file_path, sheet_name=sheet_name, index=export_index)
    else:
        raise ValueError(f"File type {file_type} not supported")

    process_df_debug(df_debug_mode, file_path, df_caption, debug_msg_base)
    return file_path


# @property
def get_now_str() -> str:
    # Format date and time as yyyy-mm-dd hhmmss
    now_str = dt.datetime.now().strftime("%Y-%m-%d %H%M%S")
    return now_str


def get_float(input_str: str) -> float:
    if isinstance(input_str, float):
        my_float = input_str
    elif isinstance(input_str, int):
        my_float = float(input_str)
    elif isinstance(input_str, str):
        input_strMod = input_str.replace(",", ".")
        try:
            my_float = float(input_strMod)
        except ValueError:
            raise ValueError(f"Could not convert {input_str} to float")
    else:
        raise ValueError(f"Could not convert {input_str} to number")
    return my_float


def check_cannon_columns(
    df: pd.DataFrame,
    cannon_columns_list: enum.CannonColumnsSet = enum.CannonColumnsSet.DoNotCheck,
    drop_excess_columns: bool = False,
):
    if cannon_columns_list != enum.CannonColumnsSet.DoNotCheck:
        cannon_columns = get_cannon_columns_set(cannon_columns_list)

        missing_columns = set(cannon_columns) - set(df.columns)

        if missing_columns:
            export_df(df, f"Missing cannong columns for '{cannon_columns_list.value}'")
            raise ValueError(f"Missing cannon columns in the DataFrame: {', '.join(missing_columns)}")

        if drop_excess_columns:
            columns_to_drop: List[Any] = list(set(df.columns) - set(cannon_columns))
            df.drop(columns_to_drop, axis=1, inplace=True)


def is_enum_value(my_string: str, my_enum: Type[Enum]) -> bool:
    ok = False
    for member in my_enum:
        if member.value == my_string:
            ok = True
            break
    return ok


def get_union_of_dfs(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    if not all(df.columns.tolist() == dfs[0].columns.tolist() for df in dfs):
        raise ValueError("Columns of the dataframes are different")

    # Concatenate the dataframes
    union_df = pd.concat(dfs, ignore_index=True)
    return union_df


def setize(data_structure) -> Set:
    len_org = len(data_structure)
    my_set = set(data_structure)
    len_distinct = len(my_set)

    if len_org != len_distinct:
        raise ValueError("Duplicate values found")
    else:
        return my_set


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    if any(key in dict1 for key in dict2):
        raise ValueError("Duplicate keys found between dict1 and dict2")
    result = {**dict1, **dict2}
    return result


def get_values_from_txt(file_path: str) -> List[str]:
    with open(file_path, "r", encoding=CONST.ENCODING) as file:
        values = file.read().splitlines()
    return values


def print_values_to_txt(values: collections.abc.Iterable, file_path: str) -> File:
    with open(file_path, "w", encoding=CONST.ENCODING) as f:
        for item in values:
            f.write(str(item) + "\n")
    file = get_file(file_path)
    return file

def build_path(part1, part2) -> str:
    path:str = str(os.path.join(str(part1), part2))
    return path

class Collection(dict):
    def add(self, item, key: Union[str, int, None] = None):
        if key is None:
            key = len(self) + 1
        elif key in self:
            raise KeyError(f'Key "{key}" already exists in collection')
        else:
            self[key] = item

    def __iter__(self):
        return iter(self.values())

    def get_first_value(self):
        return next(iter(self.values()))

def get_formatted_timediff(timediff:datetime.timedelta)->str:
    # Extract hours, minutes, seconds, and milliseconds
    seconds = timediff.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timediff.microseconds // 1000
    info = f" ({hours:02}:{minutes:02}:{seconds:02}.{round(milliseconds / 100)})"
    return info

def get_filtered_df(data_frame: pd.DataFrame, columns: Union[str, List[str]], values: Union[object, List[object]], operations: Union[str, List[str]] = None) -> pd.DataFrame: # type: ignore
    """
    Filter a DataFrame based on given column names, values, and comparison operations.

    Parameters:
        data_frame (pd.DataFrame): The input DataFrame to be filtered.
        columns (str or list): Column name(s) to filter on.
        values (object or list): Value(s) to filter against.
        operations (str or list, optional): Comparison operation(s) for filtering. Default is '='.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if not isinstance(columns, list):
        columns = [columns]

    if not isinstance(values, list):
        values = [values]

    if operations is None:
        operations = ['='] * len(columns)
    elif not isinstance(operations, list):
        operations = [operations] * len(columns)

    # Build the filter conditions
    conditions = None
    for column, value, operation in zip(columns, values, operations):
        if operation == '=':
            condition = data_frame[column] == value
        elif operation == '!=':
            condition = data_frame[column] != value
        elif operation == '<':
            condition = data_frame[column] < value
        elif operation == '>':
            condition = data_frame[column] > value
        else:
            raise ValueError(f'Unknown operation: {operation}')
        # Add more comparison operations as needed

        if conditions is None:
            conditions = condition
        else:
            conditions &= condition

    filtered_df = data_frame[conditions] # type: ignore
    return filtered_df # type: ignore