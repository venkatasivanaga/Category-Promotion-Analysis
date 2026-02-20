# Category Promotion Analysis

A full-stack promo analytics app:
Upload a CSV → compute category/SKU promotion uplift → view dashboards → save runs → export results.

## Planned Features (MVP)
- Upload CSV and validate schema
- Compute uplift metrics (baseline vs promo window) by category (and optional SKU)
- Dashboard: KPI cards, category table, filters, trends
- Save analysis runs (SQLite) + shareable run links
- Export results (JSON/CSV)

## Tech Stack
- Frontend: React + TypeScript + Vite
- Backend: FastAPI (Python) + Pandas
- Storage: SQLite (upgradeable to Postgres)

## Dataset Requirements (initial)
Minimum recommended columns (names can be adapted later):
- `date` (YYYY-MM-DD or ISO datetime)
- `category`
- `units` (int/float)
- `revenue` (float)
- promo identifier (one of):
  - `promo_id` (preferred) OR
  - `is_promo` (0/1)

## Data Contract (v0)
Required:
- `date`: date or datetime
- `category`: string
- `units`: number
- `revenue`: number

At least one promo indicator:
- `promo_id` (string) OR `is_promo` (0/1)

Optional but supported later:
- `sku`
- `discount_pct`

> We’ll include a sample dataset in `/sample_data` and also add a “Load sample” button in the UI.