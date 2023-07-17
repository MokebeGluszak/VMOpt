from typing import Dict

import zzz_const as _CONST
from classes.booking_report import BookingReport
from classes.channel_break import ChannelBreak
from classes.schedule_break import ScheduleBreak
from classes.subcampaign import Subcampaign
from zzz_ordersTools import get_empty_schedule_break


def get_booking_report(schedule_breaks, channel_breaks, subcampaigns_dict: Dict[Subcampaign, str]) -> BookingReport:
    channel_break: ChannelBreak
    schedule_break: ScheduleBreak
    booking_report = BookingReport([], [], [], [], [])
    for schedule_break in schedule_breaks:
        if schedule_break.break_info.block_id == _CONST.PODEJRZANY_BLOK_ID:
            print("chuj")
        if schedule_break.status_info.get_is_wanted:
            if schedule_break.channel_break == None:  # chcieliśy, nie dostaliśmy
                schedule_break.unbook()
                booking_report.wanted_unbooked.append(schedule_break)
            else:  # chcieliśmy, dostaliśmy
                subcampaign = subcampaigns_dict[schedule_break.channel_break.subcampaing_org]
                schedule_break.book(subcampaign_id=subcampaign.id)
                booking_report.wanted_booked.append(schedule_break)
        else:
            if schedule_break.channel_break == None:  # nie chieliśmy, nie dostaliśmy
                booking_report.unwanted_unbooked.append(schedule_break)
            else:  # nie chcieliśmy, dostaliśmy
                subcampaign = subcampaigns_dict[schedule_break.channel_break.subcampaing_org]
                booking_report.unmatched_booked.append(schedule_break)
                schedule_break.book(subcampaign_id=subcampaign.id)

    for channel_break in channel_breaks:  # bukujemy bloki które stacja nam dała a których nie było w ramówce
        if channel_break.schedule_break is None:
            # jeżeli w schedulebrejkach nie ma brejka który mugby się zmaczować to musimy dodać do schedula schedulebrejka wytworzonego na podstaiwe channelbrejka
            schedule_break = get_empty_schedule_break(channel_break.break_info)
            channel_break.schedule_break = schedule_break
            schedule_breaks.add(schedule_break, schedule_break.break_info.block_id)
            subcampaign = subcampaigns_dict[channel_break.subcampaing_org]
            schedule_break.book(subcampaign_id=subcampaign.id)
            booking_report.unmatched_booked.append(schedule_break)
    return booking_report
