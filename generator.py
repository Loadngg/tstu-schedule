from docx import Document
from docx.shared import Pt
from typing import List
from utils import remove_extra_whitespaces
import re


def sort_key(string: str):
    split = string[:5].split('.')
    return split[1], split[0]


def generate(results: List[str], search_filter: str) -> None:
    print("---GENERATION START---")

    time_interval_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b-\b[0-2]?[0-9].[0-5][0-9]\b)"
    time_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b)"

    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(14)

    results.sort(key=sort_key)

    for key, result in enumerate(results):
        temp_str = [result[:5], result[6:]]
        if re.search(time_interval_regex, temp_str[1]) is None and re.search(time_regex, temp_str[1]):
            split_string = re.split(time_regex, temp_str[1])
            split_string[0], split_string[1] = split_string[1], split_string[0]
            temp_str[1] = ' '.join(split_string)
            temp_str = remove_extra_whitespaces(' '.join(temp_str))
            results[key] = temp_str

    for result in results:
        paragraph = doc.add_paragraph(result)
        paragraph.paragraph_format.line_spacing = 1

    doc.save(f"Расписание {search_filter}.docx")

    print("---GENERATION END---")
