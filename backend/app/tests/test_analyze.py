import io
from fastapi.testclient import TestClient
from app.main import app

CSV = """date,category,units,revenue,is_promo
2025-01-01,A,10,100,0
2025-01-02,A,10,100,0
2025-01-03,A,30,240,1
2025-01-01,B,5,50,0
2025-01-03,B,6,72,1
"""

def test_analyze_and_get_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with TestClient(app) as client:
        run_id = client.post("/runs").json()["id"]
        files = {"file": ("x.csv", io.BytesIO(CSV.encode("utf-8")), "text/csv")}
        up = client.post(f"/runs/{run_id}/upload", files=files)
        assert up.status_code == 200, up.text

        an = client.post(f"/runs/{run_id}/analyze")
        assert an.status_code == 200, an.text
        body = an.json()
        assert body["run_id"] == run_id
        assert "kpis" in body["summary"]
        assert "by_category" in body["summary"]

        gr = client.get(f"/runs/{run_id}/results")
        assert gr.status_code == 200, gr.text
        assert gr.json()["run_id"] == run_id