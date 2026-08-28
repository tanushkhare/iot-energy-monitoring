import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_nominal_grid_telemetry():
    payload = {
        "device_id": "METER_TEST_01",
        "voltage_v": 230.0,
        "current_a": 10.0,
        "frequency_hz": 50.0
    }
    res = client.post("/api/v1/iot/telemetry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["anomaly_detected"] is False
    assert data["active_power_kw"] > 0
    assert data["grid_status"] == "GRID_STABLE_NOMINAL"

def test_overvoltage_anomaly():
    payload = {
        "device_id": "METER_TEST_ANOMALY",
        "voltage_v": 265.0,
        "current_a": 15.0,
        "frequency_hz": 50.0
    }
    res = client.post("/api/v1/iot/telemetry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["anomaly_detected"] is True
    assert "OVERVOLTAGE" in data["grid_status"]
