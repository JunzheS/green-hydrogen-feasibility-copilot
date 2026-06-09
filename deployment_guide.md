# Deployment Guide — Green Hydrogen Project Feasibility Copilot

**Target:** Streamlit Cloud + GitHub
**Last Updated:** 2026-06-05

---

## 1. Prerequisites

- GitHub account
- Python 3.10+ installed locally
- Git installed

---

## 2. Local Development Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/hydrogen-copilot.git
cd hydrogen-copilot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r streamlit_app/requirements.txt

# Verify engine
python -m src.main

# Run tests
python tests/test_regression.py
# Expected: "All regression tests passed. 35/35 assertions PASSED."

# Launch app
streamlit run streamlit_app/app.py
```

---

## 3. Streamlit Cloud Deployment

### 3.1 Prepare Repository

Your repository must have this structure at the root:

```
hydrogen-copilot/
├── streamlit_app/
│   ├── app.py                    # ← Streamlit entry point
│   ├── requirements.txt          # ← Dependencies
│   ├── pages/                    # ← Multi-page app
│   ├── components/
│   └── utils/
├── src/                          # ← Backend engine (imported by app)
├── knowledge_base/               # ← Data files
└── README.md
```

### 3.2 GitHub Setup

1. Push to GitHub (public or private repository)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set **Main file path** to: `streamlit_app/app.py`
6. Click "Deploy"

### 3.3 Streamlit Cloud Configuration

Create `.streamlit/config.toml` at the repository root:

```toml
[server]
headless = true
port = 8501

[theme]
primaryColor = "#1a1a2e"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#333333"
font = "sans serif"
```

### 3.4 Environment Variables (Optional)

No environment variables are required. The app reads all data from `knowledge_base/` directory.

---

## 4. Requirements Validation

### streamlit_app/requirements.txt

```
streamlit>=1.28.0
pandas>=1.5.0
```

The engine itself (`src/`) uses **only Python standard library** — no external dependencies for the core reasoning logic.

### Verification Script

```bash
# Check all imports resolve
python -c "
from src.main import FeasibilityEngine
engine = FeasibilityEngine()
report = engine.run('France','Steel','PEM',100,2029)
print('Engine OK — CAPEX:', report['capex_assessment']['total']['central_eur_m'], 'EUR M')
"
```

---

## 5. Troubleshooting

### Issue: "src module not found"

Ensure you're running Streamlit from the project root directory:

```bash
cd hydrogen-copilot
streamlit run streamlit_app/app.py
```

### Issue: Unicode errors on Windows

Set environment variable before running:

```bash
set PYTHONIOENCODING=utf-8
```

Or in PowerShell:

```powershell
$env:PYTHONIOENCODING="utf-8"
```

### Issue: Knowledge base files not found

Verify that `knowledge_base/` exists at the project root with subdirectories:

```
knowledge_base/
├── project_references/gold_dataset/   (10 GA-PR-*.json files)
├── risk_library/                       (30 RK-*.json files)
├── cost_library/                       (30 CS-*.json files)
└── technology_cards/                   (2 TC-*.json files)
```

---

## 6. Offline / Local-Only Deployment

Since the app has zero cloud dependencies:

1. Copy the entire directory to any machine with Python 3.10+
2. `pip install -r streamlit_app/requirements.txt`
3. `streamlit run streamlit_app/app.py`

No internet connection required after installation. All data is local JSON files.

---

## 7. Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r streamlit_app/requirements.txt

EXPOSE 8501

ENV PYTHONIOENCODING=utf-8

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.address=0.0.0.0"]
```

```bash
docker build -t hydrogen-copilot .
docker run -p 8501:8501 hydrogen-copilot
```

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect |
