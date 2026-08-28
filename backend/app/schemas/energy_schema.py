from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class EnergyTelemetryIngest(BaseModel):
    device_id: str = Field(..., description="Smart energy meter ID (e.g. GRID-NODE-101)")
    voltage_v: float = Field(..., ge=80.0, le=300.0, description="Measured RMS voltage")
    current_a: float = Field(..., ge=0.0, le=100.0, description="RMS load current")
    frequency_hz: Optional[float] = Field(default=50.0, ge=45.0, le=65.0)

class EnergyTelemetryResponse(BaseModel):
    device_id: str
    voltage_v: float
    current_a: float
    active_power_kw: float
    power_factor: float
    grid_status: str
    anomaly_detected: bool
    timestamp: str
