from pydantic import BaseModel, Field
from typing import List

class VideoSummarizationRequest(BaseModel):
    batch_size: int = Field(default=2500, ge=100, le=100000)
    video_source: str = Field(default="prod_stream_segment_04.mp4")
    sampling_fps: float = Field(default=30.0)

class KeyframeMetric(BaseModel):
    timestamp_sec: float
    scene_id: str
    visual_density_score: float
    keyframe_label: str
    change_confidence_pct: float

class VideoSummarizationResponse(BaseModel):
    video_source: str
    total_frames_analyzed: int
    compression_ratio_pct: float
    visual_density_index: str
    processing_time_ms: float
    summary_transcript: str
    keyframes: List[KeyframeMetric]
