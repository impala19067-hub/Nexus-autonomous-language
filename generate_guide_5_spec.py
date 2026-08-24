import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from doc_helpers import get_styles, code_box, callout_box, cover_banner, make_canvas_class

def generate_pdf_manual(filename="Sapphire_Language_Specification_and_Automation_Manual.pdf"):
    styles = get_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    # ================= COVER =================
    story.append(cover_banner(
        "SAPPHIRE PROGRAMMING LANGUAGE",
        "Formal Language Specification, AST Grammar, Standard Library Architecture & Automation Manual",
        "Version 1.0.0 (Core Architecture Spec)", styles
    ))
    story.append(Spacer(1, 15))

    # ================= SECTION 1 =================
    story.append(Paragraph("1. Executive Specification & Grammar Architecture", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "This document defines the formal language specification and runtime standard library for the <b>Sapphire Programming Language</b>. "
        "Sapphire is parsed using a recursive-descent syntax tree generator and executed via an AST visitor runtime with lexically scoped environments.",
        styles['NormalText']
    ))
    
    ebnf_text = """Program        ::= Statement*
Statement      ::= VarDecl | AssignStmt | FnDecl | ReturnStmt | IfStmt 
                 | WhileStmt | ForStmt | ParallelStmt | ExprStmt
VarDecl        ::= "let" IDENTIFIER (":" Type)? ("=" Expression)? ";"
FnDecl         ::= "fn" IDENTIFIER "(" ParamList? ")" ("->" Type)? Block
ParallelStmt   ::= "parallel" Block
PipeExpr       ::= LogicalOr ( "|>" LogicalOr )*
MemberAccess   ::= Primary ( "." IDENTIFIER | "[" Expression "]" | "(" ArgList? ")" )*"""
    story.append(code_box(ebnf_text, styles))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ================= SECTION 2 =================
    story.append(Paragraph("2. Lexical Tokens, Keywords & Operators", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))

    token_data = [
        [Paragraph("<b>Category</b>", styles['CalloutTitle']), Paragraph("<b>Token Literals</b>", styles['CalloutTitle']), Paragraph("<b>Semantic Description</b>", styles['CalloutTitle'])],
        [Paragraph("Keywords", styles['NormalText']), Paragraph("<code>let, fn, return, if, else, while, for, in, parallel, break, continue</code>", styles['CodeText']), Paragraph("Reserved language grammar keywords.", styles['NormalText'])],
        [Paragraph("Operators", styles['NormalText']), Paragraph("<code>+, -, *, /, %, ==, !=, &lt;, &gt;, &lt;=, &gt;=, and, or, not, |&gt;</code>", styles['CodeText']), Paragraph("Arithmetic, logical, comparison, and stream piping.", styles['NormalText'])],
        [Paragraph("Literals", styles['NormalText']), Paragraph("<code>42, 3.1415, \"hello\", true, false, null, [1, 2], {\"k\": \"v\"}</code>", styles['CodeText']), Paragraph("Numbers, strings, booleans, null, arrays, maps.", styles['NormalText'])],
    ]
    t_tok = Table(token_data, colWidths=[90, 214, 200])
    t_tok.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_tok)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Runtime Execution & Scoping Rules", styles['CustomH1']))
    story.append(Paragraph(
        "Sapphire employs a hierarchical lexically scoped environment model. Inner blocks inherit bindings from enclosing parent environments. "
        "Green fiber concurrency within <code>parallel { ... }</code> blocks encapsulates memory isolation while allowing structured rendezvous synchronization.",
        styles['NormalText']
    ))

    story.append(PageBreak())

    # ================= SECTION 4 =================
    story.append(Paragraph("4. Deep Learning Standard Library (ml)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))

    spec_ml = [
        [Paragraph("<b>Function</b>", styles['CalloutTitle']), Paragraph("<b>Signature</b>", styles['CalloutTitle']), Paragraph("<b>Description</b>", styles['CalloutTitle'])],
        [Paragraph("<code>ml.tensor</code>", styles['CodeText']), Paragraph("<code>ml.tensor(data, dtype, device)</code>", styles['CodeText']), Paragraph("Constructs N-dimensional tensor.", styles['NormalText'])],
        [Paragraph("<code>ml.autograd.tape</code>", styles['CodeText']), Paragraph("<code>ml.autograd.tape()</code>", styles['CodeText']), Paragraph("Context manager for automatic differentiation.", styles['NormalText'])],
        [Paragraph("<code>ml.model.mlp</code>", styles['CodeText']), Paragraph("<code>ml.model.mlp(layers, act)</code>", styles['CodeText']), Paragraph("Builds multi-layer perceptron neural model.", styles['NormalText'])],
        [Paragraph("<code>ml.train.fit</code>", styles['CodeText']), Paragraph("<code>ml.train.fit(model, ds, loss, opt, ...)</code>", styles['CodeText']), Paragraph("Trains model across N data-parallel workers.", styles['NormalText'])],
        [Paragraph("<code>ml.gpu.info</code>", styles['CodeText']), Paragraph("<code>ml.gpu.info() -> Array[Map]</code>", styles['CodeText']), Paragraph("Queries NVIDIA CUDA GPU telemetry.", styles['NormalText'])],
        [Paragraph("<code>ml.kernel.conv2d</code>", styles['CodeText']), Paragraph("<code>ml.kernel.conv2d(img, kernel)</code>", styles['CodeText']), Paragraph("Applies 2D convolution kernel filter.", styles['NormalText'])],
    ]
    t_ml = Table(spec_ml, colWidths=[100, 200, 204])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Autonomous Agent Standard Library (agent)", styles['CustomH1']))
    spec_agent = [
        [Paragraph("<b>Function</b>", styles['CalloutTitle']), Paragraph("<b>Signature</b>", styles['CalloutTitle']), Paragraph("<b>Description</b>", styles['CalloutTitle'])],
        [Paragraph("<code>agent.memory.remember</code>", styles['CodeText']), Paragraph("<code>remember(key, val, embedding=None)</code>", styles['CodeText']), Paragraph("Saves knowledge into vector memory store.", styles['NormalText'])],
        [Paragraph("<code>agent.memory.recall</code>", styles['CodeText']), Paragraph("<code>recall(key) -> Any</code>", styles['CodeText']), Paragraph("Recalls value from memory store.", styles['NormalText'])],
        [Paragraph("<code>agent.planning.create_plan</code>", styles['CodeText']), Paragraph("<code>create_plan(goal: str) -> Plan</code>", styles['CodeText']), Paragraph("Generates 4-step DAG action plan.", styles['NormalText'])],
        [Paragraph("<code>agent.tools.register</code>", styles['CodeText']), Paragraph("<code>register(name, desc, fn)</code>", styles['CodeText']), Paragraph("Registers runtime executable tool.", styles['NormalText'])],
        [Paragraph("<code>agent.autonomy.run_loop</code>", styles['CodeText']), Paragraph("<code>run_loop(goal, max_steps)</code>", styles['CodeText']), Paragraph("Executes autonomous self-correcting agent loop.", styles['NormalText'])],
    ]
    t_ag = Table(spec_agent, colWidths=[120, 190, 194])
    t_ag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ag)

    story.append(PageBreak())

    # ================= SECTION 6 =================
    story.append(Paragraph("6. System Automation Standard Library (os, fs, gui, http)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))

    spec_os = [
        [Paragraph("<b>API</b>", styles['CalloutTitle']), Paragraph("<b>Signature</b>", styles['CalloutTitle']), Paragraph("<b>Description</b>", styles['CalloutTitle'])],
        [Paragraph("<code>os.system_info</code>", styles['CodeText']), Paragraph("<code>os.system_info() -> Map</code>", styles['CodeText']), Paragraph("Returns CPU, RAM, and Disk metrics.", styles['NormalText'])],
        [Paragraph("<code>os.notify</code>", styles['CodeText']), Paragraph("<code>os.notify(title, msg) -> Void</code>", styles['CodeText']), Paragraph("Displays native OS desktop notification toast.", styles['NormalText'])],
        [Paragraph("<code>fs.read / fs.write</code>", styles['CodeText']), Paragraph("<code>fs.read(path) / fs.write(path, data)</code>", styles['CodeText']), Paragraph("Reads and writes filesystem files.", styles['NormalText'])],
        [Paragraph("<code>gui.click / gui.alert</code>", styles['CodeText']), Paragraph("<code>gui.click(x, y) / gui.alert(msg, title)</code>", styles['CodeText']), Paragraph("Simulates mouse clicks and modal popups.", styles['NormalText'])],
        [Paragraph("<code>http.get / http.post</code>", styles['CodeText']), Paragraph("<code>http.get(url) / http.post(url, json)</code>", styles['CodeText']), Paragraph("Performs REST network requests.", styles['NormalText'])],
        [Paragraph("<code>scheduler.interval</code>", styles['CodeText']), Paragraph("<code>scheduler.interval(secs, fn)</code>", styles['CodeText']), Paragraph("Schedules recurring background execution.", styles['NormalText'])],
    ]
    t_os = Table(spec_os, colWidths=[110, 190, 204])
    t_os.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_os)

    doc.build(story, canvasmaker=make_canvas_class("SAPPHIRE SPECIFICATION MANUAL"))
    print(f"[OK] Generated {filename}")

if __name__ == "__main__":
    generate_pdf_manual()
