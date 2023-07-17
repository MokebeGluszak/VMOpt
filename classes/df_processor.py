from dataclasses import dataclass
from typing import List, Any, Optional

import pandas as pd

import zzz_enums as ENUM
from classes.column_def import columnDef
from classes.merger import get_merger
from zzz_tools import Collection, get_float


@dataclass
class DfProcessorConfig:
    df_processor_type: ENUM.DfProcessorType
    sheet_name: Any
    file_type: ENUM.FileType
    date_format: str = "%Y-%m-%d"  # Specify the date format if needed
    column_separator: str = ";"  # Specify the column separator
    decimal_separator: str = ","  # Specify the decimal separator
    date_columns_to_parse: Optional[List[str]] = None  # Specify the date columns to parse
    import_only_defined_columns: bool = True  # Specify if only defined columns should be imported
    encoding: str = "utf-8"  # Specify the encoding of the file
    def add_column(self, name_org: str, name_mod: str, data_type: Optional[str] = None) -> None:
        column_def = columnDef(name_org, name_mod, data_type)
        self.column_defs.add(column_def, name_mod)

    def define_columns(self) -> None:
        self.column_defs: Collection = Collection()

        match self.df_processor_type:
            case ENUM.DfProcessorType.HISTORY_ORG:
                self.add_column("Channel", "channelOrg")
                self.add_column("Date", "xDate")  # "Datetime64[ns]")
                self.add_column("Time", "xTime")  # , "Datetime64[ns]")
                self.add_column("Prog Campaign", "programme")
                self.add_column("Cost", "ratecard")
            case ENUM.DfProcessorType.BOOKING_POLSAT:
                self.add_column("", "CopyLength")  # "Datetime64[ns]")
                self.add_column("", "dateTime")
                self.add_column("", "channelOrg")
                self.add_column("", "ratecard")
                self.add_column("", "blockId")
                self.add_column("", "subcampaign_org")
            case ENUM.DfProcessorType.SCHEDULE:
                self.add_column("blockId", "blockId")
                self.add_column("channel", "channel")
                self.add_column("programme", "programme")
                self.add_column("blockType_org", "blockType_org")
                self.add_column("blockType_mod", "blockType_mod")
                self.add_column("xDate", "xDate")
                self.add_column("xTime", "xTime")
                self.add_column("ratecard", "ratecard")
                self.add_column("freeTime", "freeTime")
                self.add_column("week", "week")
                self.add_column("timeband", "timeband")
                self.add_column("wantedness", "wantedness")
                self.add_column("bookedness", "bookedness")
                self.add_column("eqPriceNet", "eqPriceNet")
                self.add_column("grpTg_01", "grpTg_01")
                self.add_column("grpTg_02", "grpTg_02")
                self.add_column("grpTg_50", "grpTg_50")
                self.add_column("grpTg_98", "grpTg_98")
                self.add_column("grpTg_99", "grpTg_99")
                self.add_column("positionCode", "positionCode")
                self.add_column("scheduleInfo", "scheduleInfo")
            case ENUM.DfProcessorType.FREE_TIMES_POLSAT:
                # self.add_column("Channel", "channel")
                self.add_column("ID Bloku", "blockId")
                self.add_column("Data", "xDate")
                self.add_column("Godzina", "xTime")
                self.add_column("Nazwa", "programme")
                self.add_column("Spot price", "ratecard")
            case _:
                    raise ValueError(f"Wrong df_processor_type: {self.df_processor_type}")


