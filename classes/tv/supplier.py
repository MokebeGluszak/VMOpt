from typing import List
from classes.tv.channel_group import ChannelGroup


class Supplier():
    def __init__(self, name, channel_groups: List[ChannelGroup]):
        self.name = name
        self.channel_groups = channel_groups

