from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.generator import generate_commentary
from app.services.posts import save_generated_post, get_all_posts, get_recent_posts
from app.services.persistence import save_json, load_json
import re
from datetime import datetime

router = APIRouter()

class ArticleInput(BaseModel):
    title: str = Field(..., min_length=5, description="Article title")
    summary: str = Field(..., min_length=20, description="Article summary or content")
    source: str = Field(default="RSS Feeds", description="Source publication")
    link: str = Field(default="", description="Link to original article")
    post_style: Optional[str] = Field(default="consultative", description="Writing style")
    platform: Optional[str] = Field(default="LinkedIn", description="Target platform")
    
    # Alternative field names for compatibility
    url: Optional[str] = Field(default=None, description="Alternative to link")
    style: Optional[str] = Field(default=None, description="Alternative to post_style")
    
    def __init__(self, **data):
        # Handle alternative field names
        if 'url' in data and not data.get('link'):
            data['link'] = data.get('url', '')
        if 'style' in data and not data.get('post_style'):
            data['post_style'] = data.get('style', 'consultative')
        # Ensure source has a value
        if not data.get('source') or not data.get('source').strip():
            data['source'] = "RSS Feeds"
        super().__init__(**data)

class HashtagInput(BaseModel):
    content: str

class MediaInput(BaseModel):
    content: str

class PostHistoryInput(BaseModel):
    title: str
    source: str
    enhanced_summary: str
    generated_post: str
    platform: str
    media: Optional[str] = None
    hashtags: List[str] = []
    timestamp: str

@router.post("/debug")
def debug_input(payload: Dict[str, Any]):
    """Debug endpoint to inspect incoming JSON payloads."""
    return {
        "received_keys": list(payload.keys()),
        "payload": payload,
        "payload_types": {k: type(v).__name__ for k, v in payload.items()}
    }

@router.post("/generate")
def generate_post(article: ArticleInput):
    """Generate a post from article content with error handling."""
    try:
        # Log the received data for debugging
        print(f"Received article data: title='{article.title}', source='{article.source}', style='{article.post_style}'")
        print(f"Using article source: {article.source}")  # ✅ Debug echo for source
        
        # Generate content with style parameter
        result = generate_commentary(article, post_style=article.post_style)
        
        # Ensure result has expected structure
        if not isinstance(result, dict):
            raise ValueError("Generator returned invalid result format")
        
        # Save the generated post to persistent storage
        if "post" in result:
            save_generated_post(
                title=article.title,
                summary=article.summary,
                source=article.source,
                link=article.link,
                generated_content=result["post"]
            )
        else:
            print("Warning: No 'post' field in generation result")
        
        return result
        
    except Exception as e:
        print(f"Error in generate_post: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail=f"Error generating post: {str(e)}"
        )

@router.post("/hashtags")
def generate_hashtags(input_data: HashtagInput):
    """Generate hashtags for given content."""
    content = input_data.content.lower()
    
    # Extract key topics using simple keyword matching
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'automation', 'technology']
    business_keywords = ['business', 'strategy', 'growth', 'leadership', 'management', 'entrepreneur']
    smb_keywords = ['small business', 'startup', 'smb', 'local business', 'family business']
    
    # Base hashtags for Trivance content
    hashtags = []
    
    # Always include core tags
    hashtags.extend(['TrivanceAI', 'SmallBusinessAI'])
    
    # Add relevant topic hashtags
    if any(keyword in content for keyword in ai_keywords):
        hashtags.extend(['ArtificialIntelligence', 'AIStrategy', 'TechSolutions'])
    
    if any(keyword in content for keyword in business_keywords):
        hashtags.extend(['BusinessStrategy', 'Leadership', 'Growth'])
    
    if any(keyword in content for keyword in smb_keywords):
        hashtags.extend(['SmallBusiness', 'Entrepreneur', 'LocalBusiness'])
    
    # Add trending tech hashtags
    hashtags.extend(['Innovation', 'DigitalTransformation'])
    
    # Remove duplicates and limit to 8
    unique_hashtags = list(dict.fromkeys(hashtags))[:8]
    
    return {"hashtags": unique_hashtags}

@router.post("/media")
def generate_media(input_data: MediaInput):
    """Generate media prompt for DALL-E (placeholder for now)."""
    
    # Extract key themes from content
    content = input_data.content.lower()
    
    # Generate a DALL-E prompt based on content themes
    prompt_elements = []
    
    if 'ai' in content or 'artificial intelligence' in content:
        prompt_elements.append("futuristic AI technology")
    
    if 'business' in content or 'strategy' in content:
        prompt_elements.append("professional business environment")
    
    if 'small business' in content or 'entrepreneur' in content:
        prompt_elements.append("modern small business office")
    
    # Default elements
    if not prompt_elements:
        prompt_elements.append("modern technology and business")
    
    # Combine into a DALL-E prompt
    dalle_prompt = f"A professional, clean illustration showing {', '.join(prompt_elements)}, modern design, business-friendly colors, high quality digital art"
    
    # For now, return a placeholder response
    # In production, this would call OpenAI's DALL-E API
    return {
        "prompt": dalle_prompt,
        "url": "https://via.placeholder.com/512x512/4A90E2/FFFFFF?text=AI+Content+Media",
        "status": "placeholder",
        "message": "Media generation endpoint ready - integrate with DALL-E API"
    }

@router.post("/save")
def save_post_to_history(post_data: PostHistoryInput):
    """Save a published post to history."""
    try:
        # Load existing history
        history = load_json("generated_posts.json", [])
        
        # Add new post
        new_post = {
            "id": len(history) + 1,
            "title": post_data.title,
            "source": post_data.source,
            "enhanced_summary": post_data.enhanced_summary,
            "generated_post": post_data.generated_post,
            "platform": post_data.platform,
            "media": post_data.media,
            "hashtags": post_data.hashtags,
            "timestamp": post_data.timestamp,
            "character_count": len(post_data.generated_post),
            "word_count": len(post_data.generated_post.split())
        }
        
        history.append(new_post)
        
        # Save updated history
        save_json("generated_posts.json", history)
        
        return {
            "message": "Post saved to history successfully",
            "post_id": new_post["id"],
            "total_posts": len(history)
        }
        
    except Exception as e:
        return {"error": f"Failed to save post: {str(e)}"}

@router.get("/history")
def get_post_history(limit: int = 50):
    """Get post generation history."""
    try:
        history = load_json("generated_posts.json", [])
        # Return most recent first
        recent_history = sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)
        return recent_history[:limit]
    except Exception as e:
        return {"error": f"Failed to load history: {str(e)}"}

@router.get("/")
def get_posts(limit: int = 10):
    """Get recent posts with optional limit."""
    return get_recent_posts(limit)

@router.get("/all")
def get_all_generated_posts():
    """Get all generated posts."""
    return get_all_posts()
