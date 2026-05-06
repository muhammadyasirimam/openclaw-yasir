# API Reference

> REST API endpoints for OpenClaw-Yasir.

---

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production deployment, add API key middleware.

---

## Endpoints

### GET /api/status

Get system status and agent information.

**Response:**
```json
{
  "agents": {
    "researcher": { "name": "Dr. Yasir", "description": "...", "tools": [...] },
    "writer": { "name": "Yasir the Storyteller", "description": "...", "tools": [...] }
  },
  "memory_stats": {
    "collection": "openclaw_memory",
    "documents": 42,
    "persist_directory": "./data/memory"
  },
  "llm_provider": "ollama"
}
```

---

### POST /api/agent/{agent_name}

Run a specific agent.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_name` | string | Yes | Agent to run: `researcher`, `writer`, `coder`, `reviewer`, `seo_agent` |
| `prompt` | string | Yes | Task description or question |
| `topic` | string | No | Topic for context |

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/agent/researcher   -H "Content-Type: application/x-www-form-urlencoded"   -d "prompt=Research XAI methods for smart grids&topic=Explainable AI"
```

**Response:**
```json
{
  "agent": "researcher",
  "success": true,
  "output": "Research findings...",
  "metadata": { "tools_used": ["arxiv", "scholar"] }
}
```

---

### POST /api/research

Research a topic (shortcut for researcher agent).

**Parameters:**
| Name | Type | Required |
|------|------|----------|
| `topic` | string | Yes |

**Example:**
```bash
curl -X POST http://localhost:8000/api/research   -d "topic=Blockchain in healthcare"
```

---

### POST /api/write

Generate an article (shortcut for writer agent).

**Parameters:**
| Name | Type | Required | Default |
|------|------|----------|---------|
| `topic` | string | Yes | — |
| `style` | string | No | `inspirational` |

**Example:**
```bash
curl -X POST http://localhost:8000/api/write   -d "topic=AI ethics in Pakistan&style=technical"
```

---

### POST /api/seo

Analyze SEO of provided content.

**Parameters:**
| Name | Type | Required |
|------|------|----------|
| `content` | string | Yes |

**Example:**
```bash
curl -X POST http://localhost:8000/api/seo   -d "content=# My Article\n\nThis is content..."
```

**Response:**
```json
{
  "word_count": 150,
  "readability": {
    "flesch_reading_ease": 65.5,
    "flesch_kincaid_grade": 8.2,
    "difficulty": "Standard"
  },
  "keyword_density": {
    "AI": { "count": 5, "density": 3.33 }
  },
  "score": 75,
  "structure": { "h1": 1, "h2": 3, "h3": 2 }
}
```

---

### GET /api/search

Web search.

**Parameters:**
| Name | Type | Required | Default |
|------|------|----------|---------|
| `query` | string | Yes | — |
| `max_results` | int | No | 10 |

**Example:**
```bash
curl "http://localhost:8000/api/search?query=latest+AI+papers&max_results=5"
```

---

### GET /api/memory

Get memory statistics.

**Response:**
```json
{
  "collection": "openclaw_memory",
  "documents": 42,
  "persist_directory": "./data/memory"
}
```

---

### POST /api/memory/query

Query the memory engine.

**Parameters:**
| Name | Type | Required | Default |
|------|------|----------|---------|
| `query` | string | Yes | — |
| `top_k` | int | No | 5 |

**Example:**
```bash
curl -X POST http://localhost:8000/api/memory/query   -d "query=machine+learning+methods&top_k=3"
```

**Response:**
```json
{
  "query": "machine learning methods",
  "results": [
    {
      "id": "abc123",
      "document": "Relevant document text...",
      "metadata": { "topic": "ML", "source": "arxiv" },
      "distance": 0.234
    }
  ]
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

**Common Status Codes:**
| Code | Meaning |
|------|---------|
| 200 | Success |
| 404 | Agent not found |
| 422 | Validation error |
| 500 | Internal server error |

---

## Rate Limiting

For production deployments, implement rate limiting:

```python
from fastapi import Request
from fastapi.middleware import Middleware

# Add to create_web_app() in web_ui.py
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    # Implement your rate limiting logic
    return await call_next(request)
```

---

> *"Build systems that outlast your mood."* — Muhammad Yasir Imam
