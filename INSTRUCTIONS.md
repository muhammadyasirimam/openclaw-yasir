# 📘 OpenClaw-Yasir — Complete Setup & Deployment Instructions

> **For:** Muhammad Yasir Imam  
> **Project:** OpenClaw-Yasir — Personal AI Research & Creative Agent  
> **Version:** 1.0.0  
> **Date:** May 2026

---

## 🎯 What You Are Building

**OpenClaw-Yasir** is a local-first, multi-modal AI agent framework inspired by [OpenClaw](https://github.com/openclaw/openclaw). It connects AI models to your research workflows, creative writing, GitHub profile, and digital presence — all running locally on your machine.

### Key Capabilities
- 📚 **Research Assistant** — Browse arXiv, Google Scholar, ResearchGate
- ✍️ **Creative Writing** — Generate Medium articles, book chapters, SEO content
- 💻 **Code Generation** — Scaffold Python/Java/Android projects
- 🌐 **Web Presence** — Auto-update GitHub profile and portfolio
- 🧠 **Memory & Context** — Persistent vector memory (ChromaDB)
- 🤖 **Multi-Agent Swarms** — Researcher → Writer → Reviewer pipeline

---

## 📁 Project Structure Overview

```
openclaw-yasir/
├── README.md              # Main project documentation
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup
├── pyproject.toml         # Modern Python packaging
├── .gitignore             # Git ignore rules
│
├── config/                # Configuration
│   ├── .env.example       # Environment template
│   ├── settings.yaml      # Agent behavior settings
│   └── personality.json   # Your voice & style profile
│
├── openclaw_yasir/        # Main Python package
│   ├── __init__.py
│   ├── main.py            # Entry point (CLI/Web/API)
│   ├── agent.py           # Agent orchestrator
│   ├── memory.py          # Vector memory (ChromaDB)
│   ├── personality.py     # Personality engine
│   ├── tools/             # Tool integrations
│   │   ├── web_search.py
│   │   ├── arxiv_tool.py
│   │   ├── scholar_tool.py
│   │   ├── github_tool.py
│   │   ├── medium_tool.py
│   │   └── seo_tool.py
│   ├── agents/            # Specialized sub-agents
│   │   ├── researcher.py
│   │   ├── writer.py
│   │   ├── coder.py
│   │   ├── reviewer.py
│   │   └── seo_agent.py
│   ├── interfaces/        # User interfaces
│   │   ├── cli.py         # Terminal interface
│   │   ├── web_ui.py      # FastAPI web app
│   │   └── api.py         # REST API
│   └── utils/             # Utilities
│       ├── logger.py
│       └── helpers.py
│
├── data/                  # Local data storage
│   ├── memory/            # ChromaDB vector store
│   ├── cache/             # Cached API responses
│   └── exports/           # Generated outputs
│
├── pages/                 # GitHub Pages site
│   ├── index.html         # Landing page
│   └── assets/            # CSS, JS, images
│
├── tests/                 # Test suite
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_memory.py
│
├── docs/                  # Documentation
│   ├── SETUP.md           # Detailed setup guide
│   ├── AGENTS.md          # Agent customization
│   ├── API.md             # API reference
│   └── CONTRIBUTING.md    # Contribution guidelines
│
└── .github/
    └── workflows/
        └── ci.yml         # CI/CD pipeline
```

---

## 🚀 Step-by-Step Setup Instructions

### STEP 1: Create the Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. **Repository name:** `openclaw-yasir`
3. **Description:** `Personal AI Research & Creative Agent — Inspired by OpenClaw`
4. **Visibility:** Public (recommended for visibility)
5. **Initialize:** Add a README (we will replace it)
6. Click **Create repository**

---

### STEP 2: Clone the Repository Locally

```bash
# Open your terminal
cd ~/Documents  # Or your preferred projects folder

# Clone your new repo
git clone https://github.com/muhammadyasirimam/openclaw-yasir.git
cd openclaw-yasir
```

---

### STEP 3: Copy All Project Files

**Option A: Manual Copy (Recommended for understanding)**

Copy each file from the downloaded project folder into your cloned repo, maintaining the exact directory structure.

**Option B: Drag & Drop**

1. Download the project folder
2. Select ALL files and folders (except `.git`)
3. Drag into your cloned `openclaw-yasir` folder
4. Replace existing files when prompted

---

### STEP 4: Set Up Python Environment

```bash
# Check Python version (must be 3.10+)
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

---

### STEP 5: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**If you get errors with `sentence-transformers`:**
```bash
# Install PyTorch first (CPU version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Then install requirements again
pip install -r requirements.txt
```

---

### STEP 6: Configure Environment Variables

```bash
# Copy the example file
cp config/.env.example config/.env

# Edit the .env file
# macOS/Linux:
nano config/.env

# Windows:
notepad config/.env
```

**Minimum required configuration (works fully offline):**
```env
DEFAULT_MODEL=llama3.2
DEFAULT_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
GITHUB_USERNAME=muhammadyasirimam
```

**For cloud fallback (optional but recommended):**
```env
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

---

### STEP 7: Install Ollama (For Local AI)

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

**Pull a model:**
```bash
ollama pull llama3.2
```

**Verify:**
```bash
ollama list
# Should show: llama3.2
```

---

### STEP 8: Verify Installation

```bash
# Test the CLI
python -m openclaw_yasir version

# Expected output:
# OpenClaw-Yasir v1.0.0

# Test with a simple command
python -m openclaw_yasir cli

# Type: help
# You should see the command list
```

---

### STEP 9: Run the Application

**A. CLI Mode (Interactive Terminal)**
```bash
python -m openclaw_yasir cli
```

Try these commands:
```
research XAI in smart grids
write mental wealth in 2026
status
exit
```

**B. Web UI Mode**
```bash
python -m openclaw_yasir web --port 8080
```

Open browser: [http://localhost:8080](http://localhost:8080)

**C. API Mode**
```bash
python -m openclaw_yasir api --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### STEP 10: Install as a Package (Optional)

```bash
# Install in development mode
pip install -e .

# Now you can use the command anywhere:
openclaw-yasir --help
openclaw-yasir cli
openclaw-yasir web --port 8080
```

---

## 🌐 Deploy to GitHub Pages

### Method 1: GitHub Actions (Automatic)

The `.github/workflows/ci.yml` file is already configured. Just push to main:

```bash
git add .
git commit -m "Initial release: OpenClaw-Yasir v1.0.0"
git push origin main
```

GitHub Actions will automatically deploy the `pages/` folder to GitHub Pages.

**Enable GitHub Pages:**
1. Go to your repo on GitHub
2. Click **Settings** → **Pages**
3. **Source:** Deploy from a branch
4. **Branch:** `gh-pages` /root (or GitHub Actions)
5. Click **Save**

### Method 2: Manual Deployment

```bash
# From project root
git subtree push --prefix pages origin gh-pages
```

Your site will be live at:
```
https://muhammadyasirimam.github.io/openclaw-yasir
```

---

## 📊 Connect to Your Existing GitHub Profile

### Update Your Profile README

The `GitHubTool` can generate an enhanced profile README:

```bash
# In Python interactive mode
python
```

```python
from openclaw_yasir.tools.github_tool import GitHubTool

github = GitHubTool(username="muhammadyasirimam")
readme = github.generate_profile_readme()

with open("profile_readme.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("README generated! Copy contents to your GitHub profile repo.")
```

### Create a Special Profile Repository

1. Create a new repo named **exactly**: `muhammadyasirimam`
2. Initialize with README
3. Replace the README with the generated content
4. Your profile will show the enhanced README automatically

---

## 🔗 Integration with Your Portfolio Site

### Add a Link to OpenClaw-Yasir

In your existing `muhammadyasirimam.github.io` site, add:

```html
<!-- Add to your projects or tools section -->
<a href="https://github.com/muhammadyasirimam/openclaw-yasir" class="project-card">
    <h3>🦅 OpenClaw-Yasir</h3>
    <p>Your Personal AI Research & Creative Agent</p>
    <span class="tag">Python</span>
    <span class="tag">AI/ML</span>
    <span class="tag">Open Source</span>
</a>
```

### Embed the GitHub Pages Demo

```html
<iframe src="https://muhammadyasirimam.github.io/openclaw-yasir" 
        width="100%" height="600px" frameborder="0">
</iframe>
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=openclaw_yasir --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## 🔄 Daily Workflow Examples

### Morning: Research Session

```bash
# 1. Research latest XAI papers
openclaw-yasir agent researcher --topic "Explainable AI 2026" --output research/xai_2026.md

# 2. Synthesize findings
openclaw-yasir agent writer --prompt "Write a summary of research/xai_2026.md" --output drafts/xai_summary.md
```

### Afternoon: Content Creation

```bash
# 1. Generate Medium article
openclaw-yasir agent writer --topic "How AI is Changing Research in Pakistan" --style inspirational --output articles/ai_pakistan.md

# 2. Optimize for SEO
openclaw-yasir agent seo_agent --file articles/ai_pakistan.md --output articles/ai_pakistan_optimized.md

# 3. Generate social posts
openclaw-yasir agent writer --topic "AI in Pakistan" --platform twitter --output social/tweets.md
```

### Evening: Code & Review

```bash
# 1. Generate code scaffold
openclaw-yasir agent coder --task "Create a web scraper for Google Scholar" --lang python --output code/scholar_scraper.py

# 2. Review the code
openclaw-yasir agent reviewer --paper code/scholar_scraper.py --output reviews/code_review.md
```

---

## 🛠️ Troubleshooting

### Problem: `ModuleNotFoundError`
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Ollama not connecting
**Solution:**
```bash
# Start Ollama server
ollama serve

# In another terminal, test:
curl http://localhost:11434/api/tags
```

### Problem: ChromaDB errors
**Solution:**
```bash
# Clear and reinitialize
rm -rf data/memory/
python -c "from openclaw_yasir.memory import MemoryEngine; m = MemoryEngine()"
```

### Problem: GitHub API rate limit
**Solution:**
Add token to `config/.env`:
```env
GITHUB_TOKEN=ghp_your_personal_access_token
```

Generate token at: [github.com/settings/tokens](https://github.com/settings/tokens)

---

## 📚 Next Steps

1. ✅ **Read the docs:** `docs/SETUP.md`, `docs/AGENTS.md`, `docs/API.md`
2. ✅ **Customize personality:** Edit `config/personality.json`
3. ✅ **Add your papers:** Use the memory engine to store research
4. ✅ **Train on your writing:** Add Medium articles to memory
5. ✅ **Connect APIs:** Add OpenAI/Anthropic keys for cloud fallback
6. ✅ **Deploy:** Push to GitHub and enable Pages
7. ✅ **Share:** Post about it on LinkedIn, Medium, X

---

## 🎓 Pro Tips

- **Use the memory engine** to store your research papers — the agent will reference them in future responses
- **Set up cron jobs** to auto-sync your Google Scholar citations
- **Create templates** for recurring tasks (weekly research summaries, monthly reports)
- **Backup your memory** by copying `data/memory/` to cloud storage
- **Use the Web UI** for visual demos when presenting to collaborators

---

## 📞 Support

- **Issues:** [github.com/muhammadyasirimam/openclaw-yasir/issues](https://github.com/muhammadyasirimam/openclaw-yasir/issues)
- **Email:** imammuhammadyasir@gmail.com
- **Portfolio:** [muhammadyasirimam.github.io](https://muhammadyasirimam.github.io)

---

> *"From 49% to Gold Medalist — let the agent work while you dream."*  
> — Muhammad Yasir Imam

---

**🎉 Congratulations! You now have your own personal AI agent running locally.**
