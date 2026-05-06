"""Memory Engine — Local vector storage with ChromaDB."""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class MemoryEngine:
    """Local vector memory for persistent context."""

    def __init__(
        self,
        persist_directory: str = "./data/memory",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize ChromaDB
        self.client = chromadb.Client(
            Settings(
                persist_directory=str(self.persist_directory),
                anonymized_telemetry=False
            )
        )

        # Load embedding model
        self.embedder = SentenceTransformer(embedding_model)

        # Default collection
        self.default_collection = "openclaw_memory"

    def _get_collection(self, name: str = None):
        """Get or create a ChromaDB collection."""
        name = name or self.default_collection
        return self.client.get_or_create_collection(name=name)

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def _generate_id(self, text: str, metadata: Dict = None) -> str:
        """Generate unique ID for document."""
        content = text + str(metadata)
        return hashlib.md5(content.encode()).hexdigest()

    def add_document(
        self,
        text: str,
        metadata: Dict[str, Any] = None,
        collection: str = None,
        doc_id: str = None
    ) -> str:
        """Add a document to memory."""
        coll = self._get_collection(collection)
        metadata = metadata or {}

        # Chunk if too long
        chunks = self._chunk_text(text) if len(text) > self.chunk_size else [text]

        ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = doc_id or self._generate_id(chunk, metadata)
            if len(chunks) > 1:
                chunk_id = f"{chunk_id}_chunk_{i}"

            embedding = self.embedder.encode(chunk).tolist()

            coll.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{**metadata, "chunk_index": i, "total_chunks": len(chunks)}]
            )
            ids.append(chunk_id)

        return ids[0] if len(ids) == 1 else ids

    def query(
        self,
        query_text: str,
        collection: str = None,
        top_k: int = 5,
        filter_metadata: Dict = None
    ) -> List[Dict[str, Any]]:
        """Query memory for relevant documents."""
        coll = self._get_collection(collection)

        query_embedding = self.embedder.encode(query_text).tolist()

        results = coll.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )

        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return formatted

    def delete(self, doc_id: str, collection: str = None) -> bool:
        """Delete a document from memory."""
        coll = self._get_collection(collection)
        try:
            coll.delete(ids=[doc_id])
            return True
        except Exception:
            return False

    def list_collections(self) -> List[str]:
        """List all collections."""
        return [c.name for c in self.client.list_collections()]

    def get_stats(self, collection: str = None) -> Dict[str, Any]:
        """Get memory statistics."""
        coll = self._get_collection(collection)
        count = coll.count()
        return {
            "collection": collection or self.default_collection,
            "documents": count,
            "persist_directory": str(self.persist_directory)
        }

    def persist(self):
        """Persist memory to disk."""
        pass
