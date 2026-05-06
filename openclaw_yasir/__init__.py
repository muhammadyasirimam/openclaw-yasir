"""OpenClaw-Yasir: Personal AI Research & Creative Agent.

A local-first, multi-modal AI assistant built for Muhammad Yasir Imam.
Inspired by OpenClaw (https://github.com/openclaw/openclaw).
"""

__version__ = "1.0.0"
__author__ = "Muhammad Yasir Imam"
__email__ = "imammuhammadyasir@gmail.com"

from .agent import AgentOrchestrator
from .memory import MemoryEngine
from .personality import PersonalityEngine

__all__ = ["AgentOrchestrator", "MemoryEngine", "PersonalityEngine"]
