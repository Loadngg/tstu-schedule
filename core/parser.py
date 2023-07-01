import openpyxl
from re import search
from openpyxl import load_workbook
from typing import List
from customtkinter import CTkLabel

from core.utils import remove_extra_whitespaces, open_xls_as_xlsx


class Parser:
    def __init__(self, info_label: CTkLabel) -> None:
        self.books: List[openpyxl.Workbook] = []
        self.books_path: List[str] = []
        self.info_label = info_label

    def clear_books(self) -> None:
        self.books.clear()
        self.books_path.clear()

    def load_files(self, files: tuple) -> List[openpyxl.Workbook]:
        self.info_label.configure(text="Загрузка...")

        for item in files:
            if item in self.books_path:
                continue
            book = open_xls_as_xlsx(item) \
                if item[-5:].split('.')[1] == 'xls' \
                else load_workbook(item)

            self.books_path.append(item)
            self.books.append(book)
            print(f"Loaded {item}")

        self.info_label.configure(text=f"Успешно загружено файлов: {self.books.__len__()}")

        return self.books

    def search(self, search_filter: str) -> List[str]:
        self.info_label.configure(text="Обработка...")

        filter_regex = rf"\b{search_filter}\b"

        result: List[str] = []

        for book in self.books:
            for sheet_name in book.get_sheet_names():
                sheet = book.get_sheet_by_name(sheet_name)

                time_column_exist = search("время", str(sheet.cell(row=1, column=2).value))

                for cellObj in sheet[1:sheet.max_row]:
                    for cell in cellObj:
                        if cell.value is not None and str(cell.value) != '' and search(filter_regex, str(cell.value)):
                            row_index = cell.row

                            while sheet.cell(row=row_index, column=1).value is None:
                                row_index -= 1

                            result.append(
                                ' '.join(
                                    [
                                        remove_extra_whitespaces(sheet.cell(row=row_index, column=1).value)[:5],
                                        ' '.join(
                                            [
                                                remove_extra_whitespaces(sheet.cell(row=cell.row, column=2).value),
                                                remove_extra_whitespaces(
                                                    sheet.cell(row=cell.row + 1, column=2).value)
                                            ]
                                        ) if time_column_exist else '',
                                        remove_extra_whitespaces(sheet.cell(row=1, column=cell.column).value),
                                        remove_extra_whitespaces(cell.value),
                                    ]
                                )
                            )

            print(f"Book {self.books.index(book)} processed")

        self.info_label.configure(text="Обработка завершена")

        return result
