"""SEO Tool — Content optimization and keyword analysis."""

import re
from typing import Dict, Any, List, Tuple
from collections import Counter

import textstat


class SEOTool:
    """SEO analysis and content optimization."""

    def __init__(self):
        self.target_keywords = [
            "AI", "Machine Learning", "Explainable AI", "XAI",
            "Research", "Pakistan", "Gold Medal", "MYI Digital",
            "Smart Grids", "Blockchain", "Personal Growth"
        ]

    def analyze_content(self, text: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Analyze content for SEO metrics."""
        keywords = target_keywords or self.target_keywords

        word_count = len(text.split())
        char_count = len(text)
        sentence_count = textstat.sentence_count(text)

        flesch_reading = textstat.flesch_reading_ease(text)
        flesch_grade = textstat.flesch_kincaid_grade(text)

        text_lower = text.lower()
        keyword_density = {}
        for kw in keywords:
            count = text_lower.count(kw.lower())
            density = (count / word_count * 100) if word_count > 0 else 0
            keyword_density[kw] = {
                "count": count,
                "density": round(density, 2)
            }

        h1_count = len(re.findall(r'^#\s', text, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s', text, re.MULTILINE))
        h3_count = len(re.findall(r'^###\s', text, re.MULTILINE))

        internal_links = len(re.findall(r'\[.*?\]\(https?://muhammadyasirimam', text))
        external_links = len(re.findall(r'\[.*?\]\(https?://(?!muhammadyasirimam)', text))

        images_without_alt = len(re.findall(r'!\[\]\(.*?\)', text))
        images_with_alt = len(re.findall(r'!\[.+?\]\(.*?\)', text))

        return {
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": sentence_count,
            "readability": {
                "flesch_reading_ease": round(flesch_reading, 1),
                "flesch_kincaid_grade": round(flesch_grade, 1),
                "difficulty": self._get_difficulty_label(flesch_reading)
            },
            "keyword_density": keyword_density,
            "structure": {
                "h1": h1_count,
                "h2": h2_count,
                "h3": h3_count,
                "total_headings": h1_count + h2_count + h3_count
            },
            "links": {
                "internal": internal_links,
                "external": external_links,
                "total": internal_links + external_links
            },
            "images": {
                "with_alt": images_with_alt,
                "without_alt": images_without_alt,
                "total": images_with_alt + images_without_alt
            },
            "score": self._calculate_seo_score(word_count, flesch_reading, keyword_density, h2_count)
        }

    def _get_difficulty_label(self, score: float) -> str:
        if score >= 90: return "Very Easy"
        elif score >= 80: return "Easy"
        elif score >= 70: return "Fairly Easy"
        elif score >= 60: return "Standard"
        elif score >= 50: return "Fairly Difficult"
        elif score >= 30: return "Difficult"
        else: return "Very Difficult"

    def _calculate_seo_score(self, word_count, readability, keyword_density, h2_count):
        score = 0
        if 800 <= word_count <= 2500: score += 25
        elif word_count >= 500: score += 15
        if 60 <= readability <= 80: score += 20
        elif readability >= 50: score += 10
        keywords_present = sum(1 for k, v in keyword_density.items() if v["count"] > 0)
        score += min(keywords_present * 3, 25)
        if h2_count >= 3: score += 20
        elif h2_count >= 1: score += 10
        good_density = sum(1 for k, v in keyword_density.items() if 0.5 <= v["density"] <= 2.0)
        score += min(good_density * 2, 10)
        return min(score, 100)

    def generate_seo_report(self, text: str, title: str = "Content") -> str:
        analysis = self.analyze_content(text)

        report = f"""# SEO Analysis Report: {title}

## 📊 Overall Score: {analysis['score']}/100

{'🟢 Excellent' if analysis['score'] >= 80 else '🟡 Good' if analysis['score'] >= 60 else '🔴 Needs Improvement'}

---

## 📝 Content Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Word Count | {analysis['word_count']} | {'✅' if 800 <= analysis['word_count'] <= 2500 else '⚠️'} |
| Sentences | {analysis['sentence_count']} | — |
| Characters | {analysis['char_count']} | — |

## 📖 Readability

| Metric | Value | Status |
|--------|-------|--------|
| Flesch Reading Ease | {analysis['readability']['flesch_reading_ease']} | {analysis['readability']['difficulty']} |
| Grade Level | {analysis['readability']['flesch_kincaid_grade']} | — |

## 🔑 Keyword Density

| Keyword | Count | Density | Status |
|---------|-------|---------|--------|
"""

        for kw, data in analysis['keyword_density'].items():
            status = "✅" if 0.5 <= data['density'] <= 2.0 else "⚠️" if data['count'] > 0 else "❌"
            report += f"| {kw} | {data['count']} | {data['density']}% | {status} |
"

        report += f"""
## 🏗️ Structure

| Element | Count | Status |
|---------|-------|--------|
| H1 | {analysis['structure']['h1']} | {'✅' if analysis['structure']['h1'] == 1 else '⚠️'} |
| H2 | {analysis['structure']['h2']} | {'✅' if analysis['structure']['h2'] >= 3 else '⚠️'} |
| H3 | {analysis['structure']['h3']} | — |

## 🔗 Links

| Type | Count |
|------|-------|
| Internal | {analysis['links']['internal']} |
| External | {analysis['links']['external']} |
| Total | {analysis['links']['total']} |

## 🖼️ Images

| Type | Count | Status |
|------|-------|--------|
| With Alt Text | {analysis['images']['with_alt']} | — |
| Without Alt Text | {analysis['images']['without_alt']} | {'⚠️' if analysis['images']['without_alt'] > 0 else '✅'} |

---

## 💡 Recommendations

"""

        recommendations = []
        if analysis['word_count'] < 800:
            recommendations.append("- **Increase word count**: Aim for at least 800 words for better SEO")
        if analysis['structure']['h2'] < 3:
            recommendations.append("- **Add more H2 headings**: Use at least 3 H2 sections for structure")
        if analysis['images']['without_alt'] > 0:
            recommendations.append("- **Add alt text to images**: All images should have descriptive alt text")
        if analysis['links']['external'] < 2:
            recommendations.append("- **Add external links**: Link to authoritative sources")
        if analysis['links']['internal'] < 2:
            recommendations.append("- **Add internal links**: Link to your other content")

        if not recommendations:
            report += "✅ **Great job!** Your content is well-optimized.
"
        else:
            report += "
".join(recommendations) + "
"

        return report

    def suggest_keywords(self, topic: str, num_suggestions: int = 10) -> List[str]:
        keyword_map = {
            "AI": ["artificial intelligence", "machine learning", "deep learning", "neural networks", "AI ethics"],
            "XAI": ["explainable AI", "interpretable ML", "model transparency", "AI accountability", "SHAP"],
            "research": ["academic research", "scientific writing", "peer review", "citation analysis", "h-index"],
            "pakistan": ["pakistani tech", "south asia AI", "emerging markets", "tech ecosystem"],
            "writing": ["content strategy", "SEO writing", "storytelling", "medium articles", "creative writing"]
        }

        suggestions = []
        topic_lower = topic.lower()

        for key, values in keyword_map.items():
            if key in topic_lower:
                suggestions.extend(values)

        suggestions.extend([
            f"{topic} guide 2026",
            f"{topic} tutorial",
            f"{topic} best practices",
            f"{topic} for beginners",
            f"{topic} advanced techniques"
        ])

        return suggestions[:num_suggestions]
