from dataclasses import dataclass
import zzz_enums as enums
from zzz_tools import singleton



@singleton
@dataclass
class sgltLog():
    text:str

    def __init__(self):
        self.text = ""
    def log(self, add_text:str):
        self.text = self.text + add_text + "\n"

    def log_header(self, add_text:str):
        if len(self.text) > 0 :
            self.text = self.text + "-" * 20 + "\n"
        self.text = self.text  + add_text.upper() + "\n"


def log(text:str):
    logger = sgltLog()
    logger.log(text)




def log_header(text:str):
    logger =  sgltLog()
    logger.log_header(text)

def print_log():
    logger = sgltLog()
    print(logger.text)

