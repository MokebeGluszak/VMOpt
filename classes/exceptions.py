from typing import List

from zzz_enums import *


class MyProgramException(Exception):
    """Base class for other exceptions"""

    pass


# class BookingChannelsException(MyProgramException):
#     """Raised when the booking channels are not valid"""
#     def __init__(self):
#     pass



class MergerException(MyProgramException):
    """Raised when the merger is not valid"""

    def __init__(self, exception_type: ExceptionType, unjoined_values:List[str], caption: str= "Merge Operation"):
        self.exception_type = exception_type
        self.unjoined_values = unjoined_values
        self.caption = caption

    def __str__(self):
        return self.exception_type.value.replace("_UnjoinedValues_", str(self.unjoined_values).replace("_caption_", self.caption))
