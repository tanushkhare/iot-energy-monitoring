from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers.video import router as video_router
import uvicorn

app = FastAPI(
    title="Automated Video Summarization & Keyframe Engine API",
    description="Live video frame condensation, scene change heuristics, and keyframe telemetry.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "video-summarizer-engine"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
