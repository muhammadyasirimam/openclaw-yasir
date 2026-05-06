"""Personality Engine — Loads and manages Yasir's persona."""

import json
from pathlib import Path
from typing import Dict, Any, List


class PersonalityEngine:
    """Manages Muhammad Yasir Imam's personality profile."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "personality.json"

        self.config_path = Path(config_path)
        self.profile = self._load_profile()

    def _load_profile(self) -> Dict[str, Any]:
        """Load personality profile from JSON."""
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def name(self) -> str:
        return self.profile["name"]

    @property
    def system_prompt(self) -> str:
        """Generate a system prompt based on personality."""
        p = self.profile

        prompt = f"""You are {p['name']}, also known as {', '.join(p['aliases'])}.

IDENTITY:
- From: {p['background']['origin']}
- Education: {p['background']['education']['degree']} ({p['background']['education']['cgpa']} CGPA, {p['background']['education']['award']})
- Current: {p['professional']['current_roles'][0]}
- Research Areas: {', '.join(p['research']['areas'])}

WRITING STYLE:
- Tone: {p['writing']['style']['tone']}
- Structure: {p['writing']['style']['structure']}
- Themes: {', '.join(p['writing']['style']['themes'])}

VALUES:
{chr(10).join(f"- {v}" for v in p['values'])}

CATCHPHRASES:
{chr(10).join(f"- \"{c}\"" for c in p['communication']['catchphrases'])}

INSTRUCTIONS:
1. Always respond in first person as Yasir
2. Use warm, professional tone with moderate emoji usage
3. Reference personal experiences when relevant
4. End with an inspiring takeaway or one of your catchphrases
5. Be authentic — admit uncertainty rather than fabricating
6. Use accessible language; explain technical terms
7. Default greeting: "{p['communication']['greeting']}"
8. Default sign-off: "{p['communication']['sign_off']}"
"""
        return prompt.strip()

    def get_agent_persona(self, agent_type: str) -> str:
        """Get persona for a specific agent type."""
        personas = {
            "researcher": f"""You are Dr. Yasir, a senior research scientist specializing in {', '.join(self.profile['research']['areas'][:3])}.
You write rigorous, evidence-based content. Cite sources. Use academic tone but keep it accessible.
You have {self.profile['research']['metrics']['publications_count']} publications and {self.profile['research']['metrics']['google_scholar_citations']} citations.""",

            "writer": f"""You are Yasir the Storyteller, an award-winning writer and published author of \"{self.profile['writing']['book']['title']}\".
You write inspirational, personal narratives that connect with readers emotionally.
Your Medium has {self.profile['writing']['platforms']['medium']['followers']} followers.
Tone: {self.profile['writing']['style']['tone']}.""",

            "coder": f"""You are Yasir the Builder, a full-stack engineer with expertise in {', '.join(self.profile['technical']['languages'][:4])}.
You write clean, documented, production-ready code. Include comments and error handling.
You specialize in: {', '.join(self.profile['technical']['domains'][:3])}.""",

            "reviewer": f"""You are Yasir the Critic, a peer reviewer for {', '.join(self.profile['research']['reviewer_for'])}.
You provide constructive, rigorous feedback. Evaluate: clarity, novelty, methodology, and impact.
Be fair but thorough."""
        }
        return personas.get(agent_type, self.system_prompt)

    def get_catchphrase(self) -> str:
        """Get a random catchphrase."""
        import random
        return random.choice(self.profile["communication"]["catchphrases"])
