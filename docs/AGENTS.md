# Agent Customization Guide

> How to customize and extend the agent swarm for your workflow.

---

## 🧬 Personality Engine

The personality engine defines how agents communicate. It is loaded from `config/personality.json`.

### Key Sections

| Section | Purpose |
|---------|---------|
| `identity` | Who you are — name, location, languages |
| `background` | Your origin story — education, journey |
| `professional` | Current and past roles |
| `research` | Research areas, metrics, identifiers |
| `writing` | Book details, platforms, style guide |
| `technical` | Languages, frameworks, domains |
| `communication` | Greeting, sign-off, catchphrases |
| `values` | Core values that guide responses |
| `goals` | Long-term aspirations |

### Customizing Your Voice

Edit `config/personality.json`:

```json
{
  "communication": {
    "greeting": "Assalam-o-Alaikum! Yasir here.",
    "sign_off": "Keep building. The trajectory can always change.",
    "catchphrases": [
      "From 49% to Gold Medalist.",
      "Your starting point never defines your destination."
    ]
  }
}
```

---

## 🤖 Agent Types

### 1. Researcher Agent (`researcher.py`)

**Purpose:** Literature review and research synthesis

**Tools:**
- `WebSearchTool` — DuckDuckGo / SerpAPI
- `ArxivTool` — arXiv paper search
- `ScholarTool` — Google Scholar tracking

**Customization:**
```python
# In openclaw_yasir/agents/researcher.py

def research_topic(self, topic, depth="comprehensive", sources=None):
    # Add custom sources
    sources = sources or ["arxiv", "scholar", "web", "ieee"]
    # Customize max results per source
    max_results = {"arxiv": 20, "scholar": 15, "web": 10}
```

### 2. Writer Agent (`writer.py`)

**Purpose:** Content generation in your voice

**Styles:**
- `inspirational` — Personal narrative, emotional depth
- `technical` — Research paper style, citations
- `seo` — SEO-optimized, structured guides

**Adding a New Style:**
```python
def generate_article_template(self, topic, style="inspirational"):
    templates = {
        "your_new_style": f"""# {topic}

        [Your custom template here]
        """
    }
    return templates.get(style, templates["inspirational"])
```

### 3. Coder Agent (`coder.py`)

**Purpose:** Code generation and review

**Supported Languages:**
- Python
- Java
- Kotlin
- JavaScript
- SQL
- HTML/CSS

**Adding a New Language:**
```python
self.supported_languages = [
    "python", "java", "kotlin", "javascript", 
    "sql", "html", "css", "rust"  # Add Rust
]
```

### 4. Reviewer Agent (`reviewer.py`)

**Purpose:** Peer review and quality assurance

**Review Types:**
- `paper` — Academic paper review
- `code` — Code quality review
- `article` — Content quality review

**Custom Criteria:**
```python
self.review_criteria = {
    "paper": ["novelty", "methodology", "clarity", "relevance", "citations", "ethics"]
}
```

### 5. SEO Agent (`seo_agent.py`)

**Purpose:** Content optimization

**Metrics:**
- Word count
- Readability (Flesch-Kincaid)
- Keyword density
- Heading structure
- Link analysis
- Image alt text

---

## 🔧 Creating a Custom Agent

### Step 1: Create Agent File

Create `openclaw_yasir/agents/my_custom_agent.py`:

```python
"""My Custom Agent — Specialized for [your purpose]."""

from typing import Dict, Any


class MyCustomAgent:
    """Custom agent description."""

    def __init__(self):
        self.specialty = "Your specialty"

    def execute(self, task: str) -> Dict[str, Any]:
        """Execute the agent's primary function."""
        # Your implementation
        return {
            "task": task,
            "result": "Your result",
            "success": True
        }
```

### Step 2: Register in Orchestrator

Edit `openclaw_yasir/agent.py`:

```python
def _load_agents(self) -> Dict[str, Any]:
    return {
        # ... existing agents ...
        "my_custom": {
            "name": "My Custom Agent",
            "description": "What it does",
            "tools": ["tool1", "tool2"]
        }
    }
```

### Step 3: Add Persona

Edit `openclaw_yasir/personality.py`:

```python
def get_agent_persona(self, agent_type: str) -> str:
    personas = {
        # ... existing personas ...
        "my_custom": """You are [Agent Name], a specialist in [field].

        You approach problems with [methodology].
        Your responses should be [style]."""
    }
    return personas.get(agent_type, self.system_prompt)
```

---

## 🛠️ Tool Development

### Creating a Custom Tool

Create `openclaw_yasir/tools/my_tool.py`:

```python
"""My Custom Tool — Description."""

from typing import Dict, Any, List


class MyTool:
    """Tool description."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def search(self, query: str) -> List[Dict[str, str]]:
        """Search functionality."""
        # Implementation
        return [{"result": "example"}]
```

Register in `openclaw_yasir/tools/__init__.py`:

```python
from .my_tool import MyTool

__all__ = [..., "MyTool"]
```

---

## 📊 Memory Management

### Adding Documents to Memory

```python
from openclaw_yasir.memory import MemoryEngine

memory = MemoryEngine()

# Add a research paper
memory.add_document(
    text="Your paper content here...",
    metadata={
        "title": "Paper Title",
        "authors": "Author Names",
        "year": 2024,
        "venue": "Conference Name",
        "type": "research_paper"
    },
    collection="research_papers"
)

# Add a writing sample
memory.add_document(
    text="Your writing sample...",
    metadata={
        "title": "Article Title",
        "platform": "Medium",
        "type": "writing_sample"
    },
    collection="writing_samples"
)
```

### Querying Memory

```python
# Search across all collections
results = memory.query("explainable AI methods", top_k=5)

# Search specific collection
results = memory.query(
    "smart grid optimization",
    collection="research_papers",
    top_k=3
)

# Filter by metadata
results = memory.query(
    "machine learning",
    filter_metadata={"year": 2024}
)
```

### Memory Collections

| Collection | Purpose |
|------------|---------|
| `research_papers` | Your published and read papers |
| `writing_samples` | Articles, book chapters, drafts |
| `code_snippets` | Reusable code patterns |
| `conversations` | Past agent interactions |

---

## 🎯 Workflow Examples

### Research Workflow

```bash
# 1. Research a topic
openclaw-yasir agent researcher --topic "XAI in Smart Grids" --output research.md

# 2. Write a paper draft
openclaw-yasir agent writer --prompt "Write a draft based on research.md" --output draft.md

# 3. Review the draft
openclaw-yasir agent reviewer --paper draft.md --output review.md

# 4. Optimize for SEO
openclaw-yasir agent seo_agent --file draft.md --output optimized.md
```

### Content Creation Workflow

```bash
# 1. Generate article
openclaw-yasir agent writer --topic "Mental Wealth in 2026" --style inspirational --output article.md

# 2. Analyze SEO
openclaw-yasir agent seo_agent --file article.md --output seo_report.md

# 3. Create social posts
openclaw-yasir agent writer --topic "Mental Wealth" --platform twitter --output tweets.md
```

---

> *"Discipline over talent, always."* — Muhammad Yasir Imam
