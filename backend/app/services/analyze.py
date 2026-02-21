from __future__ import annotations
import pandas as pd

def compute_category_uplift(df: pd.DataFrame) -> dict:
    """
    Minimal uplift:
    - promo rows: is_promo==1 OR promo_id not null/empty
    - baseline rows: everything else
    Returns a dict with KPI + per-category table.
    """
    df = df.copy()

    # Normalize promo flag
    if "is_promo" in df.columns:
        promo_mask = df["is_promo"].fillna(0).astype(int) == 1
    else:
        promo_mask = df.get("promo_id").fillna("").astype(str).str.strip() != ""

    df["is_promo_norm"] = promo_mask

    # Aggregate by category for baseline and promo
    base = df[~df["is_promo_norm"]].groupby("category", dropna=False)[["units", "revenue"]].sum()
    promo = df[df["is_promo_norm"]].groupby("category", dropna=False)[["units", "revenue"]].sum()

    merged = base.join(promo, how="outer", lsuffix="_base", rsuffix="_promo").fillna(0.0)

    merged["units_uplift"] = merged["units_promo"] - merged["units_base"]
    merged["revenue_uplift"] = merged["revenue_promo"] - merged["revenue_base"]

    merged["units_uplift_pct"] = merged.apply(
        lambda r: (r["units_uplift"] / r["units_base"] * 100.0) if r["units_base"] else None,
        axis=1,
    )
    merged["revenue_uplift_pct"] = merged.apply(
        lambda r: (r["revenue_uplift"] / r["revenue_base"] * 100.0) if r["revenue_base"] else None,
        axis=1,
    )

    rows = []
    for cat, r in merged.reset_index().iterrows():
        rows.append({
            "category": r["category"],
            "units_base": float(r["units_base"]),
            "units_promo": float(r["units_promo"]),
            "units_uplift": float(r["units_uplift"]),
            "units_uplift_pct": None if pd.isna(r["units_uplift_pct"]) else float(r["units_uplift_pct"]),
            "revenue_base": float(r["revenue_base"]),
            "revenue_promo": float(r["revenue_promo"]),
            "revenue_uplift": float(r["revenue_uplift"]),
            "revenue_uplift_pct": None if pd.isna(r["revenue_uplift_pct"]) else float(r["revenue_uplift_pct"]),
        })

    # Overall KPIs
    total_base_rev = float(df[~df["is_promo_norm"]]["revenue"].sum())
    total_promo_rev = float(df[df["is_promo_norm"]]["revenue"].sum())
    total_uplift_rev = total_promo_rev - total_base_rev

    return {
        "kpis": {
            "total_revenue_base": total_base_rev,
            "total_revenue_promo": total_promo_rev,
            "total_revenue_uplift": total_uplift_rev,
        },
        "by_category": rows,
    }