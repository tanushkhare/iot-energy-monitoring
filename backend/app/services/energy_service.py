import math
from datetime import datetime, timezone
from typing import Dict, Any, List

class EnergyMonitoringEngine:
    def __init__(self):
        self.telemetry_store: Dict[str, List[Dict[str, Any]]] = {}

    def evaluate_telemetry(self, device_id: str, voltage: float, current: float, freq: float = 50.0) -> Dict[str, Any]:
        apparent_power_va = voltage * current
        power_factor = 0.92 if current > 0.5 else 1.0
        active_power_kw = round((apparent_power_va * power_factor) / 1000.0, 3)

        is_anomaly = False
        status = "GRID_STABLE_NOMINAL"

        if voltage > 250.0:
            is_anomaly = True
            status = "SURGE_OVERVOLTAGE_ALARM"
        elif voltage < 205.0:
            is_anomaly = True
            status = "BROWNOUT_UNDERVOLTAGE_ALARM"
        elif current > 45.0:
            is_anomaly = True
            status = "CRITICAL_OVERCURRENT_ALERT"
        elif abs(freq - 50.0) > 1.5:
            is_anomaly = True
            status = "FREQUENCY_DEVIATION_WARNING"

        reading = {
            "device_id": device_id,
            "voltage_v": round(voltage, 2),
            "current_a": round(current, 2),
            "active_power_kw": active_power_kw,
            "power_factor": round(power_factor, 2),
            "grid_status": status,
            "anomaly_detected": is_anomaly,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        if device_id not in self.telemetry_store:
            self.telemetry_store[device_id] = []
        self.telemetry_store[device_id].append(reading)

        return reading

    def get_device_history(self, device_id: str) -> Dict[str, Any]:
        records = self.telemetry_store.get(device_id, [])
        return {
            "device_id": device_id,
            "total_samples": len(records),
            "history": records
        }

energy_engine = EnergyMonitoringEngine()
