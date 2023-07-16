from unittest import TestCase

import pandas as pd

import zzz_ordersTools as ot


class TestChannelsMapping(TestCase):
    json_path: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.json_path = "./source/json channels.txt"

    def test_channels_mapping(self):
        df = ot.get_channels_mapping_df()
        self.assertIsInstance(df, pd.DataFrame)
        cannon_columns = "supplier channelGroup channel channelPossibleName".split()
        self.assertTrue(all(col in df.columns for col in cannon_columns))
