"""Command Line Interface for OpenClaw-Yasir."""

import os
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

from openclaw_yasir.agent import AgentOrchestrator
from openclaw_yasir.memory import MemoryEngine
from openclaw_yasir.personality import PersonalityEngine

console = Console()


class CLI:
    """Interactive command-line interface."""

    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.memory = MemoryEngine()
        self.personality = PersonalityEngine()
        self.running = True

    def run(self):
        """Run the interactive CLI."""
        console.print(f"\n[bold cyan]{self.personality.name}[/bold cyan] is ready to assist you.")
        console.print("[dim]Type 'help' for commands, 'exit' to quit.[/dim]\n")

        while self.running:
            try:
                user_input = Prompt.ask("[bold green]You[/bold green]")

                if not user_input.strip():
                    continue

                self._process_command(user_input)

            except KeyboardInterrupt:
                console.print("\n[dim]Use 'exit' to quit properly.[/dim]")
            except EOFError:
                break

        console.print(f"\n[bold cyan]{self.personality.get_catchphrase()}[/bold cyan] 👋")

    def _process_command(self, command: str):
        """Process user command."""
        cmd = command.strip().lower()

        if cmd in ["exit", "quit", "q"]:
            self.running = False

        elif cmd == "help":
            self._show_help()

        elif cmd == "status":
            self._show_status()

        elif cmd == "memory":
            self._show_memory()

        elif cmd.startswith("research "):
            topic = command[9:]
            self._run_research(topic)

        elif cmd.startswith("write "):
            topic = command[6:]
            self._run_writer(topic)

        elif cmd.startswith("code "):
            task = command[5:]
            self._run_coder(task)

        elif cmd.startswith("review "):
            file_path = command[7:]
            self._run_reviewer(file_path)

        elif cmd.startswith("seo "):
            file_path = command[4:]
            self._run_seo(file_path)

        elif cmd.startswith("search "):
            query = command[7:]
            self._run_search(query)

        elif cmd.startswith("ask "):
            question = command[4:]
            self._run_general(question)

        else:
            # Treat as general question
            self._run_general(command)

    def _show_help(self):
        """Display help information."""
        table = Table(title="OpenClaw-Yasir Commands", show_header=True, header_style="bold cyan")
        table.add_column("Command", style="bold green")
        table.add_column("Description")
        table.add_column("Example")

        commands = [
            ("research <topic>", "Research a topic across sources", "research XAI in smart grids"),
            ("write <topic>", "Generate an article", "write mental wealth in 2026"),
            ("code <task>", "Generate code", "code web scraper for ResearchGate"),
            ("review <file>", "Review a paper or code", "review draft.md"),
            ("seo <file>", "Analyze SEO of content", "seo article.md"),
            ("search <query>", "Web search", "search latest XAI papers"),
            ("ask <question>", "General question", "ask what is SHAP?"),
            ("status", "Show system status", "status"),
            ("memory", "Show memory stats", "memory"),
            ("help", "Show this help", "help"),
            ("exit", "Quit the application", "exit"),
        ]

        for cmd, desc, example in commands:
            table.add_row(cmd, desc, example)

        console.print(table)

    def _show_status(self):
        """Show system status."""
        status = self.orchestrator.get_agent_status()

        table = Table(title="System Status", show_header=True)
        table.add_column("Component", style="bold")
        table.add_column("Status")

        table.add_row("LLM Provider", status["llm_provider"])
        table.add_row("Memory Documents", str(status["memory_stats"]["documents"]))
        table.add_row("Available Agents", ", ".join(status["agents"].keys()))

        console.print(table)

    def _show_memory(self):
        """Show memory statistics."""
        stats = self.memory.get_stats()
        console.print(Panel(
            f"[bold]Collection:[/bold] {stats['collection']}\n"
            f"[bold]Documents:[/bold] {stats['documents']}\n"
            f"[bold]Directory:[/bold] {stats['persist_directory']}",
            title="Memory Status",
            border_style="blue"
        ))

    def _run_research(self, topic: str):
        """Run researcher agent."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Researching: {topic}...", total=None)
            result = self.orchestrator.run_agent("researcher", topic=topic)

        console.print(Panel(result.output, title=f"🔬 Research: {topic}", border_style="blue"))

    def _run_writer(self, topic: str):
        """Run writer agent."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Writing about: {topic}...", total=None)
            result = self.orchestrator.run_agent("writer", topic=topic)

        console.print(Panel(result.output, title=f"✍️  Writing: {topic}", border_style="green"))

        if Confirm.ask("Save to file?"):
            filename = f"{topic.replace(' ', '_').lower()}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result.output)
            console.print(f"[green]Saved to {filename}[/green]")

    def _run_coder(self, task: str):
        """Run coder agent."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            progress_task = progress.add_task(f"Coding: {task}...", total=None)
            result = self.orchestrator.run_agent("coder", topic=task)

        console.print(Panel(result.output, title=f"💻 Code: {task}", border_style="magenta"))

    def _run_reviewer(self, file_path: str):
        """Run reviewer agent."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("Reviewing...", total=None)
                result = self.orchestrator.run_agent("reviewer", prompt=f"Review this document:\n\n{content[:3000]}")

            console.print(Panel(result.output, title="🔍 Review Report", border_style="yellow"))

        except FileNotFoundError:
            console.print(f"[red]File not found: {file_path}[/red]")

    def _run_seo(self, file_path: str):
        """Run SEO analysis."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            from openclaw_yasir.tools import SEOTool
            seo = SEOTool()
            report = seo.generate_seo_report(content, file_path)

            console.print(Panel(report, title="📊 SEO Analysis", border_style="cyan"))

        except FileNotFoundError:
            console.print(f"[red]File not found: {file_path}[/red]")

    def _run_search(self, query: str):
        """Run web search."""
        from openclaw_yasir.tools import WebSearchTool

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Searching: {query}...", total=None)
            search = WebSearchTool()
            results = search.search(query)

        table = Table(title=f"Search Results: {query}", show_header=True)
        table.add_column("#", style="bold", width=3)
        table.add_column("Title", style="bold cyan")
        table.add_column("URL", style="dim")

        for i, result in enumerate(results[:5], 1):
            table.add_row(str(i), result.get("title", "N/A")[:50], result.get("url", "")[:40])

        console.print(table)

    def _run_general(self, question: str):
        """Run general query."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Thinking...", total=None)
            result = self.orchestrator.run_agent("researcher", prompt=question)

        console.print(Panel(result.output, title="🤖 OpenClaw-Yasir", border_style="cyan"))
