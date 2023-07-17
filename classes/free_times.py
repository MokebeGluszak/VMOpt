import os
from dataclasses import dataclass
from typing import List

import pandas as pd

import zzz_enums as ENUM
from classes.channel_break import ChannelBreak
from classes.df_processor import get_df_processor
from classes.exceptions import MyProgramException
from classes.merger import get_merger
from zzz_ordersTools import SgltChannelMapping
from zzz_tools import get_files, get_union_of_dfs


def get_free_times_folder_path(supplier: ENUM.Supplier, free_times_quality: ENUM.FreeTimesQuality) -> str:
    folder = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\zrobić porządki"

    case = supplier.value + free_times_quality.value
    if case == ENUM.Supplier.POLSAT.value + ENUM.FreeTimesQuality.OK.value:
        subfolder = "7. FreeTimesPolsat"
    else:
        raise MyProgramException(f"Wrong supplier: {supplier} / free_times_quality: {free_times_quality}")
    # elif supplier == GluSupplier.TVN:
    #     file = "2 booking 2022-10-06 114034 TVN no pato.txt"
    # elif Supplier == GluSupplier.TVP:
    #     file = "2 booking 2022-10-06 113747 TVP 1z2.xls"
    return os.path.join(folder, subfolder)


@dataclass
class free_times:
    df: pd.DataFrame
    channel_breaks: List[ChannelBreak]


def get_df_processor_type_from_supplier(supplier: ENUM.Supplier) -> ENUM.DfProcessorType:
    match supplier:
        case ENUM.Supplier.POLSAT:
            df_processor_type = ENUM.DfProcessorType.FREE_TIMES_POLSAT
        case _:
            raise NotImplementedError(f"Supplier {supplier} not implemented")
    return df_processor_type


def get_df_free_times_org(supplier: ENUM.Supplier, free_times_quality: ENUM.FreeTimesQuality) -> pd.DataFrame:
    dfs: List[pd.DataFrame] = []
    folder_path = get_free_times_folder_path(supplier, free_times_quality)
    files = get_files(folder_path)
    df_processor_type = get_df_processor_type_from_supplier(supplier)
    for file in files:
        single_file_df = get_df_processor(df_processor_type, file).get_df
        single_file_df["channel_org"]
        dfs.append(single_file_df)

    df = get_union_of_dfs(dfs)
    return df


def get_free_times(
    supplier: ENUM.Supplier,
    free_times_quality: ENUM.FreeTimesQuality,
) -> free_times:
    # free_times = free_times()
    df_org = get_df_free_times_org(supplier, free_times_quality)
    df_channel_mapping = SgltChannelMapping.get_df
    df = get_merger("Free times channel mapping", df_org, df_channel_mapping, "channel_org").get_df

    return free_times
