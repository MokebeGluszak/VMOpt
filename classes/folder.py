import dataclasses
import os


@dataclasses.dataclass
class Folder:
    name: str
    path: str


def get_folder(path:str)->Folder:
    name = os.path.basename(path)
    folder = Folder(name, path)
    return folder

