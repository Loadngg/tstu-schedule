from docx import Document
from docx.shared import Pt
from typing import List
from utils import roman_to_int, join_split_string, sort_key
import re


class Generator:
    def __init__(self):
        self.time_interval_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b-\b[0-2]?[0-9].[0-5][0-9]\b)"
        self.time_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b)"

    @staticmethod
    def __create_doc() -> Document:
        doc = Document()

        style = doc.styles['Normal']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(14)

        return doc

    def __output_results(self, item: List[str], doc: Document) -> None:
        item.sort(key=sort_key)

        for key, result in enumerate(item):
            temp_str = [result[:5], result[6:]]

            if re.search("пара", temp_str[1]):
                split_string = temp_str[1].split()
                split_string[0] = roman_to_int(split_string[0])
                split_string[0], split_string[2] = split_string[2], split_string[0]
                split_string[1], split_string[2] = split_string[2], split_string[1]
                split_string[1] = "(" + split_string[1]
                split_string[2] += ")"
                split_string[0] = split_string[0].replace(".", ":")
                item[key] = join_split_string(temp_str, split_string)
            if re.search(self.time_interval_regex, temp_str[1]):
                split_string = temp_str[1].split()
                split_string[0] = split_string[0].split("-")[0]
                item[key] = join_split_string(temp_str, split_string)
            if re.search(self.time_interval_regex, temp_str[1]) is None and re.search(self.time_regex, temp_str[1]):
                split_string = re.split(self.time_regex, temp_str[1])
                split_string[0], split_string[1] = split_string[1], split_string[0]
                split_string[0] = split_string[0].replace(".", ":")
                item[key] = join_split_string(temp_str, split_string)

        for result_string in item:
            split_string = result_string.split()
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.line_spacing = 1
            paragraph.add_run(' '.join(split_string[:2])).bold = True
            paragraph.add_run(' ' + ' '.join(split_string[2:]))

    def generate(self, results: List[List[str]], search_filter: List[str], general_file: bool = False) -> None:
        print("---GENERATION START---")

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

        print("---GENERATION END---")
