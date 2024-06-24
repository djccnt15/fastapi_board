from fastapi.testclient import TestClient

from main import app

client = TestClient(app)  # synchronous client


def test_health():
    res = client.get(url="/health")
    assert res.status_code == 200
    assert res.text == "1"


def test_ping():
    res = client.get(url="/ping")
    assert res.status_code == 200
    assert res.text == "pong"
