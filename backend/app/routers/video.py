from fastapi import APIRouter
from backend.app.schemas.video import VideoSummarizationRequest, VideoSummarizationResponse
from backend.app.services.video_service import video_service

router = APIRouter(prefix="/api/v1/video", tags=["Video Summarization & Keyframe Engine"])

@router.post("/summarize", response_model=VideoSummarizationResponse)
async def summarize_video_stream(payload: VideoSummarizationRequest):
    return video_service.process_video_stream(payload)
