"""Medium Tool — Draft creation and publishing."""

import os
from typing import Dict, Any
from datetime import datetime

import httpx


class MediumTool:
    """Medium integration for article publishing."""

    def __init__(self, api_key: str = None, user_id: str = None):
        self.api_key = api_key or os.getenv("MEDIUM_API_KEY")
        self.user_id = user_id or os.getenv("MEDIUM_USER_ID")
        self.base_url = "https://api.medium.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        } if self.api_key else {}

    def get_user_info(self) -> Dict[str, Any]:
        """Get Medium user information."""
        if not self.api_key:
            return {"error": "Medium API key not configured"}

        try:
            with httpx.Client(timeout=30) as client:
                response = client.get(
                    f"{self.base_url}/me",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("data", {})
        except Exception as e:
            return {"error": str(e)}

    def create_post(
        self,
        title: str,
        content: str,
        content_format: str = "markdown",
        tags: list = None,
        publish_status: str = "draft"
    ) -> Dict[str, Any]:
        """Create a new Medium post."""
        if not self.api_key or not self.user_id:
            return {"error": "Medium API key or user ID not configured"}

        try:
            payload = {
                "title": title,
                "contentFormat": content_format,
                "content": content,
                "tags": tags or ["AI", "Technology", "Research"],
                "publishStatus": publish_status
            }

            with httpx.Client(timeout=60) as client:
                response = client.post(
                    f"{self.base_url}/users/{self.user_id}/posts",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json().get("data", {})

        except Exception as e:
            return {"error": str(e)}

    def generate_article_template(
        self,
        topic: str,
        style: str = "inspirational",
        word_count: int = 800
    ) -> str:
        """Generate a Medium article template in Yasir's style."""

        templates = {
            "inspirational": f"""# {topic}

*A reflection on life, growth, and the quiet strength within us.*

---

## The Moment That Changed Everything

[Personal story hook — connect to your village origin or a pivotal moment]

## What Most People Miss

[Insight — the counterintuitive truth about the topic]

## The Science Behind It

[Research-backed explanation — cite a paper or study]

## My Personal Framework

[Actionable steps — what you actually do]

1. **Step One**: [Description]
2. **Step Two**: [Description]  
3. **Step Three**: [Description]

## The Question I Ask Myself

[Reflective closing — invite reader introspection]

---

> *"[Your catchphrase here]"*

*If this resonated with you, follow me on [Medium](https://medium.com/@muhammadyasirimam) for more stories about transformation, research, and the colors of life only we can see.*

---

*Muhammad Yasir Imam is a Research Scientist, CEO of MYI Digital, and author of "The Colors of Life Only We Can See." He writes about AI, personal growth, and the intersection of technology and humanity.*
""",

            "technical": f"""# {topic}

*A deep dive into the technology, methodology, and practical implementation.*

---

## Introduction

[Context — why this topic matters in 2026]

## Background & Related Work

[Literature review — cite 3-5 key papers]

## Methodology

[Technical approach — algorithms, architecture, data]

```python
# Code example
[Your implementation]
```

## Results & Analysis

[Performance metrics, comparisons, visualizations]

## Discussion

[Limitations, future work, implications]

## Conclusion

[Key takeaways for practitioners]

---

## References

1. [Paper citation]
2. [Paper citation]
3. [Paper citation]

---

*Muhammad Yasir Imam is a Research Assistant at ARC, Al-Hamd Islamic University, with 20+ publications in AI/ML. Connect on [Google Scholar](https://scholar.google.com/citations?user=b80oc1UAAAAJ).*
""",

            "seo": f"""# {topic}: The Complete Guide for 2026

*Everything you need to know about {topic}, backed by research and real-world experience.*

---

## What is {topic}?

[Clear definition — accessible to beginners]

## Why {topic} Matters Now

[Current relevance — trends, statistics, urgency]

## 7 Key Insights About {topic}

### 1. [Insight Title]
[Detailed explanation with examples]

### 2. [Insight Title]
[Detailed explanation with examples]

### 3. [Insight Title]
[Detailed explanation with examples]

### 4. [Insight Title]
[Detailed explanation with examples]

### 5. [Insight Title]
[Detailed explanation with examples]

### 6. [Insight Title]
[Detailed explanation with examples]

### 7. [Insight Title]
[Detailed explanation with examples]

## How to Get Started

[Actionable roadmap — tools, resources, first steps]

## Common Mistakes to Avoid

[Practical warnings from experience]

## FAQ

**Q: [Question]?**
A: [Answer]

**Q: [Question]?**
A: [Answer]

## Conclusion

[Summary + call to action]

---

*Want more insights on AI, research, and digital strategy? Follow [MYI News World](https://myinews.world) and connect with me on [LinkedIn](https://linkedin.com/in/muhammadyasirimam).*
"""
        }

        return templates.get(style, templates["inspirational"])
