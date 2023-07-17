import dataclasses
import os
from typing import List

from classes.file import File, get_file


@dataclasses.dataclass
class Folder:
    name: str
    path: str
    @property
    def get_files(self, omit_temp: bool = True) -> List[File]:

        files: List[str] = []

        for entry in os.scandir(self.path):
            if entry.is_file() and not entry.name.startswith('~'):
                file_path = os.path.join(self.path, entry.name)
                file = get_file(file_path)
                files.append(file)
        return files

    def clear(self) -> None:
        for file in self.get_files:
            file.delete()

    def get_file(self, file_name: str) -> File:
        file_path = os.path.join(self.path, file_name)
        file = get_file(file_path)
        return file

    def __str__(self):
        return self.path
def get_folder(path:str)->Folder:
    name = os.path.basename(path)
    folder = Folder(name, path)
    return folder


