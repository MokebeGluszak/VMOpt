from dataclasses import dataclass
from datetime import datetime

import zzz_enums as enums
from zzz_tools import singleton, get_formatted_timediff


@singleton
@dataclass
class _sgltLog():
    text:str
    operation_start:datetime
    global_start:datetime
    def __init__(self):
        self.text = ""
        self.global_start = datetime.now()


    def _get_time_info(self):
        # Assuming you have two datetime objects, dt1 and dt2

        # Calculate the time difference
        time_difference = datetime.now() - self.operation_start

        info = get_formatted_timediff(time_difference)
        return info

    def log(self, add_text:str, log_time:bool = False):
        if log_time:
            time_info = self._get_time_info()
        else:
            time_info = ""
        self.text = self.text + add_text + time_info + "\n"


    def log_header(self, add_text:str):
        if len(self.text) > 0 :
            self.text = self.text + "-" * 20 + "\n"
        self.text = self.text  + add_text.upper() + "\n"




def log(text:str, log_time:bool = False):
    logger = _sgltLog()
    logger.log(text, log_time)




def log_header(text:str):
    logger =  _sgltLog()
    logger.log_header(text)

def print_log():
    logger = _sgltLog()
    print(logger.text)
    print ("Total time:" +  get_formatted_timediff (datetime.now() - logger.global_start))

def reset_timer():
    logger = _sgltLog()
    logger.operation_start = datetime.now()