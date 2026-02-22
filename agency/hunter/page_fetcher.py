"""
Page Fetcher — visits a URL and extracts meaningful text for the LeadGrader.
"""
import requests
from bs4 import BeautifulSoup
import re

class PageFetcher:
    """Scrapes a website to extract its main content."""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch(self, url: str) -> str:
        """Fetches the URL and returns cleaned text content."""
        print(f"   🌐 Fetching: {url}...")
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove noise
            for script_or_style in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script_or_style.decompose()

            # Get text
            text = soup.get_text(separator=' ')
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit to 4000 chars to save tokens and avoid context limits
            cleaned_text = text[:4000]
            print(f"   ✅ Fetched {len(cleaned_text)} characters.")
            return cleaned_text

        except Exception as e:
            print(f"   ⚠️  Could not fetch {url}: {e}")
            return ""
