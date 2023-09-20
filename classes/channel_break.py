# # from classes.break_info import BreakInfo
# from classes.iSerializable import iSerializable
# from classes.schedule_break import ScheduleBreak
# from classes.timeband import Timeband
# from zzz_enums import *
# from zzz_tools import Collection
#
#
# class ChannelBreak(iSerializable):
#     def __init__(self, break_info: BreakInfo, subcampaign_org: int, tbId: str):
#         self.break_info = break_info
#         self.tbId = tbId
#         self.subcampaing_org = subcampaign_org
#         self._match_level = MatchLevel.NO_MATCH
#         self._schedule_timeband: Timeband
#         self._schedule_break: ScheduleBreak|None = None
#
#     @property
#     def match_level(self) -> MatchLevel:
#         return self._match_level
#
#     @match_level.setter
#     def match_level(self, value: MatchLevel) -> None:
#         self._match_level = value
#
#     @property
#     def schedule_timeband(self) -> Timeband | None:
#         try:
#             return self._schedule_timeband
#         except:
#             return None
#
#     @schedule_timeband.setter
#     def schedule_timeband(self, value: Timeband) -> None:
#         self._schedule_timeband = value
#
#     @property
#     def schedule_break(self) -> ScheduleBreak | None:
#         try:
#             return self._schedule_break
#         except:
#             return None
#
#     @schedule_break.setter
#     def schedule_break(self, value: ScheduleBreak) -> None:
#         if self._schedule_break is None:
#             self._schedule_break = value
#             self._schedule_break.channel_break = self
#         else:
#             raise ValueError("Zjebałeś, setujesz najpierw schedule brejka")
#
#
#
#     def get_closest_break(self, schedule_breaks: Collection) -> ScheduleBreak:
#         schedule_break: ScheduleBreak
#         closest_break: ScheduleBreak = schedule_breaks.get_first_value()
#         smallest_diff = abs(self.break_info.date_time - closest_break.break_info.date_time)
#
#         for schedule_break in schedule_breaks:
#             time_diff = abs(schedule_break.break_info.date_time - self.break_info.date_time)
#             if time_diff < smallest_diff:
#                 smallest_diff = time_diff
#                 closest_break = schedule_break
#
#         return closest_break
#
#     def serialize(self, export_format: ExportFormat) -> dict:
#         if export_format == ExportFormat.ChannelBreak:
#             return {"ratecard": self.break_info.ratecard, "dateTime": self.break_info.date_time}
#         else:
#             raise ValueError(f"Invalid export format: {export_format}")
#
#     def get_potential_matches_ratecard(self) -> Collection:
#         potential_matches = Collection()
#         schedule_break: ScheduleBreak
#         if self.schedule_timeband is None:
#             pass
#         else:
#             for schedule_break in self.schedule_timeband.schedule_breaks:
#                 if schedule_break.break_info.ratecard == self.break_info.ratecard:
#                     potential_matches.add(schedule_break, schedule_break.break_info.block_id)
#         return potential_matches
#
#
# def get_channel_break(row) -> ChannelBreak:
#     break_info = BreakInfo(
#         blockId=row["blockId"], channel=row["channel"], date_time=row["dateTime"], ratecard=row["ratecard"]
#     )
#
#     channel_break = ChannelBreak(
#         break_info=break_info,
#         subcampaign_org=row["subcampaign_org"],  # TODO: ogarnąć subcampaign
#         tbId=row["tbId"],
#     )
#     return channel_break
