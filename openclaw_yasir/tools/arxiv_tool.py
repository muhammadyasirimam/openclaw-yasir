"""arXiv Tool — Fetch and search academic papers."""

import arxiv
from typing import List, Dict, Any
from datetime import datetime


class ArxivTool:
    """Search and fetch papers from arXiv."""

    def __init__(self):
        self.client = arxiv.Client()

    def search(
        self,
        query: str,
        max_results: int = 20,
        categories: List[str] = None,
        sort_by: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """Search arXiv papers."""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=getattr(arxiv.SortCriterion, sort_by.upper(), arxiv.SortCriterion.Relevance)
            )

            results = []
            for paper in self.client.results(search):
                results.append({
                    "title": paper.title,
                    "authors": [str(a) for a in paper.authors],
                    "summary": paper.summary,
                    "published": paper.published.isoformat(),
                    "updated": paper.updated.isoformat() if paper.updated else None,
                    "pdf_url": paper.pdf_url,
                    "entry_id": paper.entry_id,
                    "primary_category": paper.primary_category,
                    "categories": paper.categories
                })

            return results

        except Exception as e:
            return [{"error": str(e)}]

    def get_paper_by_id(self, arxiv_id: str) -> Dict[str, Any]:
        """Fetch a specific paper by arXiv ID."""
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(self.client.results(search))

            return {
                "title": paper.title,
                "authors": [str(a) for a in paper.authors],
                "summary": paper.summary,
                "published": paper.published.isoformat(),
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id,
                "primary_category": paper.primary_category
            }

        except Exception as e:
            return {"error": str(e)}

    def download_pdf(self, arxiv_id: str, output_path: str = "./data/exports") -> str:
        """Download PDF of a paper."""
        try:
            paper = next(self.client.results(arxiv.Search(id_list=[arxiv_id])))
            filename = f"{arxiv_id.replace('/', '_')}.pdf"
            paper.download_pdf(dirpath=output_path, filename=filename)
            return f"{output_path}/{filename}"
        except Exception as e:
            return f"Error: {str(e)}"
