"""Entry point for OpenClaw-Yasir."""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from openclaw_yasir.interfaces.cli import CLI
from openclaw_yasir.interfaces.web_ui import create_web_app
from openclaw_yasir.interfaces.api import create_api_app

console = Console()


def print_banner():
    """Print the OpenClaw-Yasir banner."""
    banner = Text()
    banner.append("\n", style="")
    banner.append("    🦅  ", style="bold cyan")
    banner.append("OpenClaw-Yasir", style="bold bright_cyan")
    banner.append(" v1.0.0\n", style="dim")
    banner.append("    Your Personal AI Research & Creative Agent\n", style="italic dim")
    banner.append("    Built for Muhammad Yasir Imam | ", style="dim")
    banner.append("https://github.com/muhammadyasirimam\n", style="link https://github.com/muhammadyasirimam")
    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))


def main():
    """Main entry point."""
    # Load environment variables
    env_path = Path(__file__).parent.parent / "config" / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    parser = argparse.ArgumentParser(
        prog="openclaw-yasir",
        description="Personal AI Research & Creative Agent for Muhammad Yasir Imam"
    )
    parser.add_argument(
        "mode",
        choices=["cli", "web", "api", "agent", "version"],
        default="cli",
        nargs="?",
        help="Run mode: cli, web, api, agent, or version"
    )
    parser.add_argument("--port", type=int, default=8080, help="Port for web/api mode")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host for web/api mode")
    parser.add_argument("--agent", type=str, help="Agent name for agent mode")
    parser.add_argument("--topic", type=str, help="Topic for agent mode")
    parser.add_argument("--prompt", type=str, help="Prompt for agent mode")
    parser.add_argument("--output", type=str, help="Output file for agent mode")

    args = parser.parse_args()

    if args.mode == "version":
        console.print("[bold cyan]OpenClaw-Yasir[/bold cyan] v1.0.0")
        return

    print_banner()

    if args.mode == "cli":
        cli = CLI()
        cli.run()

    elif args.mode == "web":
        console.print(f"[green]Starting Web UI on http://{args.host}:{args.port}[/green]")
        app = create_web_app()
        import uvicorn
        uvicorn.run(app, host=args.host, port=args.port)

    elif args.mode == "api":
        console.print(f"[green]Starting API on http://{args.host}:{args.port}[/green]")
        app = create_api_app()
        import uvicorn
        uvicorn.run(app, host=args.host, port=args.port)

    elif args.mode == "agent":
        from openclaw_yasir.agent import AgentOrchestrator
        orchestrator = AgentOrchestrator()

        if not args.agent:
            console.print("[red]Error: --agent is required for agent mode[/red]")
            sys.exit(1)

        result = orchestrator.run_agent(
            agent_name=args.agent,
            topic=args.topic,
            prompt=args.prompt,
            output_file=args.output
        )
        console.print(result)


if __name__ == "__main__":
    main()
