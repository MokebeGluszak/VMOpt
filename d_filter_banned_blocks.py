import pandas as pd

import zzz_enums as enums
from classes.log import log, log_header

def filter_banned_blocks(schedule_df:pd.DataFrame, banned_blocks:list[str]) :
    log_header("Filtering banned blocks")
    count_before = len(schedule_df)
    schedule_df = schedule_df[~schedule_df['blockId'].isin(banned_blocks)]
    count_after = len(schedule_df)
    log(f"Removed {count_before - count_after} banned blocks")