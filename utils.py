import openpyxl
from xls2xlsx import XLS2XLSX


def open_xls_as_xlsx(filename: str) -> openpyxl.Workbook:
    x2x = XLS2XLSX(filename)
    return x2x.to_xlsx()


def remove_extra_whitespaces(string: str) -> str:
    return ' '.join(string.split())
