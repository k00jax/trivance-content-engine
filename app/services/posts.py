"""
Posts service for managing generated posts with persistence.
"""
from datetime import datetime
from typing import Dict, List
from .persistence import save_json, load_json, append_to_json

def save_generated_post(title: str, summary: str, source: str, link: str, generated_content: str) -> Dict:
    """Save a generated post to persistent storage."""
    post_data = {
        "id": datetime.now().isoformat(),
        "title": title,
        "summary": summary,
        "source": source,
        "link": link,
        "generated_content": generated_content,
        "created_at": datetime.now().isoformat(),
        "timestamp": datetime.now().timestamp()
    }
    
    append_to_json("posts.json", post_data)
    return {"message": "Post saved successfully", "post_id": post_data["id"]}

def get_all_posts() -> List[Dict]:
    """Retrieve all generated posts from storage."""
    return load_json("posts.json", [])

def get_recent_posts(limit: int = 10) -> List[Dict]:
    """Get the most recent posts, limited by count."""
    posts = get_all_posts()
    # Sort by timestamp descending and limit
    sorted_posts = sorted(posts, key=lambda x: x.get("timestamp", 0), reverse=True)
    return sorted_posts[:limit]

def delete_post(post_id: str) -> Dict:
    """Delete a post by ID."""
    posts = get_all_posts()
    updated_posts = [p for p in posts if p.get("id") != post_id]
    
    if len(updated_posts) == len(posts):
        return {"message": "Post not found", "success": False}
    
    save_json("posts.json", updated_posts)
    return {"message": "Post deleted successfully", "success": True}

# Future database integration methods
def migrate_posts_to_db():
    """
    Future: Migrate existing JSON posts to database.
    This function would:
    1. Load all posts from posts.json
    2. Insert them into database tables
    3. Handle any data transformation needed
    4. Backup JSON file before migration
    """
    pass
