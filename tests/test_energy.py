import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_nominal_energy_telemetry():
    payload = {
        "device_id": "METER-ALPHA-01",
        "voltage_v": 230.0,
        "current_a": 10.0,
        "frequency_hz": 50.0
    }
    res = client.post("/api/v1/energy/telemetry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["anomaly_detected"] is False
    assert data["grid_status"] == "GRID_STABLE_NOMINAL"
    assert data["active_power_kw"] > 0.0

def test_overvoltage_surge_anomaly():
    payload = {
        "device_id": "METER-CRITICAL-99",
        "voltage_v": 265.0,
        "current_a": 12.0,
        "frequency_hz": 50.0
    }
    res = client.post("/api/v1/energy/telemetry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["anomaly_detected"] is True
    assert data["grid_status"] == "SURGE_OVERVOLTAGE_ALARM"
