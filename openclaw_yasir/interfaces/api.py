"""REST API for OpenClaw-Yasir."""

from fastapi import FastAPI
from openclaw_yasir.interfaces.web_ui import create_web_app


def create_api_app() -> FastAPI:
    """Create API-only FastAPI application."""
    app = create_web_app()

    # API documentation at /docs
    return app
