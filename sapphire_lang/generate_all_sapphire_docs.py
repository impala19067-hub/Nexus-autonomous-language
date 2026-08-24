"""
Sapphire PDF Generator Script
Generates 5 comprehensive Sapphire PDF documents with ReportLab:
1. Sapphire_Coding_and_Usage_Guide.pdf / Sapphire_Coding_and_Usage_Guide.pdf
2. Building_Advanced_Autonomous_AI.pdf
3. Sapphire_Autonomy_and_Performance_Benchmarks.pdf / Sapphire_Autonomy_and_Performance_Benchmarks.pdf
4. Beginners_Guide_Your_First_Autonomous_AI.pdf
5. Sapphire_Language_Specification_and_Automation_Manual.pdf / Sapphire_Language_Specification_and_Automation_Manual.pdf
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

# Canvas with Running Headers & Footers
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

def make_code_block(code_text, styles):
    lines = code_text.strip().split('\n')
    formatted = "<br/>".join([line.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;') for line in lines])
    p = Paragraph(formatted, styles['CodeText'])
    
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#1E293B")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

def make_callout(title, text, styles, alert_type="note"):
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
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def setup_styles():
    styles = getSampleStyleSheet()
    PRIMARY = colors.HexColor("#0F172A")
    ACCENT = colors.HexColor("#2563EB")
    TEXT_DARK = colors.HexColor("#1E293B")
    
    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=30,
        textColor=colors.white, alignment=1, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=colors.HexColor("#94A3B8"), alignment=1, spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        'CustomH1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=PRIMARY, spaceBefore=18, spaceAfter=10, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'CustomH2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=ACCENT, spaceBefore=14, spaceAfter=8, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'NormalText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=TEXT_DARK, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'BulletText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=TEXT_DARK, spaceAfter=4, leftIndent=15
    ))
    styles.add(ParagraphStyle(
        'CodeText', parent=styles['Normal'],
        fontName='Courier', fontSize=9, leading=12,
        textColor=colors.HexColor("#38BDF8")
    ))
    styles.add(ParagraphStyle(
        'CalloutTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=PRIMARY, spaceAfter=4
    ))
    return styles


# 1. Sapphire Coding & Usage Guide
def generate_coding_guide(filename="Sapphire_Coding_and_Usage_Guide.pdf"):
    styles = setup_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    cover_data = [[
        Paragraph("SAPPHIRE PROGRAMMING LANGUAGE", styles['CoverTitle']),
    ], [
        Paragraph("Complete Coding Manual, Syntax Reference, ML & Agent Library Guide", styles['CoverSubtitle']),
    ]]
    t_cover = Table(cover_data, colWidths=[504])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 20))

    story.append(Paragraph("1. Introduction to Sapphire Language", styles['CustomH1']))
    story.append(Paragraph(
        "Sapphire is a modern high-level programming language engineered specifically for <b>PC Automation</b>, "
        "<b>Deep Learning & Neural Training</b>, <b>AI Agent Architectures</b>, and <b>Colorless Parallel Concurrency</b>. "
        "Sapphire combines clean readable syntax with zero-boilerplate standard library primitives for tensors, autograd, GPU acceleration, OS manipulation, and LLM reasoning.",
        styles['NormalText']
    ))
    
    story.append(make_callout(
        "Core Pipeline: Data to Autonomous Execution",
        "Data → Training → Model → Reasoning → Memory → Planning → Tool use → Autonomous execution",
        styles, "tip"
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Language Syntax & Fundamentals (.sp)", styles['CustomH1']))
    code_vars = """let agent_name = "Sapphire-Alpha";
let version = 1.0;
let is_active = true;
let tensor_data = ml.tensor([[1, 2], [3, 4]]);

