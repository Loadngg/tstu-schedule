from docx import Document
from docx.shared import Pt
from typing import List
from customtkinter import CTkLabel
from recording import Recording


def sort_key(record: Recording) -> tuple:
    split = record.get_record()[0][:5].split('.')
    return split[1], split[0]


class Generator:
    def __init__(self, info_label: CTkLabel) -> None:
        self.info_label = info_label
        self.time_interval_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b-\b[0-2]?[0-9].[0-5][0-9]\b)"
        self.time_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b)"

    @staticmethod
    def __create_doc() -> Document:
        doc = Document()

        style = doc.styles['Normal']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(14)

        return doc

    @staticmethod
    def __output_results(items: List[Recording], doc: Document) -> None:
        items.sort(key=sort_key)

        for result_item in items:
            result_string = result_item.get_record()
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.line_spacing = 1
            paragraph.add_run(' '.join(result_string[:2])).bold = True
            paragraph.add_run(' ' + ' '.join(result_string[2:]))

    def generate(self, results: List[List[Recording]], search_filter: List[str], general_file: bool = False) -> None:
        self.info_label.configure(text="Генерация...")

        if general_file:
            doc = self.__create_doc()

            for item in results:
                self.__output_results(item, doc)
                doc.add_paragraph().paragraph_format.line_spacing = 1

            doc.save(f"Расписание {' '.join(search_filter)}.docx")
        else:
            for item in results:
                doc = self.__create_doc()
                self.__output_results(item, doc)
                doc.save(f"Расписание {search_filter[results.index(item)]}.docx")

        self.info_label.configure(text="Генерация завершена")
