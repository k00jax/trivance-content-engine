from fastapi import APIRouter
from pydantic import BaseModel
from app.services.generator import generate_commentary

router = APIRouter()

class ArticleInput(BaseModel):
    title: str
    summary: str
    source: str
    link: str

@router.post("/generate")
def generate_post(article: ArticleInput):
    return generate_commentary(article)