print("Agent {agent_name} running Sapphire v{version}");"""
    story.append(make_code_block(code_vars, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Deep Learning & AI Standard Libraries", styles['CustomH1']))
    
    modules = [
        ("ml Module", "Tensors, autograd, datasets, model architectures, distributed training, numerical kernels, and GPU/TPU acceleration.",
         "let model = ml.model.mlp([16, 64, 2], 'relu');\nlet result = ml.train.fit(model, dataset, ml.loss.mse, ml.optim.adam(0.01), 5, 32, 2);"),
        ("ai Module", "Native LLM reasoning with local Ollama inference and automatic Groq API cloud fallback.",
         "let opinion = ai.prompt('Analyze RAM load and suggest optimization.');\nprint('AI Opinion: {opinion}');"),
        ("agent Module", "Short & long-term memory, goal planning, tool registration, permission policies, and autonomy loop.",
         "agent.memory.remember('accuracy', 0.95);\nagent.tools.register('deploy', 'Deploys model', fn() { os.notify('Alert', 'Deployed'); });\nagent.autonomy.run_loop('Deploy model v1', 5);")
    ]

    for title, desc, code_snippet in modules:
        story.append(Paragraph(f"<b>{title}</b>", styles['CustomH2']))
        story.append(Paragraph(desc, styles['NormalText']))
        story.append(make_code_block(code_snippet, styles))
        story.append(Spacer(1, 8))

    doc.build(story, canvasmaker=make_canvas_class("SAPPHIRE CODING & USAGE GUIDE"))


# 2. Building Advanced Autonomous AI
def generate_advanced_ai_guide(filename="Building_Advanced_Autonomous_AI.pdf"):
    styles = setup_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    cover_data = [[
        Paragraph("BUILDING ADVANCED AUTONOMOUS AI WITH SAPPHIRE", styles['CoverTitle']),
    ], [
        Paragraph("Architectural Blueprints, Neural Training, Memory, Planning, Tools & Autonomy", styles['CoverSubtitle']),
    ]]
    t_cover = Table(cover_data, colWidths=[504])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 20))

    story.append(Paragraph("1. Autonomous AI Architecture Principles", styles['CustomH1']))
    story.append(Paragraph(
        "An <b>Autonomous AI Agent</b> in Sapphire operates continuously in an environment, senses system telemetry, formulates plans, "
        "trains neural policy models, executes system actions via registered tools, evaluates feedback, and self-corrects.",
        styles['NormalText']
    ))

    code_full = """// Sapphire Complete AI Agent Pipeline (.sp)
fn run_pipeline() {
    let ds = ml.dataset.random(1000, 16, 2);
    let model = ml.model.mlp([16, 64, 2], "relu");
    let result = ml.train.fit(model, ds, ml.loss.mse, ml.optim.adam(0.01), 3, 32, 2);
    
    let ai_eval = ai.prompt("Final loss is {result.final_loss}. Is model ready?");
    agent.memory.remember("model_loss", result.final_loss);
    
    let goal = "Deploy model and notify admin";
    let agent_report = agent.autonomy.run_loop(goal, 4);
    print("Agent status: {agent_report['finished']}");
}

