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
    stupid_formatting = False
    result = 0
    values = {
        'I': 1,
        'V': 5
    }

    if re.search("пара", roman_str):
        roman_str = re.split("пара", roman_str)[0]
        stupid_formatting = True

    for i in range(len(roman_str) - 1):
        result = result - values[roman_str[i]] \
            if values[roman_str[i]] < values[roman_str[i + 1]] \
            else result + values[roman_str[i]]

    result += values[roman_str[len(roman_str) - 1]]

    if stupid_formatting:
        result = f"{result} пара"

    return str(result)


def sort_key(string: str):
    split = string[:5].split('.')
    return split[1], split[0]


def join_split_string(temp_str: List[str], split_string: List[str]) -> str:
    temp_str[1] = ' '.join(split_string)
    return remove_extra_whitespaces(' '.join(temp_str))
