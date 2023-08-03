from dataclasses import dataclass
from typing import Dict
from classes.folder import  Folder, get_folder
from zzz_tools import  singleton, get_now_str
import zzz_enums as enum
@singleton
@dataclass
# @property

class SgltResultFolder():
    folder: Folder
    def __init__(self):
        self.folder = get_folder("result/" + get_now_str())

    def get_subfolder(self, name: str) -> Folder:
        subfolder = get_folder(self.folder.path + "/" + name, behaviour_if_not_exists=enum.BehaviourIfNotExists.Create)
        return subfolder