run_pipeline();"""
    story.append(make_code_block(code_full, styles))

    doc.build(story, canvasmaker=make_canvas_class("BUILDING ADVANCED AUTONOMOUS AI"))


# 3. Sapphire Benchmarks
def generate_benchmarks_pdf(filename="Sapphire_Autonomy_and_Performance_Benchmarks.pdf"):
    styles = setup_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    cover_data = [[
        Paragraph("SAPPHIRE AUTONOMY & PERFORMANCE BENCHMARKS", styles['CoverTitle']),
    ], [
        Paragraph("Comparative Analysis vs Python, JS, Go, Rust & PowerShell", styles['CoverSubtitle']),
    ]]
    t_cover = Table(cover_data, colWidths=[504])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 15))

    story.append(Paragraph("1. Executive Benchmark Summary", styles['CustomH1']))
    story.append(Paragraph(
        "Sapphire integrates deep learning tensors, autograd, GPU acceleration, and AI agent memory/planning directly into the language runtime.",
        styles['NormalText']
    ))

    d1 = Drawing(504, 180)
    bc1 = VerticalBarChart()
    bc1.x = 40
    bc1.y = 25
    bc1.height = 135
    bc1.width = 440
    bc1.data = [[99, 65, 52, 40, 35, 68]]
    bc1.categoryAxis.categoryNames = ['Sapphire', 'Python', 'Node.js', 'Go', 'Rust', 'PowerShell']
    bc1.categoryAxis.labels.fontSize = 9
    bc1.categoryAxis.labels.dy = -10
    bc1.bars[0].fillColor = colors.HexColor("#2563EB")
    bc1.valueAxis.valueMin = 0
    bc1.valueAxis.valueMax = 100
    bc1.valueAxis.valueStep = 20
    d1.add(bc1)
    story.append(d1)

    doc.build(story, canvasmaker=make_canvas_class("SAPPHIRE BENCHMARK ANALYSIS"))


# 4. Beginner's Guide
def generate_beginner_guide(filename="Beginners_Guide_Your_First_Autonomous_AI.pdf"):
    styles = setup_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    cover_data = [[
        Paragraph("BEGINNER'S GUIDE: YOUR FIRST AUTONOMOUS AI", styles['CoverTitle']),
    ], [
        Paragraph("Step-by-Step Introduction to Building AI Agents with Sapphire", styles['CoverSubtitle']),
    ]]
    t_cover = Table(cover_data, colWidths=[504])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 20))

    story.append(Paragraph("1. Writing Your First Sapphire AI Agent (.sp)", styles['CustomH1']))
    code_beginner = """// 5-Line Autonomous AI Agent in Sapphire (.sp)
let info = os.system_info();
let question = "System CPU is at {info.cpu_usage_percent}%. Recommend optimization action.";
let ai_opinion = ai.prompt(question);

os.notify("Sapphire Agent", ai_opinion);
print("🤖 Agent Output: {ai_opinion}");"""
    story.append(make_code_block(code_beginner, styles))

    doc.build(story, canvasmaker=make_canvas_class("BEGINNER'S GUIDE TO SAPPHIRE AI"))


# 5. Sapphire Specification Manual
def generate_pdf_manual(filename="Sapphire_Language_Specification_and_Automation_Manual.pdf"):
    styles = setup_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    cover_data = [[
        Paragraph("SAPPHIRE PROGRAMMING LANGUAGE", styles['CoverTitle']),
    ], [
        Paragraph("Specification, Automation, Deep Learning & AI Agent Architecture Manual", styles['CoverSubtitle']),
    ]]
    t_cover = Table(cover_data, colWidths=[504])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 20))

    story.append(Paragraph("1. Executive Summary & Design Philosophy", styles['CustomH1']))
    story.append(Paragraph(
        "<b>Sapphire</b> is designed as a unified language for PC Automation, Deep Neural Network Training, and Autonomous AI Agents. "
        "It eliminates external package friction by embedding tensors, autograd, datasets, GPU acceleration, and LLM reasoning directly into the standard library.",
        styles['NormalText']
    ))

    doc.build(story, canvasmaker=make_canvas_class("SAPPHIRE SPECIFICATION MANUAL"))


def main():
    print("🚀 Generating Sapphire PDF Manuals...")
    
    # Generate into sapphire_lang/ and docs/
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
    os.makedirs(docs_dir, exist_ok=True)

    files_map = {
        "Sapphire_Coding_and_Usage_Guide.pdf": generate_coding_guide,
        "Building_Advanced_Autonomous_AI.pdf": generate_advanced_ai_guide,
        "Sapphire_Autonomy_and_Performance_Benchmarks.pdf": generate_benchmarks_pdf,
        "Beginners_Guide_Your_First_Autonomous_AI.pdf": generate_beginner_guide,
        "Sapphire_Language_Specification_and_Automation_Manual.pdf": generate_pdf_manual
    }

    for fname, func in files_map.items():
        func(fname)
        shutil.copy2(fname, os.path.join(docs_dir, fname))
        print(f"✅ Generated & updated: {fname}")

    print("✨ All Sapphire PDF manuals generated successfully!")

if __name__ == "__main__":
    main()
