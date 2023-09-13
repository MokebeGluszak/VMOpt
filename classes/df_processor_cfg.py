from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

import zzz_enums as enum
from classes.column_def import columnDef

from zzz_tools import Collection


@dataclass
class DfProcessorConfig:
    df_processor_type: enum.DfProcessorType
    sheet_name:Any
    file_type: enum.FileType
    date_format: str = "%Y-%m-%d"  # Specify the date format if needed
    column_separator: str = ";"  # Specify the column separator
    decimal_separator: str = ","  # Specify the decimal separator
    date_columns_to_parse: Optional[List[str]] = None  # Specify the date columns to parse
    import_only_defined_columns: bool = True  # Specify if only defined columns should be imported
    encoding: str = "utf-8"  # Specify the encoding of the file
    slownik_cfgs_types: List[enum.SlownikType] = field(default_factory=list)
    add_file_name: bool = False
    max_header_row:int = 1

    def add_column(self, name_org: str, name_mod: str, data_type: enum.DataType) -> None:
        column_def = columnDef(name_org, name_mod, data_type)
        self.column_defs.add (column_def, column_def.column_mod)

    def define_columns(self) -> None:
        self.column_defs: Collection = Collection()

        match self.df_processor_type:


            case enum.DfProcessorType.BOOKING_POLSAT:
                self.add_column("", "CopyLength", enum.DataType.INT  )  # "Datetime64[ns]")
                self.add_column("", "dateTime", enum.DataType.DATETIME64)
                self.add_column("", "channel_org", enum.DataType.STR)
                self.add_column("", "ratecard", enum.DataType.INT)
                self.add_column("", "blockId", enum.DataType.STR)
                self.add_column("", "subcampaign_org", enum.DataType.STR)

            # case enum.DfProcessorType.FREE_TIMES_POLSAT:
            #     # self.add_column("Channel", "channel")
            #     self.add_column("ID Bloku", "blockId")
            #     self.add_column("Data", "xDate")
            #     self.add_column("Godzina", "xTime")
            #     self.add_column("Nazwa", "programme")

            case enum.DfProcessorType.SCHEDULE:

                self.add_column("blockId", "blockId", enum.DataType.STR)
                self.add_column("channel", "channel", enum.DataType.STR)
                self.add_column("progBefore", "progBefore", enum.DataType.STR)
                self.add_column("progAfter", "progAfter", enum.DataType.STR)
                self.add_column("copyNumber", "copyNumber", enum.DataType.INT)
                self.add_column("xDateTime", "xDateTime", enum.DataType.DATETIME64)
                self.add_column("ratecard", "ratecard", enum.DataType.INT)
                self.add_column("grp", "grp", enum.DataType.FlOAT)

                self.add_column("eqNetPrice", "eqNetPrice", enum.DataType.INT)
                self.add_column("week", "week", enum.DataType.STR)
                self.add_column("channelGroup", "channelGroup", enum.DataType.STR)
                self.add_column("timeband", "timeband", enum.DataType.STR)
                # week	channelGroup	timeband
            case _:
                raise ValueError(f"Wrong df_processor_type: {self.df_processor_type}")


def get_df_processor_config(df_processor_type: enum.DfProcessorType):
    match df_processor_type:
        case enum.DfProcessorType.HISTORY_ORG:
            config = DfProcessorConfig(df_processor_type, 0, enum.FileType.XLSX)
        case enum.DfProcessorType.BOOKING_POLSAT:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                enum.FileType.XLSX,
                import_only_defined_columns=False,
                slownik_cfgs_types=[enum.SlownikType.SUBCAMPAIGNS, enum.SlownikType.CHANNELS],
            )
        case enum.DfProcessorType.FREE_TIMES_POLSAT:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                enum.FileType.XLSX,
                import_only_defined_columns=True,
                slownik_cfgs_types=[enum.SlownikType.WOLNE_CZASY_LENGTHS, enum.SlownikType.CHANNELS],
                add_file_name=True,
            )
        case enum.DfProcessorType.SCHEDULE:
            config = DfProcessorConfig(
                df_processor_type,
                "schedule",
                enum.FileType.XLSX
            )
        case enum.DfProcessorType.SCHEDULE_INFO:
            config = DfProcessorConfig(
                df_processor_type,
                0,
                enum.FileType.CSV,
                import_only_defined_columns=True
            )


        case _:
            raise ValueError(f"Wrong df_processor_type: {df_processor_type}")
    config.define_columns()
    return config
