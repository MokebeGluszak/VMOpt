import datetime as dt

from classes.iSerializable import iSerializable
from zzz_enums import *


class BreakInfo(iSerializable):
    def __init__(self, blockId: int, date_time: dt.datetime, ratecard: int, channel: str):
        self.block_id = blockId
        self.date_time = date_time
        self.ratecard = ratecard
        self.channel = channel

    def serialize(self, export_format: ExportFormat):
        return {
            "blockId": self.block_id,
            "date_time": self.date_time,
            "ratecard": self.ratecard,
            "channel": self.channel,
        }

    @property
    def get_supplier(self):
        from zzz_ordersTools import SgltChannelMapping

        dict = SgltChannelMapping.get_channel_supplier_dict
        supplier = dict.get(self.channel)
        return supplier
