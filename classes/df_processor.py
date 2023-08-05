from dataclasses import dataclass
from typing import List

import pandas as pd

import zzz_enums as enum
from classes.df_processor_cfg import DfProcessorConfig, get_df_processor_config
from classes.merger import get_merger
from classes.slownik import get_slownik

from zzz_tools import get_float


@dataclass
class DfProcessor:
    cfg: DfProcessorConfig
    file_path:str

    @property
    def get_file_name(self) -> str:
        return self.file_path.split("\\")[-1]

    @property
    def _get_column_orgs(self) -> List[str]:
        list = [column_def.column_org for column_def in self.cfg.column_defs.values()]
        return list

    @property
    def _get_column_mods(self) -> List[str]:
        list = [column_def.column_mod for column_def in self.cfg.column_defs.values()]
        return list

    @property
    def _get_dtype(self) -> dict:
        dtype = {}
        for column_def in self.cfg.column_defs.values():
            dtype[column_def.column_org] = column_def.data_type.value
        return dtype

    def _get_df_org_xlsx(self) -> pd.DataFrame:
        header_rows = range(0, 11)
        df_test = None
        if self.cfg.import_only_defined_columns:
            column_orgs = self._get_column_orgs
        else:
            column_orgs = None
        dtype = self._get_dtype
        # df_test = pd.read_excel(self.file_path, sheet_name=self.cfg.sheet_name, usecols=column_orgs,  nrows=1)
        for row in header_rows:
            try:
                df_test = pd.read_excel(self.file_path, sheet_name=self.cfg.sheet_name, usecols=column_orgs, header=row, nrows=1)
                break
            except:
                continue
        if df_test is None:
            raise ValueError(f"Error opening dataframe from: {self.file_path}")
        else:
            df = pd.read_excel(
                self.file_path, sheet_name=self.cfg.sheet_name, usecols=column_orgs, header=row, dtype=dtype
            )
        return df

    def _get_df_org_csv(self) -> pd.DataFrame:
        parse_dates: List[str]
        if self.cfg.date_columns_to_parse is None:
            parse_dates = []
        else:
            if isinstance(self.cfg.date_columns_to_parse, str):
                parse_dates = [self.cfg.date_columns_to_parse]
            else:
                parse_dates = self.cfg.date_columns_to_parse

        df = pd.read_csv(
            self.file_path,
            parse_dates=parse_dates,
            date_format=self.cfg.date_format,
            sep=self.cfg.column_separator,
            decimal=self.cfg.decimal_separator,
            usecols=self._get_column_orgs,
        )
        return df

    def _get_df_org(self) -> pd.DataFrame:
        match self.cfg.file_type:
            case enum.FileType.XLSX:
                df = self._get_df_org_xlsx()
            case enum.FileType.CSV:
                df = self._get_df_org_csv()

            case _:
                raise ValueError(f"Wrong df_processor_type: {self.cfg.df_processor_type}")

        return df

    def _rename_columns(self, df: pd.DataFrame):
        for old_name, new_name in zip(self._get_column_orgs, self._get_column_mods):
            if old_name != "":
                assert old_name in df.columns, f"Column '{old_name}' does not exist in the DataFrame."
                df.rename(columns={old_name: new_name}, inplace=True)

    def _transform_before_check_header(self, df: pd.DataFrame) -> pd.DataFrame:

        match self.cfg.df_processor_type:
            case enum.DfProcessorType.BOOKING_POLSAT:
                from zzz_ordersTools import get_date_time_polsat,get_copy_indexes_df

                df_copyIndexes = get_copy_indexes_df()
                df["CopyLength"] = df["Długość"].str.replace('"', "").astype(int)
                df = get_merger(
                    "copy indexes", df, df_copyIndexes, "CopyLength", case_sensitive=True
                ).return_merged_df()
                df["dateTime"] = df.apply(lambda x: get_date_time_polsat(x["Data"], x["Godzina"]), axis=1)
                df["channel_org"] = df["Stacja"]
                df["ratecard_indexed"] = df.apply(lambda x: get_float(x["Base price"]), axis=1)
                df["ratecard"] = df["ratecard_indexed"] / df["CopyIndex"]
                df["subcampaign_org"] = df["Długość"] + "-" + self.get_file_name
                df.rename(columns={"ID Bloku": "blockId"}, inplace=True)
            case enum.DfProcessorType.SCHEDULE:
                pass
            case enum.DfProcessorType.FREE_TIMES_POLSAT:
                df["channel_org"] = df["file_name"]
            case enum.DfProcessorType.SCHEDULE_INFO:
                pass
            case _:
                raise NotImplementedError
        return df


    @property
    def get_df(self) -> pd.DataFrame:
        df: pd.DataFrame = self._get_df_org()           # bierze albo wszystkie albo zdefiniowane w zależność od cfg.import_only_defined_columns
        if self.cfg.add_file_name:
            df["file_name"] = self.get_file_name
        df =  self._transform_before_check_header(df)

        self._rename_columns(df)
        self._process_slowniki(df)
        self._check_mod_columns(df)
        return df

    def _check_mod_columns(self, df):
        for new_name in self._get_column_mods:
            assert new_name in df.columns, f"Column '{new_name}' does not exist in the DataFrame."

    def _process_slowniki(self, df):
        # print(self.cfg.df_processor_type.value)
        for slownik_cfg in self.cfg.slownik_cfgs_types:
            slownik = get_slownik(slownik_cfg, df)


def get_df_processor(df_processor_type: enum.DfProcessorType, file_path: str) -> DfProcessor:
    cfg = get_df_processor_config(df_processor_type)
    df_processor = DfProcessor(cfg, file_path)
    return df_processor
