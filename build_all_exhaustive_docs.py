import os
import shutil

from generate_guide_1_coding import generate_coding_guide
from generate_guide_2_ai import generate_advanced_ai_guide
from generate_guide_3_benchmarks import generate_benchmarks_pdf
from generate_guide_4_beginner import generate_beginner_guide
from generate_guide_5_spec import generate_pdf_manual

def build_all():
    print("🚀 Building Exhaustive Multi-Page Sapphire Documentation Suite...")
    
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "docs"))
    os.makedirs(docs_dir, exist_ok=True)
    
    generators = [
        ("Sapphire_Coding_and_Usage_Guide.pdf", generate_coding_guide),
        ("Building_Advanced_Autonomous_AI.pdf", generate_advanced_ai_guide),
        ("Sapphire_Autonomy_and_Performance_Benchmarks.pdf", generate_benchmarks_pdf),
        ("Beginners_Guide_Your_First_Autonomous_AI.pdf", generate_beginner_guide),
        ("Sapphire_Language_Specification_and_Automation_Manual.pdf", generate_pdf_manual)
    ]
    
    for fname, func in generators:
        func(fname)
        shutil.copy2(fname, os.path.join(docs_dir, fname))
        size_kb = os.path.getsize(fname) / 1024.0
        print(f"✅ Generated {fname} ({size_kb:.1f} KB)")
        
    print("\n✨ All 5 Comprehensive Sapphire PDF Manuals built and updated in docs/ and root!")

if __name__ == "__main__":
    build_all()
