from __future__ import annotations

from typing import Optional

from app.core.config import settings

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None


class GeminiService:
    def __init__(self) -> None:
        self.enabled = bool(settings.gemini_api_key and genai)
        if self.enabled:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def generate_text(self, prompt: str, fallback: str) -> str:
        if not self.enabled or self.model is None:
            return fallback
        try:
            response = self.model.generate_content(prompt, request_options={"timeout": 10})
            text = getattr(response, "text", "") or fallback
            return text.strip()
        except Exception:
            return fallback
