# Category Promotion Analysis

A full-stack promo analytics app: **Upload a CSV → validate schema → compute category/SKU promotion uplift → save runs → export results**.

> Repo goal: clean, reproducible analytics workflow with a production-style API and test coverage.

---

## Table of Contents
- [What it does](#-what-it-does)
- [Tech Stack](#-tech-stack)
- [Current Features](#-current-features-backend)
- [Repository Structure](#-repository-structure)
- [CSV Data Contract](#-csv-data-contract-v0)
- [Quickstart (Backend)](#-quickstart-backend)
- [Run Tests](#-run-tests)
- [API Reference](#-api-reference)
- [Metrics](#-metrics-current)
- [Roadmap](#-roadmap)
- [Notes on Persistence](#-notes-on-persistence)
- [License](#-license)
- [Author](#-author)

---

## ✨ What it does

- Creates **analysis runs** (tracked in SQLite)
- Accepts **CSV uploads** and validates required fields
- Computes **promotion uplift metrics** (baseline vs promo rows)
- Persists analysis **results** and exposes them via API endpoints
- Includes **automated tests** (pytest) for the full run → upload → analyze workflow

---

## 🧱 Tech Stack

**Backend**
- FastAPI (REST API)
- Pandas (data parsing + metrics)
- SQLAlchemy + SQLite (run tracking + results)
- Pytest (tests)
- Ruff (linting)

**Frontend**
- Planned: React + TypeScript + Vite (GitHub Pages)
- Status: Coming next

---

## ✅ Current Features (Backend)

### Runs
- Create a run
- List recent runs
- Fetch a run by ID

### CSV Ingestion
- Upload CSV for a run (`multipart/form-data`)
- Validates schema and rejects invalid files

### Analysis + Results
- Analyze uploaded data and persist results
- Fetch stored results later

### Reliability
- Request logging middleware
- Environment-configurable CORS
- Test suite validates routes and core workflows

---

## 📁 Repository Structure

```text
Category-Promotion-Analysis/
  backend/
    app/
      api/            # API routes
      core/           # config + logging
      db/             # SQLAlchemy session/models
      schemas/        # Pydantic response models
      services/       # ingest + analyze logic
      tests/          # pytest tests
    pyproject.toml
  sample_data/
    sample_promos.csv
  README.md
  LICENSE
  .gitignore
```

---

## 📊 CSV Data Contract (v0)

### Required columns
- `date` (date/datetime)
- `category` (string)
- `units` (number)
- `revenue` (number)

### Promo indicator (at least one required)
- `promo_id` **OR**
- `is_promo` (0/1)

### Optional (supported for future enhancements)
- `sku`
- `discount_pct`

Sample file:
- `sample_data/sample_promos.csv`

---

## 🚀 Quickstart (Backend)

### 1) Create/activate conda env (recommended)

```bash
conda create -n promo-analytics python=3.11 -y
conda activate promo-analytics
```

### 2) Install backend + dev tools

From the repo root:

```bash
cd backend
pip install -e ".[dev]"
```

If you prefer not to `conda activate`, you can run:

```bash
cd backend
conda run -n promo-analytics python -m pip install -e ".[dev]"
```

### 3) Run the API

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Open:
- Health: http://127.0.0.1:8000/health
- API docs (Swagger): http://127.0.0.1:8000/docs

---

## ✅ Run Tests

From the repo root:

```bash
cd backend
pytest
```

Or with conda run:

```bash
cd backend
conda run -n promo-analytics python -m pytest
```

---

## 🔌 API Reference

Base URL (local): http://127.0.0.1:8000

### Health
- `GET /health` → `{ "status": "ok" }`

### Runs
- `POST /runs` → create a run
- `GET /runs` → list recent runs
- `GET /runs/{run_id}` → get run metadata

### Upload CSV
- `POST /runs/{run_id}/upload` (multipart/form-data)

Create a run:
```bash
curl -X POST "http://127.0.0.1:8000/runs"
```

Upload CSV:
```bash
curl -X POST "http://127.0.0.1:8000/runs/<RUN_ID>/upload" \
  -F "file=@sample_data/sample_promos.csv"
```

### Analyze + Results
- `POST /runs/{run_id}/analyze` → compute and persist results
- `GET /runs/{run_id}/results` → fetch stored results

```bash
curl -X POST "http://127.0.0.1:8000/runs/<RUN_ID>/analyze"
curl -X GET  "http://127.0.0.1:8000/runs/<RUN_ID>/results"
```

---

## 🧠 Metrics (Current)

Current analysis computes uplift by category based on promo vs baseline rows:

- `units_base`, `units_promo`, `units_uplift`, `units_uplift_pct`
- `revenue_base`, `revenue_promo`, `revenue_uplift`, `revenue_uplift_pct`

Definitions:
- Baseline rows: non-promo rows
- Promo rows: `is_promo == 1` **OR** `promo_id` present

---

## 🗺️ Roadmap

### Next (Frontend MVP)
- React + TypeScript + Vite UI
- File upload page → run detail view
- KPI cards + category table + filters
- Export results (CSV/JSON)

### Stretch
- Promo comparison view
- Anomaly flags / outlier detection
- Postgres for persistent runs in production
- GitHub Actions CI (lint + tests) + deploy frontend to GitHub Pages

---

## 🧩 Notes on Persistence

- Local dev uses SQLite (`cpa.db` under `backend/` by default).
- In tests, we use an isolated temporary SQLite database created/reset for deterministic runs.

---

## 📄 License
MIT License. See `LICENSE`.

---

## 👤 Author
**Venkata Naga**  
GitHub: https://github.com/venkatasivanaga
