import dataclasses
import os



@dataclasses.dataclass
class File:


    name:str
    parent_folder:str
    path:str

    def delete(self):
        os.remove(self.path)
def get_file(path:str):
    if os.path.exists(path) :
        name = path.split("\\")[-1]
        parent_folder = path.split("\\")[-2]
        file = File(name, parent_folder, path)
    else:
        raise FileNotFoundError(f"File {path} not found")
    return file