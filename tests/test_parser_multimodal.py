"""
Final Test for Issue #12: Document Intelligence Multimodal Demo
"""
import json
from agency.product.doc_parser import DocumentParser

def run_test():
    print("🚀 Starting Multimodal AI Parsing Test...")
    parser = DocumentParser("invoice")
    
    file_path = "data/samples/sample_invoice.png"
    
    try:
        result = parser.parse_file(file_path)
        print("\n📊 Extraction Result:")
        print(json.dumps(result, indent=2))
        
        if result.get("_status") == "success":
            print("\n✅ SUCCESS: Gemini Vision correctly parsed the invoice image.")
        else:
            print("\n❌ FAILURE: Extraction failed or returned errors.")
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR during test: {e}")

if __name__ == "__main__":
    run_test()
