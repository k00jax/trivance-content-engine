from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.rss import (
    add_feed, get_all_feeds, remove_feed, 
    get_articles_by_feed_name, get_top_article_from_all_feeds
)

router = APIRouter()

class FeedInput(BaseModel):
    name: str
    url: str

@router.post("/")
def create_feed(feed: FeedInput):
    return add_feed(feed)

@router.get("/")
def list_feeds():
    return get_all_feeds()

@router.delete("/")
def delete_feed(name: str):
    return remove_feed(name)

@router.get("/articles")
def get_articles(feed_name: str, limit: Optional[int] = 10):
    """
    Get articles from a specific feed by name.
    Returns articles with title, summary, link, published date, and relevance score.
    """
    try:
        articles = get_articles_by_feed_name(feed_name, limit)
        if not articles:
            raise HTTPException(
                status_code=404, 
                detail=f"No articles found for feed '{feed_name}' or feed does not exist"
            )
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")

@router.get("/top-article")
def get_top_article(max_age_days: Optional[int] = 7):
    """
    Get the highest-scoring article from all feeds.
    Useful for auto-generation mode.
    """
    try:
        article = get_top_article_from_all_feeds(max_age_days)
        if not article:
            raise HTTPException(
                status_code=404, 
                detail="No articles found in any feeds"
            )
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting top article: {str(e)}")

@router.get("/articles/all")
def get_all_articles(limit_per_feed: Optional[int] = 5):
    """
    Get articles from all feeds with scores.
    Useful for debugging and manual selection across feeds.
    """
    try:
        from app.services.rss import feeds_db, fetch_articles_from_feed
        
        all_articles = []
        for feed in feeds_db:
            feed_articles = fetch_articles_from_feed(feed["url"], limit_per_feed)
            for article in feed_articles:
                article["source_feed"] = feed["name"]
                article["source_url"] = feed["url"]
                all_articles.append(article)
        
        # Sort by score
        all_articles.sort(key=lambda x: x["score"], reverse=True)
        return all_articles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all articles: {str(e)}")
