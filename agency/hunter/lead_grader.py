"""
LeadGrader — uses Vertex AI (ADC) to score how much a company needs automation.
"""
import json
from typing import Dict
from agency.utils.gemini_client import generate


class LeadGrader:
    """Evaluates a lead and scores their automation potential (0-10)."""

    def grade_lead(self, lead: Dict, page_text: str = "") -> Dict:
        print(f"🧠 Grading: {lead.get('title', 'Unknown')}...")

        if len(page_text) < 50:
            return {**lead, "score": 0, "reason": "No content to analyze"}

        prompt = f"""
        You are a B2B Sales Expert identifying companies that need PROCESS AUTOMATION.

        Company URL: {lead.get('url')}
        Website text:
        {page_text[:4000]}

        Look for signals of:
        1. Manual processes ("Send us your PDF", "Fax us", "Fill this form")
        2. High-volume ops (logistics, legal, insurance, real estate)
        3. No mention of modern tools (ERP, API integrations, etc.)

        Respond with ONLY valid JSON (no markdown):
        {{
            "score": <integer 0-10>,
            "company_name": "<name>",
            "industry": "<industry>",
            "pain_points": ["<point 1>", "<point 2>"],
            "automation_opportunity": "<one sentence idea>"
        }}
        """

        try:
            raw = generate(prompt)
            cleaned = raw.strip()
            if "{" in cleaned:
                cleaned = cleaned[cleaned.find("{"):cleaned.rfind("}")+1]
            analysis = json.loads(cleaned)
            print(f"   ✅ Score: {analysis.get('score')}/10 — {analysis.get('automation_opportunity', '')[:60]}")
            return {**lead, **analysis}
        except Exception as e:
            print(f"   ❌ Grading Error: {e}")
            return {**lead, "score": 0, "reason": str(e)}
