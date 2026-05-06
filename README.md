# 🦅 OpenClaw-Yasir

> **Your Personal AI Research & Creative Agent** — Inspired by [OpenClaw](https://github.com/openclaw/openclaw), built for [Muhammad Yasir Imam](https://github.com/muhammadyasirimam).

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/muhammadyasirimam/openclaw-yasir?style=social)](https://github.com/muhammadyasirimam/openclaw-yasir)

---

## 🎯 What is OpenClaw-Yasir?

**OpenClaw-Yasir** is a personal AI agent framework that mirrors the architecture of [OpenClaw](https://openclaw.ai) — a local-first, multi-modal AI assistant that runs entirely on your own devices. It connects AI models to your research workflows, creative writing, GitHub profile, and digital presence.

Unlike cloud-based assistants, **your data never leaves your machine**. The agent is always on, capable of:
- 📚 **Research Assistant** — Browse arXiv, Google Scholar, ResearchGate, and synthesize literature reviews
- ✍️ **Creative Writing** — Generate Medium articles, book chapters, and SEO content in your voice
- 💻 **Code Generation** — Scaffold Python/Java/Android projects, write tests, and review code
- 🌐 **Web Presence** — Auto-update your GitHub profile, portfolio site, and social media
- 🧠 **Memory & Context** — Persistent vector memory of your research, publications, and preferences
- 🤖 **Multi-Agent Swarms** — Delegate tasks to specialized sub-agents (Researcher, Writer, Coder, Reviewer)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw-Yasir v1.0                      │
├─────────────────────────────────────────────────────────────┤
│  🎭 Personality Layer  │  Yasir's voice, style, preferences │
├─────────────────────────────────────────────────────────────┤
│  🧠 Memory Engine      │  ChromaDB + SQLite (local, private)│
├─────────────────────────────────────────────────────────────┤
│  🤖 Agent Swarm        │  Researcher │ Writer │ Coder │ SEO  │
├─────────────────────────────────────────────────────────────┤
│  🔧 Tool Registry      │  Web Search │ arXiv │ GitHub │ Scholar│
├─────────────────────────────────────────────────────────────┤
│  🖥️  Interfaces         │  CLI │ Web UI │ API │ GitHub Pages│
├─────────────────────────────────────────────────────────────┤
│  ⚡ LLM Backend        │  Ollama (local) │ OpenAI │ Claude  │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🔍 **Semantic Research** | Hybrid BM25 + dense vector search across papers | ✅ |
| 📝 **Auto-Writing** | Generate Medium posts, book chapters, research drafts | ✅ |
| 🧬 **XAI/ML Pipeline** | Explainable AI tools for your research (SHAP, LIME) | ✅ |
| 📊 **Citation Tracker** | Auto-sync Google Scholar, ResearchGate, ORCID | ✅ |
| 🌐 **Portfolio Sync** | Auto-update `muhammadyasirimam.github.io` | ✅ |
| 🤖 **Multi-Agent Debate** | Researcher ↔ Reviewer ↔ Editor workflow | ✅ |
| 📱 **Android Bridge** | Connect to MYI News World app | 🔄 |
| 🎙️ **Voice Interface** | Speech-to-text for hands-free research | 🔄 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) (recommended for local LLMs)
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/muhammadyasirimam/openclaw-yasir.git
cd openclaw-yasir
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys (optional — works fully local)
```

### 3. Run
```bash
# CLI Mode
python -m openclaw_yasir cli

# Web UI Mode
python -m openclaw_yasir web --port 8080

# API Mode
python -m openclaw_yasir api --port 8000
```

---

## 📁 Project Structure

```
openclaw-yasir/
├── 📄 README.md                 # This file
├── 📄 LICENSE                   # MIT License
├── 📄 requirements.txt          # Python dependencies
├── 📄 setup.py                  # Package setup
├── 📄 pyproject.toml            # Modern Python packaging
│
├── 🗂️  config/                   # Configuration files
│   ├── .env.example             # Environment variables template
│   ├── settings.yaml            # Agent behavior settings
│   └── personality.json         # Yasir's voice & style profile
│
├── 🗂️  openclaw_yasir/           # Main package
│   ├── __init__.py
│   ├── main.py                  # Entry point (CLI/Web/API)
│   ├── agent.py                 # Core agent orchestrator
│   ├── memory.py                # Vector memory (ChromaDB)
│   ├── personality.py           # Personality engine
│   ├── tools/                   # Tool integrations
│   │   ├── __init__.py
│   │   ├── web_search.py        # DuckDuckGo / SerpAPI
│   │   ├── arxiv_tool.py        # arXiv paper fetcher
│   │   ├── scholar_tool.py      # Google Scholar scraper
│   │   ├── github_tool.py       # GitHub API integration
│   │   ├── medium_tool.py       # Medium draft publisher
│   │   └── seo_tool.py          # SEO analysis & keywords
│   ├── agents/                  # Specialized sub-agents
│   │   ├── __init__.py
│   │   ├── researcher.py        # Literature review agent
│   │   ├── writer.py            # Creative writing agent
│   │   ├── coder.py             # Code generation agent
│   │   ├── reviewer.py          # Peer review agent
│   │   └── seo_agent.py         # SEO optimization agent
│   ├── interfaces/              # User interfaces
│   │   ├── __init__.py
│   │   ├── cli.py               # Terminal interface
│   │   ├── web_ui.py            # Flask/FastAPI web app
│   │   └── api.py               # REST API endpoints
│   └── utils/                   # Utilities
│       ├── __init__.py
│       ├── logger.py            # Structured logging
│       └── helpers.py           # Common utilities
│
├── 🗂️  data/                     # Local data storage
│   ├── memory/                  # ChromaDB vector store
│   ├── cache/                   # Cached API responses
│   └── exports/                 # Generated outputs
│
├── 🗂️  pages/                    # GitHub Pages deployment
│   ├── index.html               # Landing page
│   ├── assets/                  # CSS, JS, images
│   └── demo/                    # Live demo snippets
│
├── 🗂️  tests/                    # Test suite
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_memory.py
│
└── 🗂️  docs/                     # Documentation
    ├── SETUP.md                 # Detailed setup guide
    ├── AGENTS.md                # Agent customization guide
    ├── API.md                   # API reference
    └── CONTRIBUTING.md          # Contribution guidelines
```

---

## 🧠 Memory & Context

OpenClaw-Yasir uses **ChromaDB** for local vector storage. Your research papers, writing samples, and preferences are embedded and stored locally — never sent to the cloud.

```python
# Example: Add your research paper to memory
from openclaw_yasir.memory import MemoryEngine

memory = MemoryEngine()
memory.add_document(
    text="Your paper content here...",
    metadata={"title": "A Product Recommendation System", "year": 2021},
    collection="research_papers"
)

# Query memory
results = memory.query("collaborative filtering approaches", top_k=5)
```

---

## 🤖 Agent Swarm

### Researcher Agent
```bash
openclaw-yasir agent researcher --topic "Explainable AI in Smart Grids" --output report.md
```

### Writer Agent
```bash
openclaw-yasir agent writer --prompt "Write a Medium article about mental wealth" --style yasir
```

### Coder Agent
```bash
openclaw-yasir agent coder --task "Create a Python script for web scraping ResearchGate" --lang python
```

### Reviewer Agent
```bash
openclaw-yasir agent reviewer --paper draft.md --criteria "clarity, novelty, methodology"
```

---

## 🌐 GitHub Pages Integration

The `pages/` directory contains a ready-to-deploy GitHub Pages site showcasing your agent:

```bash
# Deploy to GitHub Pages
git subtree push --prefix pages origin gh-pages
```

Visit: `https://muhammadyasirimam.github.io/openclaw-yasir`

---

## 📊 Profile Analytics

Track your digital footprint:
- GitHub contribution graph
- Research citation trends
- Medium article performance
- Social media engagement

```bash
openclaw-yasir analytics --profile yasir --output dashboard.html
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.10+ |
| **LLM Backend** | Ollama, OpenAI, Anthropic |
| **Vector DB** | ChromaDB |
| **Web Framework** | FastAPI + Jinja2 |
| **Frontend** | HTML5, TailwindCSS, Alpine.js |
| **Task Queue** | Celery + Redis (optional) |
| **Testing** | pytest |
| **CI/CD** | GitHub Actions |

---

## 📜 License

MIT License — see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- Inspired by [OpenClaw](https://github.com/openclaw/openclaw) by Peter Steinberger
- Built for [Muhammad Yasir Imam](https://github.com/muhammadyasirimam)
- Research powered by [arXiv](https://arxiv.org), [Google Scholar](https://scholar.google.com), [ResearchGate](https://researchgate.net)

---

> *"From 49% to Gold Medalist — let the agent work while you dream."* — Muhammad Yasir Imam
