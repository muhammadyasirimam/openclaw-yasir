"""Tests for tool integrations."""

import pytest
from openclaw_yasir.tools import WebSearchTool, ArxivTool, ScholarTool, GitHubTool, SEOTool


class TestWebSearchTool:
    """Test cases for WebSearchTool."""

    def setup_method(self):
        self.tool = WebSearchTool()

    def test_search(self):
        """Test web search functionality."""
        results = self.tool.search("Python programming", max_results=3)
        assert isinstance(results, list)
        if len(results) > 0 and "error" not in results[0]:
            assert "title" in results[0]
            assert "url" in results[0]


class TestArxivTool:
    """Test cases for ArxivTool."""

    def setup_method(self):
        self.tool = ArxivTool()

    def test_search(self):
        """Test arXiv search."""
        results = self.tool.search("machine learning", max_results=3)
        assert isinstance(results, list)
        if len(results) > 0 and "error" not in results[0]:
            assert "title" in results[0]
            assert "authors" in results[0]

    def test_get_paper_by_id(self):
        """Test fetching paper by ID."""
        result = self.tool.get_paper_by_id("2106.09685")
        assert isinstance(result, dict)


class TestSEOTool:
    """Test cases for SEOTool."""

    def setup_method(self):
        self.tool = SEOTool()

    def test_analyze_content(self):
        """Test SEO content analysis."""
        content = """# Test Article

## Introduction

This is a test article about AI and machine learning.

## Main Content

AI is transforming research and development.

## Conclusion

The future is bright."""

        analysis = self.tool.analyze_content(content)
        assert "word_count" in analysis
        assert "readability" in analysis
        assert "score" in analysis
        assert 0 <= analysis["score"] <= 100

    def test_suggest_keywords(self):
        """Test keyword suggestions."""
        suggestions = self.tool.suggest_keywords("AI research", num_suggestions=5)
        assert isinstance(suggestions, list)
        assert len(suggestions) <= 5


class TestGitHubTool:
    """Test cases for GitHubTool."""

    def setup_method(self):
        self.tool = GitHubTool(username="muhammadyasirimam")

    def test_get_user_profile(self):
        """Test GitHub profile fetch."""
        profile = self.tool.get_user_profile()
        assert isinstance(profile, dict)
        if "error" not in profile:
            assert "login" in profile

    def test_get_repositories(self):
        """Test repository fetch."""
        repos = self.tool.get_repositories(per_page=10)
        assert isinstance(repos, list)
