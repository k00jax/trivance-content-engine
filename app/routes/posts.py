from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.generator import generate_commentary
from app.services.posts import save_generated_post, get_all_posts, get_recent_posts

router = APIRouter()

class ArticleInput(BaseModel):
    title: str
    summary: str
    source: str
    link: str = ""
    post_style: Optional[str] = "consultative"

@router.post("/generate")
def generate_post(article: ArticleInput):
    # Generate the content with style parameter
    result = generate_commentary(article, post_style=article.post_style)
    
    # Save the generated post to persistent storage
    if "post" in result:
        save_generated_post(
            title=article.title,
            summary=article.summary,
            source=article.source,
            link=article.link,
            generated_content=result["post"]
        )
    
    return result

@router.get("/")
def get_posts(limit: int = 10):
    """Get recent posts with optional limit."""
    return get_recent_posts(limit)

@router.get("/all")
def get_all_generated_posts():
    """Get all generated posts."""
    return get_all_posts()
