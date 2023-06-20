import openpyxl
from xls2xlsx import XLS2XLSX
from openpyxl import load_workbook
from typing import List


def open_xls_as_xlsx(filename: str) -> openpyxl.Workbook:
    x2x = XLS2XLSX(filename)
    return x2x.to_xlsx()


class Parser:
    def __init__(self):
        self.books: List[openpyxl.Workbook] = []

    def search(self, search_filter: str) -> None:
        pass

    def load_files(self, files: tuple) -> None:
        for item in files:
            print(item)
            book = open_xls_as_xlsx(item) \
                if item[-5:].split('.')[1] == 'xls' \
                else load_workbook(item)

            self.books.append(book)
