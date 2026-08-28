from fastapi import APIRouter, HTTPException
from backend.app.schemas.energy_schema import EnergyTelemetryIngest, EnergyTelemetryResponse
from backend.app.services.energy_service import energy_engine

router = APIRouter(prefix="/api/v1/iot", tags=["IoT Smart Grid Energy Monitoring"])

@router.post("/telemetry", response_model=EnergyTelemetryResponse)
async def ingest_grid_telemetry(payload: EnergyTelemetryIngest):
    try:
        result = energy_engine.evaluate_telemetry(
            payload.device_id, payload.voltage_v, payload.current_a, payload.frequency_hz or 50.0
        )
        return EnergyTelemetryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
