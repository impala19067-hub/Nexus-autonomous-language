"""
Exhaustive Sapphire Documentation Suite Generator
Generates 5 comprehensive, multi-page, publication-grade PDF manuals:
1. Sapphire_Coding_and_Usage_Guide.pdf (~8-12 pages)
2. Building_Advanced_Autonomous_AI.pdf (~8-10 pages)
3. Sapphire_Autonomy_and_Performance_Benchmarks.pdf (~8-10 pages)
4. Beginners_Guide_Your_First_Autonomous_AI.pdf (~6-8 pages)
5. Sapphire_Language_Specification_and_Automation_Manual.pdf (~10-14 pages)
"""

import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, String, Rect, Group, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart

# Running Canvas for Page Numbers & Headers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, doc_title="SAPPHIRE DOCUMENTATION", **kwargs):
        super().__init__(*args, **kwargs)
        self.doc_title = doc_title
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"   📄 {self.doc_title}: {num_pages} pages")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0F172A"))
        
        # Header line & title
        self.drawString(54, 750, self.doc_title)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer line & page numbers
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Sapphire Language & AI Architecture — Official Developer Manual")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def make_canvas_class(doc_title):
    class CustomCanvas(NumberedCanvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, doc_title=doc_title, **kwargs)
    return CustomCanvas

def get_styles():
    styles = getSampleStyleSheet()
    PRIMARY = colors.HexColor("#0F172A")
    ACCENT = colors.HexColor("#2563EB")
    TEXT_DARK = colors.HexColor("#1E293B")
    
    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=colors.white, alignment=1, spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=colors.HexColor("#94A3B8"), alignment=1, spaceAfter=18
    ))
    styles.add(ParagraphStyle(
        'CustomH1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=PRIMARY, spaceBefore=16, spaceAfter=8, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'CustomH2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=ACCENT, spaceBefore=12, spaceAfter=6, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'CustomH3', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=colors.HexColor("#0D9488"), spaceBefore=10, spaceAfter=4, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'NormalText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=TEXT_DARK, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'BulletText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=TEXT_DARK, spaceAfter=3, leftIndent=15
    ))
    styles.add(ParagraphStyle(
        'CodeText', parent=styles['Normal'],
        fontName='Courier', fontSize=8.5, leading=11.5,
        textColor=colors.HexColor("#38BDF8")
    ))
    styles.add(ParagraphStyle(
        'CalloutTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12.5,
        textColor=PRIMARY, spaceAfter=3
    ))
    return styles

def code_box(code_text, styles):
    lines = code_text.strip().split('\n')
    formatted = "<br/>".join([line.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;') for line in lines])
    p = Paragraph(formatted, styles['CodeText'])
    
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#1E293B")),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

def callout_box(title, text, styles, alert_type="note"):
    bg_color = colors.HexColor("#EFF6FF")
    border_color = colors.HexColor("#3B82F6")
    if alert_type == "tip":
        bg_color = colors.HexColor("#F0FDF4")
        border_color = colors.HexColor("#22C55E")
    elif alert_type == "warning":
        bg_color = colors.HexColor("#FEF2F2")
        border_color = colors.HexColor("#EF4444")
        
    title_p = Paragraph(f"<b>{title}</b>", styles['CalloutTitle'])
    text_p = Paragraph(text, styles['NormalText'])
    
    t = Table([[title_p], [text_p]], colWidths=[494])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t

def cover_banner(title, subtitle, version="v1.0.0 (Production Release)", styles=None):
    cover_data = [
        [Paragraph(title, styles['CoverTitle'])],
        [Paragraph(subtitle, styles['CoverSubtitle'])],
        [Paragraph(f"<font color='#38BDF8'><b>{version}</b></font> | Sapphire Language Architecture Team", 
                   ParagraphStyle('CoverMeta', parent=styles['CoverSubtitle'], fontSize=9.5, textColor=colors.white))]
    ]
    t_cover = Table(cover_data, colWidths=[504])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 28),
        ('BOTTOMPADDING', (0,0), (-1,-1), 28),
        ('LEFTPADDING', (0,0), (-1,-1), 18),
        ('RIGHTPADDING', (0,0), (-1,-1), 18),
        ('LINEBELOW', (0,-1), (-1,-1), 3.5, colors.HexColor("#0D9488")),
    ]))
    return t_cover
