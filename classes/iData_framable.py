import abc

import pandas as pd

from zzz_enums import ExportFormat


class iDataFrameable(abc.ABC):
    @abc.abstractmethod
    def to_dataframe(self, export_format: ExportFormat) -> pd.DataFrame:
        """zamienia obiekt na dataframe"""