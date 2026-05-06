"""Agent Orchestrator — Manages multi-agent swarm."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel

from openclaw_yasir.personality import PersonalityEngine
from openclaw_yasir.memory import MemoryEngine

console = Console()


@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent: str
    task: str
    output: str
    metadata: Dict[str, Any]
    success: bool


class AgentOrchestrator:
    """Orchestrates specialized agents for different tasks."""

    def __init__(self):
        self.personality = PersonalityEngine()
        self.memory = MemoryEngine()
        self.agents = self._load_agents()
        self.llm_client = self._init_llm()

    def _load_agents(self) -> Dict[str, Any]:
        """Load agent configurations."""
        return {
            "researcher": {
                "name": "Dr. Yasir",
                "description": "Literature review and research synthesis",
                "tools": ["web_search", "arxiv", "scholar"]
            },
            "writer": {
                "name": "Yasir the Storyteller",
                "description": "Creative writing and content generation",
                "tools": ["web_search", "seo_tool"]
            },
            "coder": {
                "name": "Yasir the Builder",
                "description": "Code generation and technical implementation",
                "tools": ["web_search", "github_tool"]
            },
            "reviewer": {
                "name": "Yasir the Critic",
                "description": "Peer review and quality assurance",
                "tools": ["scholar"]
            },
            "seo_agent": {
                "name": "Yasir the Optimizer",
                "description": "SEO analysis and content optimization",
                "tools": ["seo_tool", "web_search"]
            }
        }

    def _init_llm(self):
        """Initialize LLM client based on configuration."""
        provider = os.getenv("DEFAULT_PROVIDER", "ollama")

        if provider == "ollama":
            try:
                import ollama
                return {"type": "ollama", "client": ollama}
            except ImportError:
                console.print("[yellow]Ollama not available, falling back to OpenAI[/yellow]")
                provider = "openai"

        if provider == "openai":
            from openai import OpenAI
            return {"type": "openai", "client": OpenAI(api_key=os.getenv("OPENAI_API_KEY"))}

        if provider == "anthropic":
            from anthropic import Anthropic
            return {"type": "anthropic", "client": Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))}

        return None

    def _call_llm(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """Call LLM with system and user prompts."""
        if self.llm_client is None:
            return "[Error: No LLM client configured. Set up Ollama or API keys.]"

        try:
            if self.llm_client["type"] == "ollama":
                response = self.llm_client["client"].chat(
                    model=os.getenv("DEFAULT_MODEL", "llama3.2"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    options={"temperature": 0.7, "num_predict": max_tokens}
                )
                return response["message"]["content"]

            elif self.llm_client["type"] == "openai":
                response = self.llm_client["client"].chat.completions.create(
                    model=os.getenv("DEFAULT_MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

            elif self.llm_client["type"] == "anthropic":
                response = self.llm_client["client"].messages.create(
                    model=os.getenv("DEFAULT_MODEL", "claude-3-haiku-20240307"),
                    max_tokens=max_tokens,
                    temperature=0.7,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text

        except Exception as e:
            console.print(f"[red]LLM Error: {e}[/red]")
            return f"[Error: {str(e)}]"

    def run_agent(
        self,
        agent_name: str,
        topic: str = None,
        prompt: str = None,
        output_file: str = None,
        **kwargs
    ) -> AgentResult:
        """Run a specific agent."""
        if agent_name not in self.agents:
            return AgentResult(
                agent=agent_name,
                task="unknown",
                output=f"Agent '{agent_name}' not found. Available: {', '.join(self.agents.keys())}",
                metadata={},
                success=False
            )

        agent_config = self.agents[agent_name]
        system_prompt = self.personality.get_agent_persona(agent_name)

        if prompt:
            user_prompt = prompt
        elif topic:
            user_prompt = f"Task: {topic}\n\nPlease provide a comprehensive response."
        else:
            user_prompt = "What would you like me to help you with today?"

        # Add context from memory
        memory_results = self.memory.query(user_prompt, top_k=3)
        if memory_results:
            context = "\n\nRelevant context from memory:\n"
            for r in memory_results:
                context += f"- {r['document'][:200]}...\n"
            user_prompt += context

        console.print(f"[cyan]Running {agent_config['name']}...[/cyan]")

        output = self._call_llm(system_prompt, user_prompt)

        # Save to memory
        self.memory.add_document(
            text=output,
            metadata={"agent": agent_name, "topic": topic or prompt[:50], "type": "output"}
        )

        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
            console.print(f"[green]Output saved to {output_file}[/green]")

        return AgentResult(
            agent=agent_name,
            task=topic or prompt,
            output=output,
            metadata={"tools_used": agent_config["tools"]},
            success=True
        )

    def run_multi_agent(
        self,
        task: str,
        agents: List[str] = None,
        output_file: str = None
    ) -> Dict[str, AgentResult]:
        """Run multiple agents in sequence (Research -> Write -> Review)."""
        if agents is None:
            agents = ["researcher", "writer", "reviewer"]

        results = {}
        accumulated_output = ""

        for agent_name in agents:
            console.print(f"\n[bold blue]Step: {agent_name.upper()}[/bold blue]")

            prompt = task
            if accumulated_output:
                prompt += f"\n\nPrevious work:\n{accumulated_output[:2000]}"

            result = self.run_agent(agent_name, prompt=prompt)
            results[agent_name] = result

            if result.success:
                accumulated_output += f"\n\n--- {agent_name.upper()} OUTPUT ---\n{result.output}"

        # Final synthesis
        console.print("\n[bold green]Synthesizing final output...[/bold green]")
        final_prompt = f"""Synthesize the following multi-agent outputs into a cohesive final deliverable.
Original task: {task}

{accumulated_output}

Provide a polished, integrated final response."""

        final_output = self._call_llm(
            self.personality.system_prompt,
            final_prompt
        )

        results["final"] = AgentResult(
            agent="synthesizer",
            task=task,
            output=final_output,
            metadata={"agents_used": agents},
            success=True
        )

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_output)
            console.print(f"[green]Final output saved to {output_file}[/green]")

        return results

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            "agents": self.agents,
            "memory_stats": self.memory.get_stats(),
            "llm_provider": self.llm_client["type"] if self.llm_client else "none"
        }
