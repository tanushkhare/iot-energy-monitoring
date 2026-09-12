from fastapi import APIRouter, HTTPException
from backend.app.schemas.energy_schema import (
    EnergyTelemetryIngest,
    EnergyTelemetryResponse,
    GridTelemetryHistory
)
from backend.app.services.energy_service import energy_engine

router = APIRouter(prefix="/api/v1/energy", tags=["IoT Smart Grid Energy Telemetry"])

@router.post("/telemetry", response_model=EnergyTelemetryResponse)
async def ingest_telemetry(payload: EnergyTelemetryIngest):
    try:
        res = energy_engine.evaluate_telemetry(
            payload.device_id, payload.voltage_v, payload.current_a, payload.frequency_hz or 50.0
        )
        return EnergyTelemetryResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{device_id}", response_model=GridTelemetryHistory)
async def get_history(device_id: str):
    return GridTelemetryHistory(**energy_engine.get_device_history(device_id))
