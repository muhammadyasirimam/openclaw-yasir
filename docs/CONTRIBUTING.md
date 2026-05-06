# Contributing to OpenClaw-Yasir

> Thank you for your interest in contributing! This project is built for Muhammad Yasir Imam's personal workflow, but contributions that improve the framework are welcome.

---

## 🤝 How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)

### Submitting Changes

1. **Fork** the repository
2. **Create a branch:** `git checkout -b feature/your-feature`
3. **Make changes** with clear commit messages
4. **Add tests** for new functionality
5. **Run tests:** `pytest tests/ -v`
6. **Submit a Pull Request**

---

## 📝 Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `style` — Formatting
- `refactor` — Code restructuring
- `test` — Tests
- `chore` — Maintenance

**Examples:**
```
feat(agent): add sentiment analysis to writer agent
fix(memory): resolve ChromaDB connection issue
docs(readme): update installation instructions
```

---

## 🧪 Testing Guidelines

- Write tests for all new features
- Maintain >80% code coverage
- Use pytest fixtures for shared resources
- Mock external API calls

---

## 🎨 Code Style

- Follow PEP 8
- Use type hints
- Document with docstrings
- Maximum line length: 100 characters

---

## 🚀 Deploying to GitHub Pages

### Method 1: GitHub Actions (Recommended)

Create `.github/workflows/pages.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./pages
```

### Method 2: Manual Deployment

```bash
# From project root
git subtree push --prefix pages origin gh-pages
```

Or:

```bash
# Create orphan branch
git checkout --orphan gh-pages
git rm -rf .
cp -r pages/* .
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
git checkout main
```

---

## 📋 Release Checklist

- [ ] Update version in `__init__.py`, `setup.py`, `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create GitHub release
- [ ] Tag version: `git tag -a v1.0.0 -m "Release v1.0.0"`

---

## 🙏 Acknowledgments

- Inspired by [OpenClaw](https://github.com/openclaw/openclaw) by Peter Steinberger
- Built for [Muhammad Yasir Imam](https://github.com/muhammadyasirimam)

---

> *"Impact over vanity. Always."* — Muhammad Yasir Imam
