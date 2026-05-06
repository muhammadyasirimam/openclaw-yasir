"""Web UI for OpenClaw-Yasir using FastAPI + Jinja2."""

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from openclaw_yasir.agent import AgentOrchestrator
from openclaw_yasir.memory import MemoryEngine
from openclaw_yasir.personality import PersonalityEngine
from openclaw_yasir.tools import WebSearchTool, SEOTool

# Template directory
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "pages"


def create_web_app() -> FastAPI:
    """Create and configure the FastAPI web application."""

    app = FastAPI(
        title="OpenClaw-Yasir",
        description="Your Personal AI Research & Creative Agent",
        version="1.0.0"
    )

    # Initialize components
    orchestrator = AgentOrchestrator()
    memory = MemoryEngine()
    personality = PersonalityEngine()

    # Mount static files
    static_dir = TEMPLATE_DIR / "assets"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Main dashboard."""
        return templates.TemplateResponse("index.html", {
            "request": request,
            "name": personality.name,
            "catchphrase": personality.get_catchphrase()
        })

    @app.get("/api/status")
    async def status():
        """Get system status."""
        return orchestrator.get_agent_status()

    @app.post("/api/agent/{agent_name}")
    async def run_agent(agent_name: str, prompt: str = Form(...), topic: Optional[str] = Form(None)):
        """Run a specific agent."""
        if agent_name not in orchestrator.agents:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

        result = orchestrator.run_agent(agent_name, topic=topic, prompt=prompt)
        return JSONResponse({
            "agent": result.agent,
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata
        })

    @app.post("/api/research")
    async def research(topic: str = Form(...)):
        """Research a topic."""
        result = orchestrator.run_agent("researcher", topic=topic)
        return {"topic": topic, "result": result.output}

    @app.post("/api/write")
    async def write(topic: str = Form(...), style: str = Form("inspirational")):
        """Generate an article."""
        result = orchestrator.run_agent("writer", topic=topic)
        return {"topic": topic, "style": style, "result": result.output}

    @app.post("/api/seo")
    async def analyze_seo(content: str = Form(...)):
        """Analyze SEO of content."""
        seo = SEOTool()
        analysis = seo.analyze_content(content)
        return analysis

    @app.get("/api/search")
    async def search(query: str, max_results: int = 10):
        """Web search."""
        search_tool = WebSearchTool()
        results = search_tool.search(query, max_results)
        return {"query": query, "results": results}

    @app.get("/api/memory")
    async def get_memory_stats():
        """Get memory statistics."""
        return memory.get_stats()

    @app.post("/api/memory/query")
    async def query_memory(query: str = Form(...), top_k: int = 5):
        """Query memory."""
        results = memory.query(query, top_k=top_k)
        return {"query": query, "results": results}

    return app
