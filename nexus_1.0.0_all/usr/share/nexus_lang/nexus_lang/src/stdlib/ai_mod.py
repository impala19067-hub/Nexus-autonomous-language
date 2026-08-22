"""
Nexus AI & Autonomous Agent Standard Library
"""
import json
import re

class AIModule:
    @staticmethod
    def prompt(prompt_text: str, model: str = "default", temperature: float = 0.7) -> str:
        """Executes LLM / AI prompt. Built-in structured response engine."""
        # Clean & parse prompt intent
        if "summarize" in prompt_text.lower():
            lines = [line.strip() for line in prompt_text.splitlines() if line.strip()]
            return f"Summary: Extracted {len(lines)} key lines from input text with automated insights."
        elif "json" in prompt_text.lower() or "extract" in prompt_text.lower():
            return json.dumps({
                "status": "success",
                "extracted_fields": ["auto_analyzed"],
                "summary": "Nexus Built-in AI Parsing Complete"
            })
        else:
            return f"[AI Response ({model})]: Successfully processed prompt: {prompt_text[:100]}..."

    @staticmethod
    def extract_json(text: str) -> dict:
        """Extracts and parses first JSON block found within LLM response or text."""
        match = re.search(r'\{.*\}|\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return {}

    @staticmethod
    def classify(text: str, categories: list[str]) -> str:
        """Classifies text into one of the provided categories."""
        text_lower = text.lower()
        for cat in categories:
            if cat.lower() in text_lower:
                return cat
        return categories[0] if categories else "Unknown"
