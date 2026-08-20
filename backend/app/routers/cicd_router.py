from fastapi import APIRouter
from app.schemas.cicd import PipelineStatus
from app.services.cicd_service import get_pipeline_status

router = APIRouter(prefix="/api", tags=["CI/CD Pipeline"])

@router.get("/pipeline-status", response_model=PipelineStatus)
def pipeline_status():
    return get_pipeline_status()