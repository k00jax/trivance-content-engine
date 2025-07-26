import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .persistence import save_json, load_json

# Load feeds from persistent storage on startup
feeds_db = load_json("feeds.json", [])

def add_feed(feed):
    global feeds_db
    new_feed = {"name": feed.name, "url": feed.url}
    feeds_db.append(new_feed)
    save_json("feeds.json", feeds_db)
    return {"message": "Feed added", "total": len(feeds_db)}

def get_all_feeds():
    return feeds_db

def remove_feed(name: str):
    global feeds_db
    feeds_db = [f for f in feeds_db if f["name"] != name]
    save_json("feeds.json", feeds_db)
    return {"message": f"Feed '{name}' removed."}

def score_article(title: str, summary: str) -> int:
    """
    Score article relevance to Trivance's target audience.
    Higher scores indicate better fit for SMB AI strategy content.
    """
    keywords = [
        "AI", "GPT", "automation", "business", "workflow", "ops", "strategy", 
        "productivity", "ChatGPT", "machine learning", "artificial intelligence",
        "small business", "startup", "entrepreneur", "efficiency", "optimization",
        "digital transformation", "innovation", "technology adoption"
    ]
    
    score = 0
    content = f"{title} {summary}".lower()
    
    # Keyword scoring (higher weight for title matches)
    title_lower = title.lower()
    summary_lower = summary.lower()
    
    for keyword in keywords:
        kw_lower = keyword.lower()
        if kw_lower in title_lower:
            score += 3  # Title matches worth more
        elif kw_lower in summary_lower:
            score += 2
    
    # Content length bonus (substantial articles preferred)
    word_count = len(summary.split())
    if word_count > 50:
        score += 2
    elif word_count > 30:
        score += 1
    
    # Avoid purely technical or academic content
    avoid_terms = ["research paper", "peer review", "academic", "phd", "university study"]
    for term in avoid_terms:
        if term in content:
            score -= 1
    
    return max(0, score)  # Ensure non-negative score

def fetch_articles_from_feed(feed_url: str, limit: int = 10) -> List[Dict]:
    """
    Fetch articles from a single RSS feed using feedparser.
    Returns list of articles with title, summary, link, published, and score.
    """
    try:
        # Set user agent to avoid blocking
        feedparser.USER_AGENT = "Trivance AI Content Engine 1.0"
        
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            return []
        
        articles = []
        for entry in feed.entries[:limit]:
            # Extract basic info
            title = getattr(entry, 'title', 'No title')
            summary = getattr(entry, 'summary', getattr(entry, 'description', 'No summary'))
            link = getattr(entry, 'link', '')
            published = getattr(entry, 'published', '')
            
            # Clean up summary (remove HTML tags if present)
            if summary:
                import re
                summary = re.sub('<[^<]+?>', '', summary)  # Remove HTML tags
                summary = summary.strip()
            
            # Calculate relevance score
            score = score_article(title, summary)
            
            articles.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
                "score": score
            })
        
        # Sort by score (highest first) then by published date
        articles.sort(key=lambda x: (x["score"], x.get("published", "")), reverse=True)
        
        return articles
        
    except Exception as e:
        print(f"Error fetching articles from {feed_url}: {e}")
        return []

def get_top_article_from_all_feeds(max_age_days: int = 7) -> Optional[Dict]:
    """
    Get the highest-scoring article from all feeds.
    Optionally filter out articles older than max_age_days.
    """
    all_articles = []
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    
    for feed in feeds_db:
        feed_articles = fetch_articles_from_feed(feed["url"], limit=5)
        
        # Add source feed info and filter by date if needed
        for article in feed_articles:
            article["source_feed"] = feed["name"]
            article["source_url"] = feed["url"]
            
            # Optional: filter by date (requires parsing published date)
            # For now, include all articles
            all_articles.append(article)
    
    if not all_articles:
        return None
    
    # Sort by score and return the top one
    all_articles.sort(key=lambda x: x["score"], reverse=True)
    return all_articles[0]

def get_articles_by_feed_name(feed_name: str, limit: int = 10) -> List[Dict]:
    """
    Get articles from a specific feed by name.
    """
    feed = next((f for f in feeds_db if f["name"] == feed_name), None)
    if not feed:
        return []
    
    articles = fetch_articles_from_feed(feed["url"], limit)
    
    # Add source feed info
    for article in articles:
        article["source_feed"] = feed_name
        article["source_url"] = feed["url"]
    
    return articles
