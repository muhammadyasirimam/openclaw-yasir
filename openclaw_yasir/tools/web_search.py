"""Web Search Tool — DuckDuckGo and SerpAPI integration."""

import os
import json
from typing import List, Dict, Any
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup


class WebSearchTool:
    """Web search using DuckDuckGo (free) or SerpAPI (premium)."""

    def __init__(self, engine: str = "duckduckgo"):
        self.engine = engine
        self.serpapi_key = os.getenv("SERPAPI_KEY")

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Perform web search."""
        if self.engine == "serpapi" and self.serpapi_key:
            return self._search_serpapi(query, max_results)
        return self._search_duckduckgo(query, max_results)

    def _search_duckduckgo(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search using DuckDuckGo HTML."""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            with httpx.Client(timeout=30) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for result in soup.select(".result")[:max_results]:
                title_elem = result.select_one(".result__title")
                snippet_elem = result.select_one(".result__snippet")
                url_elem = result.select_one(".result__url")

                if title_elem and url_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": url_elem.get_text(strip=True),
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else ""
                    })

            return results

        except Exception as e:
            return [{"error": str(e), "title": "Search failed", "url": "", "snippet": ""}]

    def _search_serpapi(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search using SerpAPI."""
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "engine": "google",
                "num": max_results
            }

            with httpx.Client(timeout=30) as client:
                response = client.get(url, params=params)
                response.raise_for_status()

            data = response.json()
            results = []

            for result in data.get("organic_results", [])[:max_results]:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })

            return results

        except Exception as e:
            return [{"error": str(e), "title": "Search failed", "url": "", "snippet": ""}]
