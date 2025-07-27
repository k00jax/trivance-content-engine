import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
from .persistence import save_json, load_json

# Load feeds from persistent storage on startup
feeds_db = load_json("feeds.json", [])

def get_feed_name_by_url(url: str) -> Optional[str]:
    """Get the feed name by URL from the feeds database."""
    for feed in feeds_db:
        if feed["url"] == url:
            return feed["name"]
    return None

# Configuration for content enhancement
CONTENT_ENHANCEMENT_CONFIG = {
    "enabled": True,  # Set to False to disable content extraction
    "max_summary_length": 1000,  # Maximum length for enhanced summaries
    "extraction_timeout": 10,  # Timeout for web scraping in seconds
    "min_enhancement_ratio": 1.5,  # Only use enhanced content if it's 50% longer
    "min_enhanced_length": 200,  # Minimum length to consider content "enhanced"
}

def clean_html(text: str) -> str:
    """Clean HTML tags and entities from text."""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # First decode standard HTML entities using html.unescape
    import html
    text = html.unescape(text)
    
    # Replace additional common HTML entities that might not be caught
    html_entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'",
        '&nbsp;': ' ',
        '&mdash;': '—',
        '&ndash;': '–',
        '&#38;': '&',        # Numeric entity for &
        '&#8212;': '—',      # Numeric entity for em dash
        '&#8213;': '—',      # Another em dash variant
        '&#8216;': ''',      # Left single quote
        '&#8217;': ''',      # Right single quote
        '&#8220;': '"',      # Left double quote
        '&#8221;': '"',      # Right double quote
        '&#8230;': '...',    # Ellipsis
    }
    
    for entity, replacement in html_entities.items():
        text = text.replace(entity, replacement)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_article_content(url: str, fallback_summary: str) -> str:
    """
    Attempt to extract fuller article content from the URL.
    Falls back to RSS summary if extraction fails.
    """
    try:
        # Skip extraction for certain domains that are problematic
        skip_domains = ['youtube.com', 'twitter.com', 'linkedin.com', 'facebook.com']
        if any(domain in url.lower() for domain in skip_domains):
            return fallback_summary
        
        # Set headers to appear like a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Try to fetch the article page with timeout
        timeout = CONTENT_ENHANCEMENT_CONFIG["extraction_timeout"]
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        html_content = response.text
        
        # Try to extract article content using common selectors
        content_selectors = [
            # Common article content selectors
            r'<article[^>]*>(.*?)</article>',
            r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*post[^"]*"[^>]*>(.*?)</div>',
            r'<main[^>]*>(.*?)</main>',
            r'<section[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</section>',
        ]
        
        extracted_content = ""
        
        for selector in content_selectors:
            matches = re.findall(selector, html_content, re.DOTALL | re.IGNORECASE)
            if matches:
                # Take the first match and clean it
                raw_content = matches[0]
                cleaned = clean_html(raw_content)
                
                # If we got substantial content (more than the fallback), use it
                if len(cleaned) > len(fallback_summary) * 1.5 and len(cleaned) > 200:
                    extracted_content = cleaned
                    break
        
        # If we got good content, return it (truncated to reasonable length)
        if extracted_content and len(extracted_content) > len(fallback_summary):
            # Truncate to first few paragraphs or reasonable length
            sentences = extracted_content.split('. ')
            
            # Take first 8-10 sentences or up to 800 characters
            summary_sentences = []
            char_count = 0
            
            for sentence in sentences:
                if char_count + len(sentence) > 800 or len(summary_sentences) >= 10:
                    break
                summary_sentences.append(sentence)
                char_count += len(sentence)
            
            if summary_sentences:
                result = '. '.join(summary_sentences)
                if not result.endswith('.'):
                    result += '.'
                return result
        
        # If extraction didn't work well, return the original summary
        return fallback_summary
        
    except Exception as e:
        # If anything goes wrong, return the original RSS summary
        print(f"Content extraction failed for {url}: {e}")
        return fallback_summary

def enhance_rss_summary(entry, max_length: int = None) -> str:
    """
    Get the best possible summary from RSS entry and optionally enhance it.
    """
    # Use config for max length if not specified
    if max_length is None:
        max_length = CONTENT_ENHANCEMENT_CONFIG["max_summary_length"]
    
    # Try multiple fields in order of preference
    summary_fields = ['summary', 'description', 'content', 'subtitle']
    
    raw_summary = ""
    for field in summary_fields:
        content = getattr(entry, field, None)
        if content:
            if isinstance(content, list) and len(content) > 0:
                # Some feeds have content as a list of dicts
                if hasattr(content[0], 'value'):
                    raw_summary = content[0].value
                else:
                    raw_summary = str(content[0])
            else:
                raw_summary = str(content)
            
            if raw_summary and len(raw_summary.strip()) > 50:
                break
    
    if not raw_summary:
        raw_summary = "No summary available"
    
    # Clean the summary
    cleaned_summary = clean_html(raw_summary)
    
    # Check if content enhancement is enabled and summary needs enhancement
    config = CONTENT_ENHANCEMENT_CONFIG
    if (config["enabled"] and 
        (len(cleaned_summary) < config["min_enhanced_length"] or 
         cleaned_summary.endswith('...') or 
         cleaned_summary.endswith('[…]') or 
         'read more' in cleaned_summary.lower())):
        
        article_url = getattr(entry, 'link', '')
        if article_url:
            enhanced_summary = extract_article_content(article_url, cleaned_summary)
            if (enhanced_summary and 
                len(enhanced_summary) >= config["min_enhanced_length"] and
                len(enhanced_summary) >= len(cleaned_summary) * config["min_enhancement_ratio"]):
                cleaned_summary = enhanced_summary
    
    # Ensure reasonable length
    if len(cleaned_summary) > max_length:
        # Try to cut at sentence boundary
        sentences = cleaned_summary[:max_length].split('. ')
        if len(sentences) > 1:
            cleaned_summary = '. '.join(sentences[:-1]) + '.'
        else:
            cleaned_summary = cleaned_summary[:max_length] + '...'
    
    return cleaned_summary

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
    Returns list of articles with title, enhanced summary, link, published, score, and source.
    """
    try:
        # Set user agent to avoid blocking
        feedparser.USER_AGENT = "Trivance AI Content Engine 1.0"
        
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            return []

        # Get the feed name for source attribution
        feed_name = get_feed_name_by_url(feed_url)
        source = feed_name or "RSS Feeds"  # ✅ Fallback if name not found
        
        articles = []
        for entry in feed.entries[:limit]:
            # Extract basic info
            title = getattr(entry, 'title', 'No title')
            link = getattr(entry, 'link', '')
            published = getattr(entry, 'published', '')
            
            # Get enhanced summary
            try:
                enhanced_summary = enhance_rss_summary(entry, max_length=1000)
            except Exception as e:
                print(f"Error enhancing summary for {title}: {e}")
                # Fallback to basic summary extraction
                raw_summary = getattr(entry, 'summary', getattr(entry, 'description', 'No summary'))
                enhanced_summary = clean_html(raw_summary) if raw_summary else 'No summary'
            
            # Calculate relevance score using the enhanced summary
            score = score_article(title, enhanced_summary)
            
            articles.append({
                "title": clean_html(title),
                "summary": enhanced_summary,
                "link": link,
                "published": published,
                "score": score,
                "source": source,  # ✅ Add the feed's name as source
                "word_count": len(enhanced_summary.split()),
                "enhanced": len(enhanced_summary) > 200  # Flag if we got enhanced content
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
        
        # Add additional feed metadata (source is already included from fetch_articles_from_feed)
        for article in feed_articles:
            article["source_feed"] = feed["name"]  # Keep for backward compatibility
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
    
    # Add additional feed metadata (source is already included from fetch_articles_from_feed)
    for article in articles:
        article["source_feed"] = feed_name  # Keep for backward compatibility
        article["source_url"] = feed["url"]
    
    return articles
    
    return articles
