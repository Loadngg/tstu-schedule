import re
import openpyxl
from xls2xlsx import XLS2XLSX
from typing import List


def open_xls_as_xlsx(filename: str) -> openpyxl.Workbook:
    x2x = XLS2XLSX(filename)
    return x2x.to_xlsx()


def remove_extra_whitespaces(string: str) -> str:
    return ' '.join(string.split())


def roman_to_int(roman_str: str) -> str:
    result = 0
    values = {
        'I': 1,
        'V': 5
    }

    for i in range(len(roman_str) - 1):
        result = result - values[roman_str[i]] \
            if values[roman_str[i]] < values[roman_str[i + 1]] \
            else result + values[roman_str[i]]

    result += values[roman_str[len(roman_str) - 1]]

    return str(result)


def find_in_list(regex_pattern: str, string: List[str]) -> List:
    result = list(filter(re.compile(regex_pattern).match, string))

    return result


def remove_substring_from_string(regex_pattern: str, string: str) -> str:
    return remove_extra_whitespaces(re.sub(f"{regex_pattern}", "", string))
