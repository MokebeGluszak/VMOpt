from typing import Dict



class SingletonMeta(type):
    _instances: Dict["SingletonMeta", object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ResultFolder(metaclass=SingletonMeta):
    result_dir = None
    def get_result_dir(self):
        from zzz_tools import get_now_str, get_dir_safe
        if self.result_dir is None:
            folder_name = r"result/" + get_now_str()
            root_dir = get_dir_safe("result")
            self.result_dir = get_dir_safe(folder_name)
        return self.result_dir

    def get_result_sub_dir(self, sub_folder_name):
        return get_dir_safe(self.get_result_dir() + "/" + sub_folder_name)
