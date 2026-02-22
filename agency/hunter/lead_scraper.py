"""
LeadScraper — finds potential B2B leads using Google Custom Search API.

Priority order:
1. Google Custom Search (100 free queries/day, uses existing GCP key)
2. googlesearch-python (free but often blocked)
3. Mock fallback (development only)

Setup for option 1:
  1. Go to https://programmablesearchengine.google.com/
  2. Create a search engine → get GOOGLE_CSE_ID
  3. Add to .env: GOOGLE_CSE_ID=<your_id>
  The GOOGLE_API_KEY in .env is reused for CSE billing.
"""
import os
import time
import random
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class LeadHunter:
    """Finds potential B2B leads via web search."""

    CSE_ENDPOINT = "https://www.googleapis.com/customsearch/v1"

    def hunt(self, keyword: str, num_results: int = 10) -> List[Dict]:
        print(f"🕵️  Hunting for leads: '{keyword}'...")

        leads = self._search_cse(keyword, num_results)
        if leads:
            return leads

        leads = self._search_googlesearch(keyword, num_results)
        if leads:
            return leads

        print("⚠️  All search methods failed. Using mock data for development.")
        return self._mock_leads()

    # ── Method 1: Google Custom Search API ────────────────────────────────
    def _search_cse(self, keyword: str, num_results: int) -> List[Dict]:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        cse_id = os.getenv("GOOGLE_CSE_ID")

        if not cse_id:
            print("   ℹ️  No GOOGLE_CSE_ID set — skipping Google CSE.")
            return []

        leads = []
        # CSE returns max 10 per request; page if needed
        start = 1
        while len(leads) < num_results:
            batch = min(10, num_results - len(leads))
            params = {
                "key": api_key,
                "cx": cse_id,
                "q": keyword,
                "num": batch,
                "start": start,
            }
            try:
                r = requests.get(self.CSE_ENDPOINT, params=params, timeout=10)
                data = r.json()

                if "error" in data:
                    print(f"   ❌ CSE Error: {data['error']['message']}")
                    break

                items = data.get("items", [])
                if not items:
                    break

                for item in items:
                    leads.append({
                        "url": item.get("link", ""),
                        "title": item.get("title", ""),
                        "description": item.get("snippet", ""),
                        "source": "google_cse",
                    })
                    print(f"   🎯 {item.get('title','')[:50]} → {item.get('link','')[:40]}")

                start += batch
                time.sleep(0.5)

                if len(items) < batch:
                    break  # No more results

            except Exception as e:
                print(f"   ❌ CSE request failed: {e}")
                break

        print(f"   ✅ CSE found {len(leads)} leads.")
        return leads

    # ── Method 2: googlesearch-python (free, may be rate-limited) ─────────
    def _search_googlesearch(self, keyword: str, num_results: int) -> List[Dict]:
        try:
            from googlesearch import search
        except ImportError:
            return []

        leads = []
        try:
            print("   🔍 Trying googlesearch-python...")
            for url in search(keyword, num_results=num_results, lang="es"):
                time.sleep(random.uniform(1.5, 3.0))
                leads.append({
                    "url": url,
                    "title": f"Company at {url.split('/')[2]}",
                    "description": "Found via web search",
                    "source": "googlesearch_python",
                })
                print(f"   🎯 {url}")
        except Exception as e:
            print(f"   ❌ googlesearch-python failed: {e}")

        return leads

    # ── Fallback: Mock data ────────────────────────────────────────────────
    def _mock_leads(self) -> List[Dict]:
        return [
            {
                "url": "https://www.ajv.cl",
                "title": "AJV - Agencia de Aduana",
                "description": "Agencia de aduana con servicios integrales de comercio exterior en Chile.",
                "source": "mock",
            },
            {
                "url": "https://www.browne.cl",
                "title": "Browne & Cía",
                "description": "Servicios de comercio exterior y desaduanamiento.",
                "source": "mock",
            },
        ]
