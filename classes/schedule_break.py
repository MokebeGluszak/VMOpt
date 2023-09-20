from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from classes.iSerializable import iSerializable
from classes.status_info import StatusInfo
from zzz_enums import Origin, ExportFormat




@dataclass
class ScheduleBreak(iSerializable):
    blockId: str
    channel: str
    progBefore: str
    progAfter: str
    xDateTime: datetime
    ratecard: int
    grp: float

    copyNumber: str

    week: str
    channelGroup: str
    timeband: str
    eqNetPrice: float
    def __str__(self):
        return str(self.blockId)

    def unbook(self):
        self.copyNumber = 0

    def book(self, copyNumber: int):
        self.copyNumber = copyNumber
    def serialize(self, export_format: ExportFormat):
        raise NotImplementedError
        # if export_format == ExportFormat.ScheduleBreak_rozkminki:
        #     my_dict = self.break_info.serialize(ExportFormat.Irrelevant) | self.status_info.serialize(
        #         ExportFormat.Irrelevant
        #     )
        # elif export_format == ExportFormat.ScheduleBreak_minerwa:
        #     my_dict = self.get_export_row_minerwa()
        # else:
        #     raise ValueError("Wrong export format")
        # return my_dict

    def get_export_row_minerwa(self) -> dict:
        my_dict: dict = {}
        raise NotImplementedError
        # my_dict["blockId"] = self.break_info.block_id
        # my_dict["channel"] = self.break_info.channel
        # my_dict["programme"] = self.programme
        # my_dict["blockType_org"] = self.blockType_org
        # my_dict["blockType_mod"] = self.blockType_mod
        # my_dict["xDate"] = self.break_info.date_time.date()
        # my_dict["xTime"] = self.break_info.date_time.time()
        # my_dict["ratecard"] = self.break_info.ratecard
        # my_dict["freeTime"] = self.freeTime
        # my_dict["week"] = "irrelevant"
        # my_dict["timeband"] = "irrelevant"
        # my_dict["wantedness"] = self.status_info.get_wantedness
        # my_dict["bookedness"] = self.status_info.get_bookedness
        # my_dict["eqPriceNet"] = 2137
        # # print (type(self.grpTg_01))
        # my_dict["grpTg_01"] = self.grpTg_01
        # my_dict["grpTg_02"] = self.grpTg_02
        # my_dict["grpTg_50"] = self.grpTg_50
        # my_dict["grpTg_98"] = self.grpTg_98
        # my_dict["grpTg_99"] = self.grpTg_99
        # my_dict["positionCode"] = self.positionCode
        # my_dict["scheduleInfo"] = self.scheduleInfo

        return my_dict


