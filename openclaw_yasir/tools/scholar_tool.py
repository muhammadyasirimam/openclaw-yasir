"""Google Scholar Tool — Track citations and papers."""

import os
import json
from typing import List, Dict, Any
from pathlib import Path

import httpx
from bs4 import BeautifulSoup


class ScholarTool:
    """Google Scholar integration for citation tracking."""

    def __init__(self, author_id: str = None):
        self.author_id = author_id or os.getenv("SCHOLAR_AUTHOR_ID", "b80oc1UAAAAJ")
        self.base_url = "https://scholar.google.com"

    def get_author_profile(self) -> Dict[str, Any]:
        """Fetch author profile from Google Scholar."""
        try:
            url = f"{self.base_url}/citations?user={self.author_id}&hl=en"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            with httpx.Client(timeout=30) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract metrics
            metrics = {}
            for row in soup.select("#gsc_rsb_st td"):
                text = row.get_text(strip=True)
                if text.isdigit():
                    metrics["citations"] = int(text)

            # Extract publications
            publications = []
            for item in soup.select("#gsc_a_tw .gsc_a_tr"):
                title_elem = item.select_one(".gsc_a_at")
                if title_elem:
                    publications.append({
                        "title": title_elem.get_text(strip=True),
                        "link": title_elem.get("href", "")
                    })

            return {
                "author_id": self.author_id,
                "metrics": metrics,
                "publications": publications[:10]
            }

        except Exception as e:
            return {"error": str(e), "author_id": self.author_id}

    def search_papers(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search papers on Google Scholar."""
        try:
            url = f"{self.base_url}/scholar"
            params = {"q": query, "hl": "en"}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            with httpx.Client(timeout=30) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for item in soup.select(".gs_r")[:max_results]:
                title_elem = item.select_one(".gs_rt")
                author_elem = item.select_one(".gs_a")
                snippet_elem = item.select_one(".gs_rs")

                if title_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "authors": author_elem.get_text(strip=True) if author_elem else "",
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                        "link": title_elem.select_one("a")["href"] if title_elem.select_one("a") else ""
                    })

            return results

        except Exception as e:
            return [{"error": str(e)}]
