"""生成试卷排版用的 Word 参考样式（A4、宋体五号、1.45 倍行距）。"""
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT

doc = docx.Document('ref_default.docx')


def get_style(name):
    for s in doc.styles:
        if s.name == name:
            return s
    raise KeyError(name)


def set_font(style, cn='宋体', en='Times New Roman', size=10.5, bold=False):
    f = style.font
    f.name = en
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = RGBColor(0, 0, 0)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = docx.oxml.OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:ascii'), en)
    rfonts.set(qn('w:hAnsi'), en)
    rfonts.set(qn('w:eastAsia'), cn)


def set_para(style, line=1.45, before=0, after=0, indent=0, align=None, first_line=0):
    pf = style.paragraph_format
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.left_indent = Cm(indent)
    pf.first_line_indent = Cm(first_line)
    if align is not None:
        pf.alignment = align


# 正文
for name in ['Normal', 'Body Text', 'First Paragraph', 'Compact']:
    st = get_style(name)
    set_font(st, '宋体', 'Times New Roman', 10.5)
    set_para(st, line=1.45, before=0, after=0, first_line=0)

# 标题 / 副标题
t = get_style('Title')
set_font(t, '黑体', 'Times New Roman', 18, bold=True)
set_para(t, line=1.3, before=0, after=6, align=WD_ALIGN_PARAGRAPH.CENTER)

s = get_style('Subtitle')
set_font(s, '宋体', 'Times New Roman', 10.5)
set_para(s, line=1.3, before=0, after=4, align=WD_ALIGN_PARAGRAPH.CENTER)

# 一级、二级标题
h1 = get_style('Heading 1')
set_font(h1, '黑体', 'Times New Roman', 11.5, bold=True)
set_para(h1, line=1.45, before=10, after=2)

h2 = get_style('Heading 2')
set_font(h2, '黑体', 'Times New Roman', 10.5, bold=True)
set_para(h2, line=1.4, before=6, after=2)

# 图片居中、图注
fig = get_style('Figure')
set_para(fig, line=1.0, before=4, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
cap = get_style('Image Caption')
set_font(cap, '宋体', 'Times New Roman', 9)
set_para(cap, line=1.0, before=0, after=4, align=WD_ALIGN_PARAGRAPH.CENTER)

# 表格：加全框线
tb = get_style('Table')
set_font(tb, '宋体', 'Times New Roman', 10)
tblpr = tb.element.find(qn('w:tblPr'))
if tblpr is None:
    tblpr = docx.oxml.OxmlElement('w:tblPr')
    tb.element.append(tblpr)
borders = docx.oxml.OxmlElement('w:tblBorders')
for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
    el = docx.oxml.OxmlElement(f'w:{edge}')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), '6')
    el.set(qn('w:space'), '0')
    el.set(qn('w:color'), '000000')
    borders.append(el)
tblpr.append(borders)

sec = doc.sections[0]
sec.orientation = WD_ORIENT.PORTRAIT
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(2.0)
sec.right_margin = Cm(2.0)
sec.top_margin = Cm(2.0)
sec.bottom_margin = Cm(1.9)

doc.save('ref.docx')
print('ok')
