from dataclasses import dataclass
from typing import List

from classes.schedule_break import ScheduleBreak


@dataclass
class BookingReport():
    wanted_unbooked:List[ScheduleBreak]
    wanted_booked:List[ScheduleBreak]
    unwanted_booked:List[ScheduleBreak]
    unwanted_unbooked:List[ScheduleBreak]
    unmatched_booked:List[ScheduleBreak]

    def __str__(self)   -> str:
        wu_str = f"Wanted unbooked.\t Count:{len(self.wanted_unbooked)}\t GRP: " +   "{:.1f}".format(sum([schedule_break.grpTg_50 for schedule_break in self.wanted_unbooked]))
        wb_str = f"Wanted booked.   \t Count:{len(self.wanted_booked)}\t GRP: " + "{:.1f}".format(sum([schedule_break.grpTg_50 for schedule_break in self.wanted_booked]))
        ub_str = f"Unwanted booked.\t Count:{len(self.unwanted_booked)}\t GRP: " +  "{:.1f}".format(sum([schedule_break.grpTg_50 for schedule_break in self.unwanted_booked]))
        uu_str = f"Unwanted unbooked.\t Count:{len(self.unwanted_unbooked)}\t GRP: " + "{:.1f}".format(sum([schedule_break.grpTg_50 for schedule_break in self.unwanted_unbooked]))
        unb_str = f"Unmatched unbooked.\t Count:{len(self.unmatched_booked)}\t GRP: " +  "{:.1f}".format( sum([schedule_break.grpTg_50 for schedule_break in self.unmatched_booked]))

        report_str = "\n".join([wu_str,wb_str,ub_str,uu_str,unb_str])
        return report_str


