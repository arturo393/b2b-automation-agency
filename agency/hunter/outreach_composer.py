"""
OutreachComposer — writes personalized cold emails using Vertex AI (ADC).
"""
from typing import Dict
from agency.utils.gemini_client import generate


class OutreachComposer:
    """Generates a personalized cold email for a qualified lead."""

    def compose_email(self, lead: Dict) -> str:
        company = lead.get("company_name", "your company")
        industry = lead.get("industry", "your industry")
        pain = lead.get("pain_points", ["manual processes"])
        opportunity = lead.get("automation_opportunity", "process automation")

        prompt = f"""
        Write a short B2B cold email.

        Sender: Arturo (AI Automation Engineer, B2B Automation Agency)
        Recipient: Decision-maker at {company} ({industry})

        Context:
        - Pain points detected: {pain}
        - Automation idea: {opportunity}

        Rules:
        - Max 5 sentences in body.
        - No "I hope this finds you well".
        - Lead with a specific insight about their business (use pain_points).
        - Close with: "Open to a 5-min loom demo?"
        - Subject line should be curiosity-driven.

        Format:
        Subject: <subject line>

        <email body>
        """

        try:
            return generate(prompt)
        except Exception as e:
            return f"Error composing email: {e}"
