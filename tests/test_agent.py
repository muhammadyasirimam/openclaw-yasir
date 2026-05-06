"""Tests for Agent Orchestrator."""

import pytest
from openclaw_yasir.agent import AgentOrchestrator, AgentResult


class TestAgentOrchestrator:
    """Test cases for AgentOrchestrator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.orchestrator = AgentOrchestrator()

    def test_agent_loading(self):
        """Test that all agents are loaded."""
        expected_agents = ["researcher", "writer", "coder", "reviewer", "seo_agent"]
        for agent in expected_agents:
            assert agent in self.orchestrator.agents

    def test_invalid_agent(self):
        """Test running an invalid agent."""
        result = self.orchestrator.run_agent("nonexistent")
        assert not result.success
        assert "not found" in result.output

    def test_researcher_agent(self):
        """Test researcher agent execution."""
        result = self.orchestrator.run_agent("researcher", topic="test topic")
        assert result.agent == "researcher"
        assert result.success

    def test_writer_agent(self):
        """Test writer agent execution."""
        result = self.orchestrator.run_agent("writer", topic="test article")
        assert result.agent == "writer"
        assert result.success

    def test_multi_agent_workflow(self):
        """Test multi-agent workflow."""
        results = self.orchestrator.run_multi_agent(
            task="test task",
            agents=["researcher", "writer"]
        )
        assert "researcher" in results
        assert "writer" in results
        assert "final" in results

    def test_agent_status(self):
        """Test getting agent status."""
        status = self.orchestrator.get_agent_status()
        assert "agents" in status
        assert "memory_stats" in status
        assert "llm_provider" in status
