from dataclasses import dataclass
from typing import List

from classes.channel_break import ChannelBreak


@dataclass
class FreeTimes():
    channel_breaks:List[ChannelBreak]



