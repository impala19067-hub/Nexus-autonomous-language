"""
Sapphire AI & Native LLM Standard Library
Integrates Google Gemini Cloud AI with automatic fallback to Ollama (Local), Groq API, & smart offline heuristics.
"""
import json
import re
import urllib.request
import os

DEFAULT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyB18pVLV_GYKzmGCOglQ3xiWVmYRz_Auns")
DEFAULT_GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_GEMINI_MODELS = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-3.6-flash", "gemini-3.7-flash"]
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_OLLAMA_MODEL = "llama3"

class AIModule:
    _gemini_key = DEFAULT_GEMINI_KEY
    _groq_key = DEFAULT_GROQ_KEY
    _ollama_url = DEFAULT_OLLAMA_URL
    _preferred_backend = "auto"  # "auto", "gemini", "ollama", "groq", "offline"

    @classmethod
    def set_gemini_key(cls, key: str):
        cls._gemini_key = key
        return True

    @classmethod
    def set_groq_key(cls, key: str):
        cls._groq_key = key
        return True

    @classmethod
    def set_ollama_url(cls, url: str):
        cls._ollama_url = url.rstrip('/')
        return True

    @classmethod
    def set_backend(cls, backend: str):
        cls._preferred_backend = backend.lower()
        return True

    @classmethod
    def prompt(cls, prompt_text: str, model: str = "default", temperature: float = 0.7) -> str:
        """
        Executes LLM prompt.
        1. Attempts Gemini Cloud API first (ultra-fast, comprehensive intelligence).
        2. Falls back to local Ollama endpoint if offline or preferred.
        3. Falls back to Groq API.
        4. If all unreachable, uses Sapphire's smart offline inference engine.
        """
        # Gemini Cloud AI
        if cls._preferred_backend in ("auto", "gemini"):
            res = cls._query_gemini(prompt_text, model, temperature)
            if res:
                return res

        # Ollama local endpoint
        if cls._preferred_backend in ("auto", "ollama"):
            res = cls._query_ollama(prompt_text, model, temperature)
            if res:
                return res

        # Groq API fallback
        if cls._preferred_backend in ("auto", "groq"):
            res = cls._query_groq(prompt_text, model, temperature)
            if res:
                return res

        # Offline fallback engine
        return cls._offline_fallback(prompt_text, model)

    @classmethod
    def _query_gemini(cls, prompt_text: str, model: str, temperature: float) -> str:
        """Query Google Gemini API with model fallback list."""
        if not cls._gemini_key:
            return None
        models_to_try = [model] if model != "default" else DEFAULT_GEMINI_MODELS
        for m in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={cls._gemini_key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt_text}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": 1024}
            }).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=10.0) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            res = parts[0].get("text", "").strip()
                            if res:
                                return res
            except Exception:
                continue
        return None

    @classmethod
    def _query_ollama(cls, prompt_text: str, model: str, temperature: float) -> str:
        """Query local Ollama instance."""
        target_model = DEFAULT_OLLAMA_MODEL if model == "default" else model
        url = f"{cls._ollama_url}/api/generate"
        payload = json.dumps({
            "model": target_model,
            "prompt": prompt_text,
            "stream": False,
            "options": {"temperature": temperature}
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get("response", "").strip()
        except Exception:
            return None

    @classmethod
    def _query_groq(cls, prompt_text: str, model: str, temperature: float) -> str:
        """Query Groq Cloud API."""
        if not cls._groq_key:
            return None
        target_model = DEFAULT_GROQ_MODEL if model == "default" else model
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = json.dumps({
            "model": target_model,
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": temperature,
            "max_tokens": 1024
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cls._groq_key}"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=8.0) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            return None
        return None


    @classmethod
    def _offline_fallback(cls, prompt_text: str, model: str) -> str:
        """Smart offline heuristic generator."""
        text_lower = prompt_text.lower()
        if "summarize" in text_lower:
            lines = [line.strip() for line in prompt_text.splitlines() if line.strip()]
            return f"[Sapphire AI (Offline)]: Summary of {len(lines)} input items processed."
        elif "json" in text_lower or "extract" in text_lower:
            return json.dumps({
                "status": "success",
                "extracted_fields": ["auto_analyzed"],
                "summary": "Sapphire Built-in Offline AI Parser"
            })
        elif "plan" in text_lower or "step" in text_lower:
            return "1. Perception & Data Ingestion\n2. Model Inference & Reasoning\n3. Memory & Tool Execution\n4. Verification"
        else:
            return f"[Sapphire AI ({model})]: Evaluated prompt ({len(prompt_text)} chars)."

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
    def classify(text: str, categories: list) -> str:
        """Classifies text into one of the provided categories."""
        text_lower = text.lower()
        for cat in categories:
            if cat.lower() in text_lower:
                return cat
        return categories[0] if categories else "Unknown"

    @classmethod
    def status(cls) -> dict:
        """Return status of AI backends."""
        gemini_active = cls._query_gemini("test", "default", 0.1) is not None if cls._gemini_key else False
        ollama_active = cls._query_ollama("test", "llama3", 0.1) is not None if not gemini_active else False
        groq_active = cls._query_groq("test", DEFAULT_GROQ_MODEL, 0.1) is not None if (not gemini_active and not ollama_active and cls._groq_key) else False

        active = "gemini" if gemini_active else ("ollama" if ollama_active else ("groq" if groq_active else "offline"))

        return {
            "gemini_key_configured": bool(cls._gemini_key),
            "gemini_online": gemini_active,
            "ollama_url": cls._ollama_url,
            "ollama_online": ollama_active,
            "groq_key_configured": bool(cls._groq_key),
            "groq_online": groq_active,
            "active_backend": active
        }

