# -*- coding:utf-8 -*-

from docx import Document

read_doc=Document(r'李玉宾与新疆维吾尔自治区人民政府不予受理行政复议申请决定一审docx')
for p in read_doc.paragraphs:
    print(p.text)
