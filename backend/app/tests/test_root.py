from fastapi.testclient import TestClient
from app.main import app

def test_root():
    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        body = r.json()
        assert "message" in body
        assert body.get("docs") == "/docs"