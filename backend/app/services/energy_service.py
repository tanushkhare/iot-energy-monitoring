import math
from datetime import datetime, timezone
from typing import Dict, Any

class EnergyMonitoringEngine:
    def evaluate_telemetry(self, device_id: str, voltage: float, current: float, freq: float = 50.0) -> Dict[str, Any]:
        # Theoretical apparent power and active power calculation
        apparent_power_va = voltage * current
        power_factor = 0.92 if current > 0.5 else 1.0
        active_power_kw = round((apparent_power_va * power_factor) / 1000.0, 3)
        
        # Anomaly threshold checks (Overvoltage > 250V, Undervoltage < 205V, Frequency instability)
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

        return {
            "device_id": device_id,
            "voltage_v": round(voltage, 2),
            "current_a": round(current, 2),
            "active_power_kw": active_power_kw,
            "power_factor": power_factor,
            "grid_status": status,
            "anomaly_detected": is_anomaly,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

energy_engine = EnergyMonitoringEngine()
