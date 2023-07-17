import dataclasses
import os


def get_file(path:str):
    if os.path.exists(path) :
        name = path.split("\\")[-1]
        parent_folder = path.split("\\")[-2]
        file = File(name, parent_folder, path)
    else:
        raise FileNotFoundError(f"File {path} not found")
@dataclasses.dataclass
class File:
    name:str
    parent_folder:str
    path:str