from typing import Dict, Any
from datetime import datetime, timezone

class IoTEnergyEngine:
    def evaluate_telemetry(self, device_id: str, voltage_v: float, current_a: float, power_factor: float = 0.95) -> Dict[str, Any]:
        active_power_kw = round((voltage_v * current_a * power_factor) / 1000.0, 3)
        grid_anomaly = voltage_v < 210.0 or voltage_v > 245.0 or current_a > 32.0
        
        return {
            "device_id": device_id,
            "voltage_v": voltage_v,
            "current_a": current_a,
            "active_power_kw": active_power_kw,
            "grid_status": "CRITICAL_ANOMALY" if grid_anomaly else "OPTIMAL_LOAD",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

iot_engine = IoTEnergyEngine()
