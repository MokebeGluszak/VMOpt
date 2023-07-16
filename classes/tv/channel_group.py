from typing import List

from classes.tv.channel import Channel


class ChannelGroup():
    def __init__(self, name:str, channels:List[Channel]):
        self.name = name
        self.channels = channels