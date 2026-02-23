"""
TenderAnalyzer: Analyzes government "Bases Técnicas" (heavy text/pdfs) 
to extract structured requirements and evaluate B2B bidding opportunities.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any
from agency.utils.gemini_client import generate_multimodal, generate

class TenderAnalyzer:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Tender file not found: {file_path}")

        print(f"🏛️ Analyzing Tender Document: {path.name}...")
        
        prompt = self._build_prompt()
        
        # Use multimodal client (handles text files by sending base64 + correct mime)
        raw_response = generate_multimodal(prompt, file_path, model_name=self.model_name)
        return self._parse_json(raw_response)
        
    def _build_prompt(self) -> str:
        return """
        You are an expert Government Bidding Consultant.
        Read the attached tender document (Bases Técnicas/Administrativas).
        Extract the key aspects of the tender and evaluate if a B2B Automation Agency 
        (specializing in AI document parsing, data extraction, and OCR pipelines) should bid for this.

        Return a structured JSON object exactly like this, without any markdown formatting:
        {
          "tender_title": "string, the name of the project",
          "estimated_budget": "string, budget or 'Not specified'",
          "submission_deadline": "string, date/time",
          "key_requirements": ["string", "Top 3-5 technical MUST-HAVEs"],
          "required_documents": ["string", "Admin docs needed to apply (e.g. Boleta de Garantía, Anexos)"],
          "compliance_score": int, (0-10 score evaluating how well our AI Automation Pipeline fits the requirements),
          "bid_recommendation": boolean, (True if compliance_score >= 7, else False),
          "analysis_summary": "string, 2 sentences explaining why we should or shouldn't bid."
        }
        """

    def _parse_json(self, response: str) -> Dict[str, Any]:
        """Cleans Gemini's markdown wrapper if present and parses JSON."""
        clean = response.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
            
        try:
            return json.loads(clean.strip())
        except json.JSONDecodeError as e:
            print("Failed to parse JSON. Raw output:")
            print(response)
            raise ValueError("Gemini did not return valid JSON.") from e

if __name__ == "__main__":
    analyzer = TenderAnalyzer()
    test_file = "data/samples/sample_bases_tecnicas.txt"
    if os.path.exists(test_file):
        result = analyzer.analyze_file(test_file)
        print("\n📊 Tender Analysis Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
