from dataclasses import dataclass, field
from typing import List, Optional

import zzz_enums as ENUM
from classes.column_def import columnDef
from zzz_tools import Collection


@dataclass
class DfProcessorConfig:
    df_processor_type: ENUM.DfProcessorType
    sheet_name: any
    file_type: ENUM.FileType
    date_format: str = "%Y-%m-%d"  # Specify the date format if needed
    column_separator: str = ";"  # Specify the column separator
    decimal_separator: str = ","  # Specify the decimal separator
    date_columns_to_parse: Optional[List[str]] = None  # Specify the date columns to parse
    import_only_defined_columns: bool = True  # Specify if only defined columns should be imported
    encoding: str = ("utf-8",)  # Specify the encoding of the file
    slownik_cfgs_types: List[ENUM.SlownikType] = field(default_factory=list)
    add_file_name: bool = False

    def add_column(self, name_org: str, name_mod: str, data_type: Optional[str] = None) -> None:
        column_def = columnDef(name_org, name_mod, data_type)
        self.column_defs.add(column_def, name_mod)

    def define_columns(self) -> None:
        self.column_defs: Collection = Collection()

        match self.df_processor_type:
            case ENUM.DfProcessorType.HISTORY_ORG:
                self.add_column("Channel", "channel_org")
                self.add_column("Date", "xDate")  # "Datetime64[ns]")
                self.add_column("Time", "xTime")  # , "Datetime64[ns]")
                self.add_column("Prog Campaign", "programme")
                self.add_column("Cost", "ratecard")
            case ENUM.DfProcessorType.BOOKING_POLSAT:
                self.add_column("", "CopyLength")  # "Datetime64[ns]")
                self.add_column("", "dateTime")
                self.add_column("", "channel_org")
                self.add_column("", "ratecard")
                self.add_column("", "blockId")
                self.add_column("", "subcampaign_org")
            case ENUM.DfProcessorType.SCHEDULE:
                self.add_column("blockId", "blockId")
                self.add_column("channel", "channel_org")
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
            case ENUM.DfProcessorType.FREE_TIMES_POLSAT:
                # self.add_column("Channel", "channel")
                self.add_column("ID Bloku", "blockId")
                self.add_column("Data", "xDate")
                self.add_column("Godzina", "xTime")
                self.add_column("Nazwa", "programme")
                self.add_column("Spot price", "ratecard")
            case ENUM.DfProcessorType.SCHEDULE_INFO:
                self.add_column("scheduleInfo", "scheduleInfo")
            case _:
                raise ValueError(f"Wrong df_processor_type: {self.df_processor_type}")


def get_df_processor_config(df_processor_type: ENUM.DfProcessorType):
    match df_processor_type:
        case ENUM.DfProcessorType.HISTORY_ORG:
            config = DfProcessorConfig(df_processor_type, 0, ENUM.FileType.XLSX)
        case ENUM.DfProcessorType.BOOKING_POLSAT:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                ENUM.FileType.XLSX,
                import_only_defined_columns=False,
                slownik_cfgs_types=[ENUM.SlownikType.SUBCAMPAIGNS, ENUM.SlownikType.CHANNELS],
            )
        case ENUM.DfProcessorType.FREE_TIMES_POLSAT:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                ENUM.FileType.XLSX,
                import_only_defined_columns=True,
                slownik_cfgs_types=[ENUM.SlownikType.WOLNE_CZASY_LENGTHS, ENUM.SlownikType.CHANNELS],
                add_file_name=True,
            )
        case ENUM.DfProcessorType.SCHEDULE:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                ENUM.FileType.CSV,
                import_only_defined_columns=False,
                date_columns_to_parse=["xDate"],
                date_format="%Y-%m-%d %H:%M:%S",
                column_separator=";",
                decimal_separator=",",
                encoding="utf-8",
            )
        case ENUM.DfProcessorType.SCHEDULE_INFO:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                ENUM.FileType.CSV,
                import_only_defined_columns=True
            )


        case _:
            raise ValueError(f"Wrong df_processor_type: {df_processor_type}")
    config.define_columns()
    return config
