from __future__ import annotations

import os
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"date", "category", "units", "revenue"}
PROMO_COLUMNS_OK = [{"promo_id"}, {"is_promo"}]

def ensure_upload_dir(upload_dir: str) -> Path:
    p = Path(upload_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p

def validate_columns(df: pd.DataFrame) -> None:
    cols = set(c.strip() for c in df.columns)
    missing = REQUIRED_COLUMNS - cols
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    has_promo = any(req.issubset(cols) for req in PROMO_COLUMNS_OK)
    if not has_promo:
        raise ValueError("Missing promo indicator: include 'promo_id' or 'is_promo' column")

def load_csv_from_path(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_columns(df)
    return df