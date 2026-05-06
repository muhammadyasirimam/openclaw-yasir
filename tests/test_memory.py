"""Tests for Memory Engine."""

import pytest
import tempfile
import shutil
from pathlib import Path

from openclaw_yasir.memory import MemoryEngine


class TestMemoryEngine:
    """Test cases for MemoryEngine."""

    def setup_method(self):
        """Set up temporary memory directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.memory = MemoryEngine(persist_directory=self.temp_dir)

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_document(self):
        """Test adding a document."""
        doc_id = self.memory.add_document(
            text="This is a test document about machine learning.",
            metadata={"topic": "ML", "source": "test"}
        )
        assert doc_id is not None

    def test_query(self):
        """Test querying memory."""
        self.memory.add_document(
            text="Machine learning is a subset of artificial intelligence.",
            metadata={"topic": "AI"}
        )

        results = self.memory.query("artificial intelligence", top_k=1)
        assert len(results) > 0
        assert "document" in results[0]

    def test_delete(self):
        """Test deleting a document."""
        doc_id = self.memory.add_document(
            text="Document to delete",
            metadata={"temp": True}
        )

        result = self.memory.delete(doc_id)
        assert result

    def test_get_stats(self):
        """Test getting memory statistics."""
        stats = self.memory.get_stats()
        assert "collection" in stats
        assert "documents" in stats
        assert "persist_directory" in stats

    def test_list_collections(self):
        """Test listing collections."""
        collections = self.memory.list_collections()
        assert isinstance(collections, list)
