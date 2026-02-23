"""
ProposalDrafter: Automatically generates a Markdown Technical Proposal Outline
based on the "Bases Técnicas" analysis extracted by TenderAnalyzer.
"""
import json
import os
from typing import Dict, Any
from datetime import datetime
from agency.utils.gemini_client import generate

class ProposalDrafter:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name

    def draft_proposal(self, analysis_data: Dict[str, Any]) -> str:
        
        # We only draft if the analyzer recommends bidding
        if not analysis_data.get("bid_recommendation", False):
            print("❌ Analyzer recommended NO-BID. Skipping proposal generation.")
            return ""

        print(f"✍️ Drafting Technical Proposal for: {analysis_data.get('tender_title')}...")
        
        prompt = self._build_prompt(analysis_data)
        draft = generate(prompt, model_name=self.model_name)
        
        self._save_draft(draft, analysis_data.get("tender_title", "Tender"))
        return draft

    def _build_prompt(self, data: Dict[str, Any]) -> str:
        reqs = "\n- ".join(data.get("key_requirements", []))
        docs = "\n- ".join(data.get("required_documents", []))
        
        return f"""
        You are an expert Bid Writer for a B2B Automation Agency specializing in AI Document Parsing.
        We have decided to bid on the following government tender:
        
        **Project Name**: {data.get('tender_title')}
        **Budget**: {data.get('estimated_budget')}
        **Key Technical Requirements**:
        - {reqs}
        
        **Admin Documents to prepare**:
        - {docs}
        
        Draft a "Technical Proposal Outline" (in Spanish, formatted in Markdown) that we can use as the basis for our final PDF submission.
        
        The outline should include:
        1. Executive Summary: Why our AI pipeline is the perfect fit.
        2. Proposed Solution Architecture: Explain how we will use OCR + Gemini + Secure Cloud Infrastructure to meet their key requirements.
        3. Compliance Matrix: A checklist showing how we meet exactly what they asked for.
        4. Next Steps & Admin Checklist: A reminder of all the Admin Documents we need to attach.
        
        Keep it professional, confident, and highly tailored to their specific technical requirements.
        """

    def _save_draft(self, draft: str, title: str):
        safe_title = "".join(c if c.isalnum() else "_" for c in title)[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"outbox/proposal_{safe_title}_{timestamp}.md"
        
        os.makedirs("outbox", exist_ok=True)
        with open(filepath, "w") as f:
            f.write(draft)
        
        print(f"✅ Technical Proposal Draft saved to: {filepath}")

# For standalone testing
if __name__ == "__main__":
    from agency.product.tender_analyzer import TenderAnalyzer
    analyzer = TenderAnalyzer()
    test_file = "data/samples/sample_bases_tecnicas.txt"
    if os.path.exists(test_file):
        analysis = analyzer.analyze_file(test_file)
        drafter = ProposalDrafter()
        drafter.draft_proposal(analysis)
