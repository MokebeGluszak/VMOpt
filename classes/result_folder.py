from dataclasses import dataclass
from typing import Dict
from classes.folder import  Folder, get_folder
from zzz_tools import  singleton, get_now_str
import zzz_enums as enum

@singleton
@dataclass
class sgltResultFolder():
    folder:Folder

    def __init__(self):
        self.folder = get_folder("result/" + get_now_str())


def export_file_path(file_name:str):
    path = sgltResultFolder().folder.path + "/" + file_name
    return path