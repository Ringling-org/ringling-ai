from fastapi import APIRouter
from pydantic import BaseModel
from services.summarizer import summarize_title

ROUTE_PREFIX = "/summary"
router = APIRouter()

class TitleSummarizationRequest(BaseModel):
    targetUrl: str

@router.post("")
def summarize_title_from_url_content(request: TitleSummarizationRequest):
    summary_title  = summarize_title(request.targetUrl)
    return {"summaryTitle": summary_title}
