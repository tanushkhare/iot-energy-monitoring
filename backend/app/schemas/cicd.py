from pydantic import BaseModel

class PipelineStatus(BaseModel):
    pipeline_id: str
    branch: str
    last_commit: str
    build_status: str