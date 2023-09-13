from typing import Dict

import zzz_const as CONST
import zzz_enums as ENUM
from classes.channel_break import ChannelBreak
from classes.timeband import Timeband
from zzz_tools import Collection


def match_channel_breaks_step1_id(channel_breaks, schedule_breaks: Collection):
    channel_break: ChannelBreak
    for channel_break in channel_breaks:
        if channel_break.break_info.block_id == CONST.PODEJRZANY_BLOK_ID:
            print("chuj")
        if channel_break.break_info.block_id in schedule_breaks.keys():
            channel_break.schedule_break = schedule_breaks[channel_break.break_info.block_id]
            channel_break.match_level = ENUM.MatchLevel.ID


def match_channel_breaks_step2_timebands(channel_breaks: Collection, timebands_dict: Dict[str, Timeband]) -> None:
    channel_break: ChannelBreak
    for channel_break in channel_breaks.values():
        try:
            channel_break.schedule_timeband = timebands_dict[channel_break.tbId]
        except KeyError:
            channel_break.match_level  = ENUM.MatchLevel.NO_TIMEBAND

        # if channel_break.break_info.blockId == 15107428494:
        #     pass

        if channel_break.schedule_timeband is not None:
            potential_matches_ratecard = channel_break.get_potential_matches_ratecard()
            if len(potential_matches_ratecard) > 0:
                channel_break.schedule_break = channel_break.get_closest_break(potential_matches_ratecard)
                channel_break.match_level = ENUM.MatchLevel.RATECARD
            else:
                potential_matches_time = channel_break.schedule_timeband.schedule_breaks
                if len(potential_matches_time) > 0:
                    channel_break.schedule_break = channel_break.get_closest_break(potential_matches_time)
                    channel_break.match_level = ENUM.MatchLevel.TIME
                else:
                    channel_break.match_level = ENUM.MatchLevel.NO_MATCH



