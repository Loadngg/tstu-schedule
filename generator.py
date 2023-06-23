from docx import Document
from docx.shared import Pt
from typing import List
from utils import roman_to_int, join_split_string, sort_key
import re


def generate(results: List[List[str]], search_filter: List[str], general_file: bool = False) -> None:
    print("---GENERATION START---")

    time_interval_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b-\b[0-2]?[0-9].[0-5][0-9]\b)"
    time_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b)"

    if general_file:
        pass
    else:
        for item in results:
            doc = Document()

            style = doc.styles['Normal']
            style.font.name = 'Times New Roman'
            style.font.size = Pt(14)

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
                if re.search(time_interval_regex, temp_str[1]):
                    split_string = temp_str[1].split()
                    split_string[0] = split_string[0].split("-")[0]
                    item[key] = join_split_string(temp_str, split_string)
                if re.search(time_interval_regex, temp_str[1]) is None and re.search(time_regex, temp_str[1]):
                    split_string = re.split(time_regex, temp_str[1])
                    split_string[0], split_string[1] = split_string[1], split_string[0]
                    split_string[0] = split_string[0].replace(".", ":")
                    item[key] = join_split_string(temp_str, split_string)

            for result_string in item:
                split_string = result_string.split()
                paragraph = doc.add_paragraph()
                paragraph.paragraph_format.line_spacing = 1
                paragraph.add_run(' '.join(split_string[:2])).bold = True
                paragraph.add_run(' ' + ' '.join(split_string[2:]))

            doc.save(f"Расписание {search_filter[results.index(item)]}.docx")

    print("---GENERATION END---")
