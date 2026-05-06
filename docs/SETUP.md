# Setup Guide — OpenClaw-Yasir

> Complete step-by-step guide to set up your personal AI agent.

---

## 📋 Prerequisites

Before you begin, ensure you have:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.10+ | `python --version` |
| Git | Latest | `git --version` |
| pip | Latest | `pip --version` |

### Optional (Recommended)
- **Ollama** — For local LLM inference ([ollama.com](https://ollama.com))
- **GitHub Token** — For profile analytics ([github.com/settings/tokens](https://github.com/settings/tokens))
- **OpenAI API Key** — For GPT-4o fallback ([platform.openai.com](https://platform.openai.com))

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/muhammadyasirimam/openclaw-yasir.git
cd openclaw-yasir
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you encounter issues with `sentence-transformers`, install PyTorch first:
> ```bash
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
> pip install -r requirements.txt
> ```

---

## ⚙️ Configuration

### Step 4: Environment Variables

```bash
cp config/.env.example config/.env
```

Edit `config/.env` with your values:

```env
# LLM Providers (at least one required)
OPENAI_API_KEY=sk-your-openai-key-here          # Optional — for cloud fallback
ANTHROPIC_API_KEY=sk-ant-your-key-here          # Optional — for Claude fallback
OLLAMA_HOST=http://localhost:11434              # Default — local LLM

# Default LLM Model
DEFAULT_MODEL=llama3.2
DEFAULT_PROVIDER=ollama

# Research APIs
SERPAPI_KEY=your-serpapi-key                    # Optional — for premium search

# GitHub
GITHUB_TOKEN=ghp_your_github_token              # Optional — for profile sync
GITHUB_USERNAME=muhammadyasirimam

# Medium (for auto-publishing)
MEDIUM_API_KEY=your-medium-integration-token    # Optional
MEDIUM_USER_ID=your-medium-user-id              # Optional

# Memory & Storage
CHROMA_DB_PATH=./data/memory
CACHE_DIR=./data/cache
EXPORTS_DIR=./data/exports

# Agent Behavior
MAX_ITERATIONS=10
TEMPERATURE=0.7
MAX_TOKENS=4096

# Web UI
WEB_PORT=8080
API_PORT=8000
DEBUG=false
```

### Step 5: Verify Setup

```bash
python -m openclaw_yasir version
```

Expected output:
```
OpenClaw-Yasir v1.0.0
```

---

## 🖥️ Running the Application

### CLI Mode (Interactive Terminal)

```bash
python -m openclaw_yasir cli
```

**Available commands:**
- `research <topic>` — Research a topic
- `write <topic>` — Generate an article
- `code <task>` — Generate code
- `review <file>` — Review a document
- `seo <file>` — Analyze SEO
- `search <query>` — Web search
- `ask <question>` — General question
- `status` — System status
- `memory` — Memory statistics
- `help` — Show help
- `exit` — Quit

### Web UI Mode

```bash
python -m openclaw_yasir web --port 8080
```

Open browser: [http://localhost:8080](http://localhost:8080)

### API Mode

```bash
python -m openclaw_yasir api --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🤖 Setting Up Ollama (Local LLM)

### Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com/download](https://ollama.com/download)

### Pull a Model

```bash
ollama pull llama3.2
```

Other recommended models:
```bash
ollama pull mistral
ollama pull codellama
ollama pull llama3
```

### Verify Ollama is Running

```bash
ollama list
```

You should see your pulled models. The agent will automatically connect to `http://localhost:11434`.

---

## 📦 Installing as a Package

```bash
pip install -e .
```

Now you can use the command anywhere:
```bash
openclaw-yasir --help
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=openclaw_yasir --cov-report=html
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'chromadb'`
**Fix:**
```bash
pip install chromadb
```

### Issue: `Ollama connection refused`
**Fix:** Ensure Ollama is running:
```bash
ollama serve
```

### Issue: `sentence-transformers` download fails
**Fix:** Set HuggingFace cache directory:
```bash
export HF_HOME="~/.cache/huggingface"
```

### Issue: GitHub API rate limit
**Fix:** Add your GitHub token to `config/.env`:
```env
GITHUB_TOKEN=ghp_your_token_here
```

---

## 🎓 Next Steps

1. **Read the API docs:** [docs/API.md](API.md)
2. **Customize agents:** [docs/AGENTS.md](AGENTS.md)
3. **Deploy to GitHub Pages:** See [docs/CONTRIBUTING.md](CONTRIBUTING.md)
4. **Add your research papers** to the memory engine
5. **Configure your writing style** in `config/personality.json`

---

> *"The trajectory can always change. It only requires the courage to begin."* — Muhammad Yasir Imam
