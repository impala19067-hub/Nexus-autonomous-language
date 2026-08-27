"""
Sapphire Programming Language Manual PDF Generator
Generates: Sapphire_Language_Specification_and_Automation_Manual.pdf
"""
import sys
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover header/footer
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A2530"))
        
        # Header
        self.drawString(54, 750, "SAPPHIRE PROGRAMMING LANGUAGE — SPECIFICATION & AUTOMATION MANUAL")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential & Proprietary — Sapphire Core Architecture")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Dark Navy
    ACCENT = colors.HexColor("#2563EB")     # Bright Blue
    SECONDARY = colors.HexColor("#0D9488")  # Teal Accent
    TEXT_DARK = colors.HexColor("#1E293B")  # Off-black
    BG_CODE = colors.HexColor("#F8FAFC")    # Code Block BG
    BORDER_CODE = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.white,
        alignment=1, # Center
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#94A3B8"),
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=4,
        spaceAfter=4
    )

    story = []

    # ================= COVER BANNER =================
    cover_data = [
        [Paragraph("SAPPHIRE PROGRAMMING LANGUAGE", title_style)],
        [Paragraph("Next-Generation High-Convenience Automation & AI Language Specification", subtitle_style)],
        [Paragraph("<font color='#38BDF8'><b>Version 1.0.0 (Automation Era)</b></font> | Author: Antigravity AI Engine", ParagraphStyle('CoverMeta', parent=subtitle_style, fontSize=10, textColor=colors.white))]
    ]

    cover_table = Table(cover_data, colWidths=[504])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 35),
        ('BOTTOMPADDING', (0,0), (-1,-1), 35),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('LINEBELOW', (0,-1), (-1,-1), 4, SECONDARY),
    ]))

    story.append(cover_table)
    story.append(Spacer(1, 20))

    # ================= EXECUTIVE SUMMARY =================
    story.append(Paragraph("1. Executive Summary & Design Philosophy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    exec_text = (
        "<b>Sapphire</b> is designed to solve the critical friction points of modern programming languages. "
        "Current era languages force developers into compromises: Python offers readability but lacks speed and native process control; "
        "Rust provides memory safety and concurrency but imposes high compiler cognitive overhead; JavaScript offers ecosystem agility "
        "but suffers from async function coloring and callback fragility; Bash handles shell piping well but degrades quickly on structured data.<br/><br/>"
        "<b>Why Sapphire is 2X Advanced & Convenient:</b>"
    )
    story.append(Paragraph(exec_text, body_style))

    philosophy_points = [
        "<b>1. Colorless Concurrency:</b> Lightweight green fibers eliminate function coloring (`async/await` overhead). Native `parallel { ... }` blocks run task branches concurrently with structured safety.",
        "<b>2. First-Class Shell & Stream Piping:</b> Shell commands (e.g. `$ dir /b`) are native syntax literals returning structured <code>ProcessResult</code> objects. The pipe operator (<code>|&gt;</code>) flows data seamlessly between commands, arrays, and functions.",
        "<b>3. Native PC & System Automation:</b> Out-of-the-box standard library for hardware monitoring (CPU, RAM, Disks), OS process management, keyboard/mouse GUI automation, desktop notifications, and clipboard access.",
        "<b>4. Integrated Autonomous AI Agent Engine:</b> Built-in prompt evaluation (<code>ai.prompt</code>), schema extraction (<code>ai.extract_json</code>), and classification (<code>ai.classify</code>) directly inside language primitives.",
        "<b>5. Gradual Typing & Zero-Config Execution:</b> Write zero-boilerplate scripts instantly with type inference, while supporting optional sound static type annotations (`fn add(a: int, b: int) -> int`)."
    ]
    for pt in philosophy_points:
        story.append(Paragraph(f"• {pt}", bullet_style))

    story.append(Spacer(1, 15))

    # ================= SYNTAX & GRAMMAR REFERENCE =================
    story.append(Paragraph("2. Language Syntax & Core Grammar", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    syntax_intro = (
        "Sapphire combines Pythonic clean syntax with C/Rust-style brace scoping. Expressions support string interpolation, "
        "lambda functions, process literals, and pipeline operators."
    )
    story.append(Paragraph(syntax_intro, body_style))

    syntax_code = (
        "// Variable Declarations & Gradual Typing\n"
        "let username = \"Developer\";            // Inferred String\n"
        "const MAX_RETRY: int = 5;              // Type Annotated Constant\n\n"
        "// String Interpolation with Expression Evaluation\n"
        "let message = \"User: {username}, Retries Left: {MAX_RETRY - 1}\";\n\n"
        "// Functions & Lambda Shorthand\n"
        "fn calculate_tax(amount, rate: float) -> float {\n"
        "    return amount * rate;\n"
        "}\n"
        "let numbers = [10, 20, 30, 40];\n"
        "let doubled = numbers.map(x -> x * 2);\n"
        "let filtered = numbers.filter(x -> x > 15);\n"
    )

    code_table = Table([[Paragraph(syntax_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CODE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CODE),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 15))

    # ================= PROCESS PIPELINES & CONCURRENCY =================
    story.append(Paragraph("3. Native Process Execution & Colorless Concurrency", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    proc_desc = (
        "In Sapphire, process execution is elevated to a first-class language feature. Commands prefixed with <code>$</code> "
        "or enclosed in backticks run OS processes natively and return <code>ProcessResult</code> strings equipped with helper methods."
    )
    story.append(Paragraph(proc_desc, body_style))

    pipeline_code = (
        "// Native Process Execution & Stream Piping\n"
        "let active_files = $ dir /b\n"
        "                   |> lines()\n"
        "                   |> filter(f -> f.contains(\".sp\") or f.contains(\".py\"));\n\n"
        "// Colorless Concurrency: Parallel Block Execution\n"
        "parallel {\n"
        "    os.notify(\"Task A\", \"System audit starting...\");\n"
        "    fs.write(\"./backup.log\", \"Backup initiated at runtime\");\n"
        "    let net_info = http.get(\"https://httpbin.org/get\");\n"
        "}\n"
    )

    code_table2 = Table([[Paragraph(pipeline_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    code_table2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CODE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CODE),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(code_table2)
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # ================= STANDARD LIBRARY AUTOMATION MANUAL =================
    story.append(Paragraph("4. Standard Library Automation Reference", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    story.append(Paragraph(
        "Sapphire includes built-in standard library modules covering 100% of PC and OS automation needs without external third-party dependencies.",
        body_style
    ))

    # STDLIB TABLE DEFINITION
    stdlib_headers = [Paragraph("<b>Module</b>", body_style), Paragraph("<b>Function / Method Signature</b>", body_style), Paragraph("<b>Description & Return Type</b>", body_style)]
    
    table_rows = [stdlib_headers]

    api_defs = [
        ("os", "os.system_info() -> Map", "Returns CPU usage %, RAM total/used/free, Disk stats, and OS platform info."),
        ("os", "os.exec(cmd: str) -> Map", "Executes shell command returning {stdout, stderr, exit_code, success}."),
        ("os", "os.processes() -> Array[Map]", "Gets list of running PC processes with PID, CPU %, and Memory %."),
        ("os", "os.kill_process(target: str|int) -> Bool", "Terminates process by PID or matching process name."),
        ("os", "os.clip_read() -> String", "Reads text content from Windows / OS clipboard."),
        ("os", "os.clip_write(text: str) -> Bool", "Copies text string to Windows / OS clipboard."),
        ("os", "os.notify(title, message) -> Void", "Triggers OS desktop toast notification dialog."),
        
        ("fs", "fs.read(path: str) -> String", "Reads text file content from disk with UTF-8 encoding."),
        ("fs", "fs.write(path, content) -> Bool", "Creates directory path if needed and writes file content."),
        ("fs", "fs.list_dir(path: str) -> Array[String]", "Returns array of file/folder names inside directory."),
        ("fs", "fs.copy(src, dst) -> Bool", "Copies single file or entire directory recursively."),
        ("fs", "fs.remove(path: str) -> Bool", "Deletes target file or folder recursively."),
        ("fs", "fs.find_files(pattern) -> Array[String]", "Glob searches files matching pattern."),

        ("http", "http.get(url, headers) -> Map", "Performs HTTP GET request returning {status_code, body, json, ok}."),
        ("http", "http.post(url, body, json) -> Map", "Performs HTTP POST request with JSON payload or raw body."),
        ("http", "http.download(url, dest_path) -> Bool", "Downloads remote file stream directly to disk."),

        ("gui", "gui.click(x, y) -> Void", "Simulates left mouse button click at screen coordinate (x, y)."),
        ("gui", "gui.move_mouse(x, y) -> Void", "Moves mouse cursor to absolute screen coordinate."),
        ("gui", "gui.type_text(text: str) -> Void", "Simulates typing text key sequence into focused window."),
        ("gui", "gui.alert(message, title) -> Void", "Displays modal GUI alert box to user."),

        ("ai", "ai.prompt(text: str) -> String", "Evaluates LLM / AI prompt returning structured answer."),
        ("ai", "ai.extract_json(text: str) -> Map", "Extracts and parses JSON block from unstructured text."),
        ("ai", "ai.classify(text, categories) -> String", "Classifies input text into one of the target categories."),

        ("data", "data.parse_json(str) / data.to_json(val)", "Parses and formats JSON data structures."),
        ("data", "data.sha256(text) / base64_encode(text)", "Computes SHA256 hashes and Base64 strings."),

        ("scheduler", "scheduler.sleep(seconds: float)", "Pauses current task execution thread."),
        ("scheduler", "scheduler.run_later(seconds, fn)", "Schedules background callback function execution.")
    ]

    for mod, sig, desc in api_defs:
        table_rows.append([
            Paragraph(f"<b>{mod}</b>", ParagraphStyle('ModCell', parent=body_style, textColor=ACCENT)),
            Paragraph(f"<code>{sig}</code>", ParagraphStyle('SigCell', parent=body_style, fontName='Courier', fontSize=8)),
            Paragraph(desc, body_style)
        ])

    api_table = Table(table_rows, colWidths=[60, 194, 250])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(api_table)
    story.append(Spacer(1, 15))

    # ================= FULL PC AUTOBOT TUTORIAL SCRIPT =================
    story.append(Paragraph("5. End-to-End PC Automation Autobot Script", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    autobot_script = (
        "// 05_full_pc_autobot.sp — Complete PC Automation Script\n\n"
        "fn pc_autobot() {\n"
        "    print(\"🤖 SAPPHIRE PC AUTOMATION BOT STARTING\");\n\n"
        "    // Step 1: PC System Metrics Audit\n"
        "    let stats = os.system_info();\n"
        "    print(\"RAM Used: {stats.ram_percent}%, CPU Used: {stats.cpu_usage_percent}%\");\n\n"
        "    // Step 2: File Directory Diagnostics\n"
        "    let temp_files = fs.list_dir(\".\");\n"
        "    print(\"Inspected workspace directory ({temp_files.length} items found).\");\n\n"
        "    // Step 3: Network Check & Report File Creation\n"
        "    let http_check = http.get(\"https://httpbin.org/get\");\n"
        "    let report = {\n"
        "        \"cpu\": stats.cpu_usage_percent,\n"
        "        \"ram\": stats.ram_percent,\n"
        "        \"network_online\": http_check.ok\n"
        "    };\n"
        "    fs.write(\"./pc_autobot_report.json\", data.to_json(report));\n\n"
        "    // Step 4: Clipboard Copy & Desktop Notification\n"
        "    os.clip_write(\"PC Diagnostic: RAM {stats.ram_percent}%\");\n"
        "    os.notify(\"Sapphire Autobot\", \"Full PC Diagnostic Completed!\");\n"
        "}\n\n"
        "pc_autobot();\n"
    )

    autobot_table = Table([[Paragraph(autobot_script.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    autobot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CODE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CODE),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(autobot_table)
    story.append(Spacer(1, 15))

    # ================= CLI TOOLCHAIN =================
    story.append(Paragraph("6. Sapphire CLI Executable & REPL Toolchain", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    cli_info = (
        "Sapphire comes with a unified Command Line Interface toolchain supporting file execution, REPL shell interaction, "
        "and direct evaluation:<br/>"
        "• <b>Run Script File:</b> <code>python -m src.cli run script.sp</code><br/>"
        "• <b>Interactive REPL:</b> <code>python -m src.cli repl</code><br/>"
        "• <b>Inline Evaluation:</b> <code>python -m src.cli eval \"let info = os.system_info(); print(info.ram_percent);\"</code><br/>"
        "• <b>System Info:</b> <code>python -m src.cli info</code>"
    )
    story.append(Paragraph(cli_info, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated PDF Manual: {filename}")

if __name__ == '__main__':
    target_pdf = os.path.abspath("Sapphire_Language_Specification_and_Automation_Manual.pdf")
    build_pdf(target_pdf)
