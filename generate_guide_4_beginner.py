import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from doc_helpers import get_styles, code_box, callout_box, cover_banner, make_canvas_class

def generate_beginner_guide(filename="Beginners_Guide_Your_First_Autonomous_AI.pdf"):
    styles = get_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    # ================= COVER =================
    story.append(cover_banner(
        "BEGINNER'S GUIDE: YOUR FIRST AUTONOMOUS AI",
        "Step-by-Step Friendly Introduction to Building Intelligent Autonomous AI Bots with Sapphire",
        "Version 1.0.0 (Beginner Edition)", styles
    ))
    story.append(Spacer(1, 15))

    # ================= CHAPTER 1 =================
    story.append(Paragraph("1. Welcome! What is an Autonomous AI Agent?", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Welcome to the exciting world of <b>Autonomous AI Programming</b> with Sapphire! "
        "If you have never built an AI before, do not worry. An <b>Autonomous AI Agent</b> is simply a computer program "
        "that can observe what is happening on your computer, think about what needs to be done using AI, and take action automatically.",
        styles['NormalText']
    ))
    story.append(callout_box(
        "Analogy: Chatbot vs Autonomous Agent",
        "• <b>Chatbot:</b> Like a friend who only replies when you send a text.<br/>"
        "• <b>Autonomous Agent:</b> Like a dedicated assistant who monitors your computer, fixes problems, trains smart models, and works 24/7 in the background without needing to be asked!",
        styles, "tip"
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. The 3 Steps of Every Autonomous Bot", styles['CustomH1']))
    story.append(Paragraph(
        "Every autonomous bot in Sapphire follows 3 simple steps:",
        styles['NormalText']
    ))
    story.append(Paragraph("<b>Step 1: Check the System (Perception)</b> — The bot reads system metrics like RAM, CPU, or files using <code>os.system_info()</code>.", styles['BulletText']))
    story.append(Paragraph("<b>Step 2: Ask the AI (Intelligence)</b> — The bot sends system data to <code>ai.prompt(...)</code> for decision making.", styles['BulletText']))
    story.append(Paragraph("<b>Step 3: Perform Action (Execution)</b> — The bot posts desktop alerts with <code>os.notify()</code> or executes commands.", styles['BulletText']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Writing Your Very First 5-Line AI Agent", styles['CustomH1']))
    story.append(Paragraph(
        "Here is the simplest complete Autonomous AI Agent written in Sapphire (.sp):",
        styles['NormalText']
    ))

    code_beginner = """// 5-Line Autonomous AI Agent in Sapphire (.sp)
let info = os.system_info();
let question = "System CPU is at {info.cpu_usage_percent}%. Recommend optimization action.";
let ai_opinion = ai.prompt(question);

os.notify("Sapphire Agent Alert", ai_opinion);
print("🤖 Agent Output: {ai_opinion}");"""
    story.append(code_box(code_beginner, styles))

    story.append(PageBreak())

    # ================= CHAPTER 4 =================
    story.append(Paragraph("4. Line-by-Line Code Breakdown", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    
    explanation_data = [
        [Paragraph("<b>Code Line</b>", styles['CalloutTitle']), Paragraph("<b>What It Does (Beginner Friendly)</b>", styles['CalloutTitle'])],
        [Paragraph("<code>let info = os.system_info();</code>", styles['CodeText']), Paragraph("Gets live CPU, RAM, and disk usage from your computer.", styles['NormalText'])],
        [Paragraph("<code>let question = \"...\";</code>", styles['CodeText']), Paragraph("Constructs a prompt string with your CPU percentage.", styles['NormalText'])],
        [Paragraph("<code>let ai_opinion = ai.prompt(question);</code>", styles['CodeText']), Paragraph("Passes the question to Sapphire's native AI engine.", styles['NormalText'])],
        [Paragraph("<code>os.notify(\"...\");</code>", styles['CodeText']), Paragraph("Displays a pop-up toast notification on your Windows desktop!", styles['NormalText'])],
        [Paragraph("<code>print(\"...\");</code>", styles['CodeText']), Paragraph("Prints the AI's recommendations to your screen.", styles['NormalText'])],
    ]
    t_explain = Table(explanation_data, colWidths=[200, 304])
    t_explain.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_explain)
    story.append(Spacer(1, 12))

    story.append(Paragraph("5. How to Run Your Agent", styles['CustomH1']))
    story.append(Paragraph(
        "You can run your Sapphire AI agent in 3 easy ways:",
        styles['NormalText']
    ))
    story.append(Paragraph("<b>Option A (Emerald Developer Studio)</b>: Double-click <code>Emerald_Studio.exe</code>, select the 'Auto Agent' template, and click ▶ Run.", styles['BulletText']))
    story.append(Paragraph("<b>Option B (Command Line)</b>: Open terminal and type <code>sapphire run bot.sp</code>.", styles['BulletText']))
    story.append(Paragraph("<b>Option C (Voice Tutor)</b>: Double-click <code>sapphire_voice_tutor.exe</code> for audio guided practice.", styles['BulletText']))
    story.append(Spacer(1, 10))

    story.append(callout_box(
        "🎉 Next Steps & Challenges",
        "Try customizing the prompt to inspect RAM load, or use `scheduler.interval(60.0, fn)` to make your bot monitor your PC every minute automatically!",
        styles, "tip"
    ))

    doc.build(story, canvasmaker=make_canvas_class("BEGINNER'S GUIDE TO SAPPHIRE AI"))
    print(f"[OK] Generated {filename}")

if __name__ == "__main__":
    generate_beginner_guide()
