from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import energy_router
import uvicorn

app = FastAPI(
    title="IoT Smart Grid Energy & Power Telemetry API",
    description="High-frequency smart meter ingestion, load profiling, and power quality anomaly detection.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(energy_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iot-energy-monitoring"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
