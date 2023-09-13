import dataclasses
import os
from typing import List

from classes.file import File, get_file
from zzz_enums import BehaviourIfNotExists


@dataclasses.dataclass
class Folder:
    name: str
    path: str
    @property
    def get_files(self, omit_temp: bool = True) -> List[File]:

        files: List[File] = []

        for entry in os.scandir(self.path):
            if entry.is_file() and not entry.name.startswith('~'):
                file_path = os.path.join(self.path, entry.name)
                file:File = get_file(file_path)
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
        return os.path.abspath(self.path)

    def get_sub_folder_safe(self, name:str):
        path = os.path.join(self.path, name)
        return get_folder(path, BehaviourIfNotExists.Create)
def get_folder(path:str, behaviour_if_not_exists:BehaviourIfNotExists= BehaviourIfNotExists.Break)->Folder:

    if not os.path.exists(path):
        try:
            # Attempt to create the folder if it doesn't exist
            os.makedirs(path)
            name = os.path.basename(path)
            folder = Folder(name, path)
        except OSError:
            # If there was an error creating the folder, handle it here
            raise OSError (f"Error: Could not create folder {path}")
    else:
        name = os.path.basename(path)
        folder = Folder(name, path)



    return folder


