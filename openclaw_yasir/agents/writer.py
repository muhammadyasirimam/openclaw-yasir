"""Writer Agent — Creative and technical writing."""

from typing import Dict, Any, List
from openclaw_yasir.tools import MediumTool, SEOTool


class WriterAgent:
    """Specialized agent for content creation."""

    def __init__(self):
        self.medium = MediumTool()
        self.seo = SEOTool()

    def generate_article(self, topic: str, style: str = "inspirational", target_platform: str = "medium", keywords: List[str] = None) -> Dict[str, Any]:
        """Generate an article in Yasir's voice."""
        template = self.medium.generate_article_template(topic, style)
        seo_analysis = self.seo.analyze_content(template)
        keyword_suggestions = self.seo.suggest_keywords(topic)

        return {
            "title": topic,
            "content": template,
            "style": style,
            "platform": target_platform,
            "seo_score": seo_analysis["score"],
            "word_count": seo_analysis["word_count"],
            "keyword_suggestions": keyword_suggestions,
            "seo_report": self.seo.generate_seo_report(template, topic)
        }

    def generate_book_chapter(self, title: str, theme: str = "personal growth", word_count: int = 2000) -> str:
        """Generate a book chapter in Yasir's style."""

        chapter = f"""# {title}

*Chapter from "The Colors of Life Only We Can See"*

---

## The Color Before Dawn

There was a time when I believed that success was a destination you reached by following a map someone else had drawn. I was wrong.

## The Weight of Expectations

Growing up in a mud house near the Indus River, I learned early that the world assigns you a color before you choose your own. The color of poverty. The color of a D grade. The color of "he'll never amount to much."

## The Moment of Choice

At sixteen, with a 49% in matriculation, I sat under a neem tree and made a decision. Not to prove them wrong — but to prove myself right.

## The Science of Transformation

Psychologists call this "post-traumatic growth" — the positive psychological change experienced as a result of struggle. But I call it something simpler: the refusal to let your starting point define your destination.

## The Framework I Use

Here is what I learned about transforming your trajectory:

1. **Discipline over motivation**: Motivation is a feeling. Discipline is a practice.
2. **Process over outcome**: Focus on what you control today.
3. **Community over isolation**: Find mentors who see your potential before you do.
4. **Rest over burnout**: Sustainable effort beats heroic sprints.

## The Question I Leave You With

What color have you been assigned — and what color are you choosing to become?

---

> *"The trajectory can always change. It only requires the courage to begin."*

---

*This chapter is part of "The Colors of Life Only We Can See" by Muhammad Yasir Imam, available on Amazon.* 
"""

        return chapter

    def generate_social_post(self, topic: str, platform: str = "twitter", tone: str = "inspirational") -> List[str]:
        """Generate social media posts."""

        posts = {
            "twitter": [
                f"From 49% to Gold Medalist. The trajectory can always change. What are you working on today? 🚀 #{topic.replace(' ', '')}",
                f"Discipline > Talent. Every single time. What's your non-negotiable daily practice? 💪 #{topic.replace(' ', '')}",
                f"Your starting point never defines your destination. It only defines where you begin. 🎯 #{topic.replace(' ', '')}"
            ],
            "linkedin": [
                f"""🎯 {topic}: A Reflection

After 8+ years in research and building MYI Digital, here is what I have learned about sustainable success:

It is not about being the smartest in the room. It is about being the most consistent.

From a mud house in Rajanpur to a Gold Medal in Software Engineering — the common thread was never talent. It was discipline.

What is your one non-negotiable practice?"""
            ],
            "instagram": [
                f"From mud house to gold medal 🏆 Your starting point is NOT your destination. Drop a 🔥 if you agree. #{topic.replace(' ', '')} #motivation #pakistan"
            ]
        }

        return posts.get(platform, posts["twitter"])
