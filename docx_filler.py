from docx import Document
from docx.shared import Mm
import text_fill
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt


class docx_form:

    def __init__(self):
        self.document = Document()
        self.section = self.document.sections[-1]
        self.new_width, self.new_height = self.section.page_height, self.section.page_width
        self.section.page_width = Mm(210)
        self.section.page_height = Mm(297)

        self.style = self.document.styles['Normal']
        self.font = self.style.font
        self.font.name = 'Times New Roman'
        self.font.size = Pt(14)


    def doc_fill(self):
        paragraph = self.document.add_paragraph(text_fill.title)
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        self.font = 'bold'
        paragraph.style = self.style
        self.document.save('ТЗ.docx')

d = docx_form()
d.doc_fill()