def get_df_processor_config(df_processor_type: ENUM.DfProcessorType):
    match df_processor_type:
        case ENUM.DfProcessorType.HISTORY_ORG:
            config = DfProcessorConfig(df_processor_type, 0, ENUM.FileType.XLSX)
        case ENUM.DfProcessorType.BOOKING_POLSAT:
            config = DfProcessorConfig(df_processor_type, 0, ENUM.FileType.XLSX, import_only_defined_columns=False)
        case ENUM.DfProcessorType.FREE_TIMES_POLSAT:
            config = DfProcessorConfig(df_processor_type, 0, ENUM.FileType.XLSX, import_only_defined_columns=True)
        case ENUM.DfProcessorType.SCHEDULE:
            config = DfProcessorConfig(
                    df_processor_type,
                    0,
                    ENUM.FileType.CSV,
                    import_only_defined_columns=False ,
                    date_columns_to_parse=["xDate"],
                    date_format="%Y-%m-%d %H:%M:%S",
                    column_separator=";",
                    decimal_separator=",",
                    encoding="utf-8"
            )

        case _:
            raise ValueError(f"Wrong df_processor_type: {df_processor_type}")
    config.define_columns()
    return config


class DfProcessor:
    def __init__(self, cfg: DfProcessorConfig, file_path: str):
        self.file_path = file_path
        self.cfg = cfg

    @property
    def get_file_name(self) -> str:
        return self.file_path.split("\\")[-1]

    @property
    def _get_column_orgs(self) -> List[str]:
        list = [column_def.column_org for column_def in self.cfg.column_defs]
        return list

    @property
    def _get_column_mods(self) -> List[str]:
        list = [column_def.column_mod for column_def in self.cfg.column_defs]
        return list

    @property
    def _get_dtype(self) -> dict:
        dtype = {}
        for column_def in self.cfg.column_defs:
            if column_def.data_type is not None:
                dtype[column_def.column_org] = column_def.data_type
        return dtype

    def _get_df_org_xlsx(self) -> pd.DataFrame:
        header_rows = range(0, 11)
        df_test = None
        if self.cfg.import_only_defined_columns:
            column_orgs = self._get_column_orgs
        else:
            column_orgs = None
        dtype = self._get_dtype

        for row in header_rows:
            try:
                df_test = pd.read_excel(
                    self.file_path, sheet_name=self.cfg.sheet_name, usecols=column_orgs, header=row, nrows=1
                )
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
            case ENUM.FileType.XLSX:
                df = self._get_df_org_xlsx()
            case ENUM.FileType.CSV:
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
            case ENUM.DfProcessorType.BOOKING_POLSAT:
                from zzz_ordersTools import get_date_time_polsat,get_copy_indexes_df

                df_copyIndexes = get_copy_indexes_df()
                df["CopyLength"] = df["Długość"].str.replace('"', "").astype(int)
                df = get_merger(
                    "copy indexes", df, df_copyIndexes, "CopyLength", case_sensitive=True
                ).return_merged_df()
                df["dateTime"] = df.apply(lambda x: get_date_time_polsat(x["Data"], x["Godzina"]), axis=1)
                df["channelOrg"] = df["Stacja"]
                df["ratecard_indexed"] = df.apply(lambda x: get_float(x["Base price"]), axis=1)
                df["ratecard"] = df["ratecard_indexed"] / df["CopyIndex"]
                df["subcampaign_org"] = df["Długość"] + "-" + self.get_file_name
                df.rename(columns={"ID Bloku": "blockId"}, inplace=True)
            case ENUM.DfProcessorType.SCHEDULE:
                pass
            case ENUM.DfProcessorType.FREE_TIMES_POLSAT:
                pass
            case _:
                raise NotImplementedError
        return df

    @property
    def get_df(self) -> pd.DataFrame:
        df: pd.DataFrame = self._get_df_org()           # bierze albo wszystkie albo zdefiniowane w zależność od cfg.import_only_defined_columns
        df =  self._transform_before_check_header(df)
        self._rename_columns(df)
        self._check_mod_columns(df)
        return df

    def _check_mod_columns(self, df):
        for new_name in self._get_column_mods:
            assert new_name in df.columns, f"Column '{new_name}' does not exist in the DataFrame."


def get_df_processor(df_processor_type: ENUM.DfProcessorType, file_path: str) -> DfProcessor:
    cfg = get_df_processor_config(df_processor_type)
    df_processor = DfProcessor(cfg, file_path)
    return df_processor
