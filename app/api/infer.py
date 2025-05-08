from fastapi import APIRouter
from pydantic import BaseModel
from services.title_generator import do_inference

ROUTE_PREFIX = "/infer"
router = APIRouter()

class ContentRequest(BaseModel):
    content: str

@router.post("/")
def generate_title_from_url_content(request: ContentRequest):
    summary_title  = do_inference(request.content)
    return {"title": summary_title}
