
from dataclasses import dataclass

@dataclass
class columnDef():
    column_org:str
    column_mod:str
    data_type:str|None=None