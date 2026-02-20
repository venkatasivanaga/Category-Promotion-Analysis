from fastapi.testclient import TestClient
from app.main import app

def test_create_and_get_run():
    client = TestClient(app)
    created = client.post("/runs").json()
    assert "id" in created
    run_id = created["id"]

    got = client.get(f"/runs/{run_id}")
    assert got.status_code == 200
    assert got.json()["id"] == run_id

def test_list_runs():
    client = TestClient(app)
    client.post("/runs")
    r = client.get("/runs")
    assert r.status_code == 200
    assert isinstance(r.json(), list)