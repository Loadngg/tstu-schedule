from re import search
from openpyxl import load_workbook
from utils import *
from typing import List


class Parser:
    def __init__(self):
        self.books: List[openpyxl.Workbook] = []

    def load_files(self, files: tuple) -> None:
        print("---LOAD START---")

        for item in files:
            print(item)
            book = open_xls_as_xlsx(item) \
                if item[-5:].split('.')[1] == 'xls' \
                else load_workbook(item)

            self.books.append(book)

        print("---LOAD END---")

    def search(self, search_filter: str) -> None:
        print("---SEARCH START---")

        for book in self.books:
            for sheet_name in book.get_sheet_names():
                sheet = book.get_sheet_by_name(sheet_name)

                for cellObj in sheet[1:sheet.max_row]:
                    for cell in cellObj:
                        if cell.value is not None and str(cell.value) != '' and search(search_filter, str(cell.value)):
                            row_index = cell.row
                            while sheet.cell(row=row_index, column=1).value is None:
                                row_index -= 1
                            print(
                                remove_extra_whitespaces(sheet.cell(row=row_index, column=1).value),
                                remove_extra_whitespaces(sheet.cell(row=1, column=cell.column).value),
                                remove_extra_whitespaces(cell.value)
                            )

            print(f"Book {self.books.index(book)} processed\n")

        print("---SEARCH END---")
