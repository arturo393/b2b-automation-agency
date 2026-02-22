"""
DocumentParser — extracts structured data from PDFs using Gemini.
This is "The Product" we sell to B2B clients.
Use case: Parse invoices, contracts, purchase orders → structured JSON.
"""
import json
from pathlib import Path
from typing import Dict
from agency.utils.gemini_client import generate, generate_multimodal


class DocumentParser:
    """
    Extracts structured data from documents using Gemini Vision.
    Supports PDF and images.
    """

    DOCUMENT_TYPES = {
        "invoice": {
            "fields": ["invoice_number", "date", "vendor_name", "total_amount",
                       "line_items", "tax", "payment_terms"],
            "description": "a supplier invoice or bill"
        },
        "contract": {
            "fields": ["parties", "effective_date", "expiry_date", "obligations",
                       "payment_terms", "jurisdiction"],
            "description": "a legal contract or agreement"
        },
        "purchase_order": {
            "fields": ["po_number", "date", "buyer", "supplier", "items",
                       "total_value", "delivery_date"],
            "description": "a purchase order"
        }
    }

    def __init__(self, doc_type: str = "invoice"):
        if doc_type not in self.DOCUMENT_TYPES:
            raise ValueError(f"Unsupported doc_type. Choose from: {list(self.DOCUMENT_TYPES.keys())}")
        self.doc_type = doc_type
        self.config = self.DOCUMENT_TYPES[doc_type]

    def parse_file(self, file_path: str) -> Dict:
        """Parse a local PDF or image file via Multimodal Gemini."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"📄 Parsing {self.doc_type}: {path.name}...")
        prompt = self._build_prompt()
        
        # Use our multimodal REST client
        raw = generate_multimodal(prompt, file_path, model_name="gemini-2.5-flash")
        
        return self._parse_response(raw, path.name)

    def parse_text(self, text: str) -> Dict:
        """Parse raw text (for testing without a real file)."""
        print(f"📝 Parsing {self.doc_type} from text ({len(text)} chars)...")
        prompt = self._build_prompt() + f"\n\nDocument text:\n{text}"
        raw = generate(prompt)
        return self._parse_response(raw, source="text_input")

    def _build_prompt(self) -> str:
        fields = self.config["fields"]
        return f"""
        This document is {self.config['description']}.
        
        Extract the following fields and return ONLY valid JSON (no markdown):
        {json.dumps({f: "<value or null>" for f in fields}, indent=2)}
        
        Rules:
        - Use null for missing fields.
        - Normalize monetary values to floats (e.g. "$ 1,500.00" → 1500.0).
        - Dates in ISO 8601 format (YYYY-MM-DD).
        - Line items as array of objects.
        """

    def _parse_response(self, raw: str, source: str) -> Dict:
        try:
            cleaned = raw.strip()
            if "{" in cleaned:
                cleaned = cleaned[cleaned.find("{"):cleaned.rfind("}")+1]
            result = json.loads(cleaned)
            result["_source"] = source
            result["_doc_type"] = self.doc_type
            result["_status"] = "success"
            print(f"   ✅ Extracted {len(result)} fields.")
            return result
        except Exception as e:
            print(f"   ❌ Parse error: {e}\n   Raw: {raw[:200]}")
            return {"_status": "error", "_error": str(e), "_raw": raw[:500]}
