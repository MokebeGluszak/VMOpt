from typing import List


class Channel():
    def __init__(self, name:str, possible_names:List[str]):
        self.name = name
        self.possible_names = possible_names