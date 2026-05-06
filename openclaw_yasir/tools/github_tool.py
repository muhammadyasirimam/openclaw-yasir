"""GitHub Tool — Profile analysis and repo management."""

import os
from typing import Dict, Any, List
from datetime import datetime

import httpx


class GitHubTool:
    """GitHub API integration for profile analytics."""

    def __init__(self, token: str = None, username: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.username = username or os.getenv("GITHUB_USERNAME", "muhammadyasirimam")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "OpenClaw-Yasir/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def get_user_profile(self) -> Dict[str, Any]:
        """Fetch user profile information."""
        try:
            with httpx.Client(timeout=30) as client:
                response = client.get(
                    f"{self.base_url}/users/{self.username}",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "login": data["login"],
                    "name": data.get("name", ""),
                    "bio": data.get("bio", ""),
                    "location": data.get("location", ""),
                    "company": data.get("company", ""),
                    "blog": data.get("blog", ""),
                    "public_repos": data["public_repos"],
                    "public_gists": data["public_gists"],
                    "followers": data["followers"],
                    "following": data["following"],
                    "created_at": data["created_at"],
                    "avatar_url": data["avatar_url"],
                    "html_url": data["html_url"]
                }

        except Exception as e:
            return {"error": str(e), "username": self.username}

    def get_repositories(self, per_page: int = 100) -> List[Dict[str, Any]]:
        """Fetch user's repositories."""
        try:
            repos = []
            page = 1

            while True:
                with httpx.Client(timeout=30) as client:
                    response = client.get(
                        f"{self.base_url}/users/{self.username}/repos",
                        headers=self.headers,
                        params={"per_page": per_page, "page": page, "sort": "updated"}
                    )
                    response.raise_for_status()
                    data = response.json()

                    if not data:
                        break

                    for repo in data:
                        repos.append({
                            "name": repo["name"],
                            "description": repo.get("description", ""),
                            "language": repo.get("language", ""),
                            "stars": repo["stargazers_count"],
                            "forks": repo["forks_count"],
                            "open_issues": repo["open_issues_count"],
                            "created_at": repo["created_at"],
                            "updated_at": repo["updated_at"],
                            "html_url": repo["html_url"],
                            "clone_url": repo["clone_url"],
                            "topics": repo.get("topics", []),
                            "is_fork": repo["fork"],
                            "size_kb": repo["size"]
                        })

                    page += 1
                    if len(data) < per_page:
                        break

            return repos

        except Exception as e:
            return [{"error": str(e)}]

    def get_contribution_stats(self) -> Dict[str, Any]:
        """Analyze contribution patterns."""
        repos = self.get_repositories()

        if repos and "error" in repos[0]:
            return repos[0]

        languages = {}
        total_stars = 0
        total_forks = 0

        for repo in repos:
            lang = repo.get("language") or "Unknown"
            languages[lang] = languages.get(lang, 0) + 1
            total_stars += repo["stars"]
            total_forks += repo["forks"]

        return {
            "total_repos": len(repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "languages": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)),
            "top_repos": sorted(repos, key=lambda x: x["stars"], reverse=True)[:5]
        }

    def generate_profile_readme(self) -> str:
        """Generate an enhanced GitHub profile README."""
        profile = self.get_user_profile()
        stats = self.get_contribution_stats()

        readme = f"""# 👋 Hi, I'm {profile.get('name', 'Muhammad Yasir Imam')}

> {profile.get('bio', 'Research Scientist | CEO | Published Author | Gold Medalist')}

[![GitHub followers](https://img.shields.io/github/followers/{self.username}?style=social)](https://github.com/{self.username}?tab=followers)
[![GitHub stars](https://img.shields.io/github/stars/{self.username}?style=social)](https://github.com/{self.username}?tab=repositories)

---

## 🧬 About Me

- 🔬 Research Assistant @ ARC, Al-Hamd Islamic University
- 🚀 CEO & Founder @ [MYI Digital](https://myinews.world)
- 📚 Published Author — *"The Colors of Life Only We Can See"*
- 🎓 BS Software Engineering — **4.0 CGPA Gold Medal**
- 🏆 Award-Winning Researcher | 19 Citations | 20+ Publications

---

## 📊 GitHub Stats

| Metric | Count |
|--------|-------|
| 📦 Public Repos | {stats.get('total_repos', 0)} |
| ⭐ Total Stars | {stats.get('total_stars', 0)} |
| 🍴 Total Forks | {stats.get('total_forks', 0)} |
| 👥 Followers | {profile.get('followers', 0)} |

---

## 🔝 Top Repositories

"""

        for repo in stats.get("top_repos", [])[:5]:
            readme += f"""### [{repo['name']}]({repo['html_url']})
> {repo.get('description', 'No description')}
- ⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks | 📝 {repo['language'] or 'N/A'}

"""

        readme += f"""---

## 🛠️ Tech Stack

{chr(10).join(f"- **{lang}**: {count} repos" for lang, count in list(stats.get('languages', {}).items())[:8])}

---

## 🌐 Connect With Me

- 🔗 [Portfolio](https://muhammadyasirimam.github.io)
- 📧 imammuhammadyasir@gmail.com
- 🐦 [X/Twitter](https://x.com/muhammadyasirim)
- 💼 [LinkedIn](https://linkedin.com/in/muhammadyasirimam)
- 📝 [Medium](https://medium.com/@muhammadyasirimam)
- 📚 [Google Scholar](https://scholar.google.com/citations?user=b80oc1UAAAAJ)

---

> *"From 49% to Gold Medalist — the trajectory can always change."*

_© {datetime.now().year} Muhammad Yasir Imam_
"""

        return readme
