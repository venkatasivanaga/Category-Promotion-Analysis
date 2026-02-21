import io
from fastapi.testclient import TestClient
from app.main import app

VALID_CSV = """date,category,sku,units,revenue,promo_id,is_promo,discount_pct
2025-01-01,Beverages,BEV-001,120,240.00,,0,0
2025-01-04,Beverages,BEV-001,200,360.00,PROMO-10,1,10
"""

INVALID_CSV_MISSING_COL = """date,category,units,promo_id
2025-01-01,Beverages,120,PROMO-1
"""

def test_upload_valid_csv_sets_run_uploaded(tmp_path, monkeypatch):
    # Ensure uploads go into a temp folder
    monkeypatch.chdir(tmp_path)

    with TestClient(app) as client:
        run = client.post("/runs").json()
        run_id = run["id"]

        files = {"file": ("sample.csv", io.BytesIO(VALID_CSV.encode("utf-8")), "text/csv")}
        r = client.post(f"/runs/{run_id}/upload", files=files)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["status"] == "uploaded"
        assert body["original_filename"] == "sample.csv"
        assert body["file_path"] is not None

def test_upload_invalid_csv_returns_400(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with TestClient(app) as client:
        run = client.post("/runs").json()
        run_id = run["id"]

        files = {"file": ("bad.csv", io.BytesIO(INVALID_CSV_MISSING_COL.encode("utf-8")), "text/csv")}
        r = client.post(f"/runs/{run_id}/upload", files=files)
        assert r.status_code == 400