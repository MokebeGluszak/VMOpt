from dataclasses import dataclass
import zzz_enums as enums
from zzz_tools import singleton

@singleton
@dataclass
class sgltLog():
    text:str
    def log(self, add_text:str):
        self.text = self.text + add_text + "\n"