
import random
import time
from typing import List, Dict
try:
    from googlesearch import search
except ImportError:
    print("⚠️  To use real Google Search: pip install googlesearch-python")
    search = None

class LeadHunter:
    """
    The Hunter finds potential clients on Google.
    It looks for businesses that likely have manual processes.
    """
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]

    def hunt(self, keyword: str, num_results: int = 10) -> List[Dict]:
        """
        Search for leads based on a keyword.
        Returns a list of potential leads with URL and basic metadata.
        """
        print(f"🕵️  Hunting for leads: '{keyword}'...")
        
        leads = []
        
        if not search:
            # Mock behavior if library missing
            print("🔹 Using Mock Search Results (Install googlesearch-python for real data)")
            return [
                {"url": "https://example-logistics-chile.cl", "title": "Logistica Chile Ltda"},
                {"url": "https://importadora-manual.com", "title": "Importadora Manual SA"}
            ]

        try:
            # Add "contact" or "about us" to find relevant pages
            query = f"{keyword} site:.cl" # Focusing on Chile/LATAM for now
            
            # Simple search (returns strings)
            results = list(search(query, num_results=num_results))
            
            for url in results:
                # Random delay to be polite
                time.sleep(random.uniform(1, 2))
                
                lead = {
                    "url": url,
                    "title": f"Business at {url}", # Placeholder as simple search might not give title
                    "description": "Potential lead found via search."
                }
                print(f"   🎯 Found: {url}")
                leads.append(lead)
                
            if not leads:
                 print("⚠️  Google returned 0 results. Using Fallback Mock Data for demo.")
                 return [
                    {"url": "https://agencia-ejemplo.cl", "title": "Agencia Aduana Ejemplo", "description": "Tramites manuales de importacion"},
                    {"url": "https://logistica-antigua.cl", "title": "Logistica Ltda", "description": "Envienos sus facturas por fax"}
                ]
                
        except Exception as e:
            print(f"❌ Search Error: {e}")
            print("⚠️  Using Fallback Mock Data due to error.")
            return [
                {"url": "https://agencia-ejemplo.cl", "title": "Agencia Aduana Ejemplo", "description": "Tramites manuales de importacion"},
                {"url": "https://logistica-antigua.cl", "title": "Logistica Ltda", "description": "Envienos sus facturas por fax"}
            ]
            
        print(f"✅ Found {len(leads)} raw leads.")
        return leads
