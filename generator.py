from docx import Document
from docx.shared import Pt
from typing import List


def generate(results: List[str], search_filter: str) -> None:
    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(14)

    for result in results:
        paragraph = doc.add_paragraph(result)
        paragraph.paragraph_format.line_spacing = 1

    doc.save(f"Расписание {search_filter}.docx")
