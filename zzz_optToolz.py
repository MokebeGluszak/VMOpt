from typing import List
import zzz_enums as enums
from classes.log import log, log_header



def _clear_string_before_substr(input_string:str, substr:str)->str:
    # Split the input_string using "/" as the delimiter
    parts = input_string.split(substr)

    # Select the first part (before the first "/")
    trimmed_string = parts[0]

    return trimmed_string

# def _clear_string(input_string:str)->str:
#
#     str = input_string
#     str = _clear_string_before_substr(str, "/")
#     str = _clear_string_before_substr(str, "odc.")
#     return str

# input_string = "wojsko - polskie.pl - odc. 22/2023"
# result = clear_string(input_string)
# print(result)  # Output: "example"