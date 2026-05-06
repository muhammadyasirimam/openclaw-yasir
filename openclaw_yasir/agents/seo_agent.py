"""SEO Agent — Content optimization specialist."""

from typing import Dict, Any, List
from openclaw_yasir.tools import SEOTool, WebSearchTool


class SEOAgent:
    """Specialized agent for SEO optimization."""

    def __init__(self):
        self.seo = SEOTool()
        self.web = WebSearchTool()

    def optimize_article(self, content: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Optimize an article for SEO."""

        # Analyze current state
        analysis = self.seo.analyze_content(content, target_keywords)

        # Generate improvements
        improvements = []

        if analysis["word_count"] < 800:
            improvements.append("Expand content to at least 800 words")

        if analysis["structure"]["h2"] < 3:
            improvements.append("Add more H2 subheadings for structure")

        if analysis["links"]["external"] < 2:
            improvements.append("Add 2-3 external links to authoritative sources")

        if analysis["links"]["internal"] < 2:
            improvements.append("Add internal links to related content")

        # Keyword suggestions
        keyword_suggestions = []
        for kw, data in analysis["keyword_density"].items():
            if data["count"] == 0:
                keyword_suggestions.append(f"Include '{kw}' at least once")
            elif data["density"] > 3.0:
                keyword_suggestions.append(f"Reduce '{kw}' usage (currently {data['density']}%)")

        return {
            "original_score": analysis["score"],
            "improvements": improvements,
            "keyword_suggestions": keyword_suggestions,
            "analysis": analysis,
            "optimized_content": self._apply_optimizations(content, improvements)
        }

    def _apply_optimizations(self, content: str, improvements: List[str]) -> str:
        """Apply basic SEO optimizations to content."""
        optimized = content

        # Add table of contents if missing and content is long
        if len(content.split()) > 1000 and "## Table of Contents" not in content:
            toc = "## Table of Contents

"
            # Extract H2 headings
            import re
            h2s = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
            for i, h2 in enumerate(h2s, 1):
                anchor = h2.lower().replace(' ', '-').replace(',', '')[:30]
                toc += f"{i}. [{h2}](#{anchor})
"
            toc += "
---

"

            # Insert after first H1
            h1_end = content.find("\n", content.find("# "))
            if h1_end > 0:
                optimized = content[:h1_end+1] + "\n" + toc + content[h1_end+1:]

        return optimized

    def competitor_analysis(self, topic: str, competitors: List[str] = None) -> Dict[str, Any]:
        """Analyze competitor content for a topic."""

        search_results = self.web.search(f"{topic} best practices 2026", max_results=10)

        analysis = {
            "topic": topic,
            "competitors_analyzed": len(search_results),
            "common_themes": [],
            "content_gaps": [],
            "recommendations": []
        }

        # Extract common themes from search results
        all_text = " ".join([r.get("snippet", "") for r in search_results])
        common_words = ["AI", "machine learning", "research", "best practices", "guide"]

        analysis["common_themes"] = [w for w in common_words if w.lower() in all_text.lower()]

        analysis["content_gaps"] = [
            "Personal narrative angle — most content is purely technical",
            "Pakistani perspective — underrepresented in global discourse",
            "Practical implementation examples — many articles lack code"
        ]

        analysis["recommendations"] = [
            f"Write {len(analysis['common_themes'])} sections covering: {', '.join(analysis['common_themes'])}",
            "Include personal anecdotes to differentiate from competitors",
            "Add downloadable code samples and templates",
            "Target long-tail keywords: specific subtopics within the domain"
        ]

        return analysis

    def generate_meta_description(self, content: str, max_length: int = 160) -> str:
        """Generate an SEO-optimized meta description."""

        # Extract first paragraph
        paragraphs = content.split("\n\n")
        first_para = paragraphs[0] if paragraphs else content

        # Clean and truncate
        clean = first_para.replace("#", "").replace("*", "").strip()

        if len(clean) > max_length:
            clean = clean[:max_length-3] + "..."

        return clean
