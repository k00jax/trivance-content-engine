#!/usr/bin/env python3

"""
Quick test to demonstrate the new UI behavior
"""

# Mock data similar to what the API would return
mock_articles = [
    {
        "title": "AI Breakthrough in Drug Discovery",
        "summary": "Recent advances in artificial intelligence...",
        "score": 8.5,
        "source_feed": "BioPharma News",
        "link": "https://example.com/ai-drug",
        "published": "2025-01-26"
    },
    {
        "title": "Market Analysis: Q4 Earnings",
        "summary": "Companies report strong quarterly results...",
        "score": 7.2,
        "source_feed": "Financial Times",
        "link": "https://example.com/earnings",
        "published": "2025-01-26"
    },
    {
        "title": "New FDA Regulations Announced",
        "summary": "The FDA has introduced new guidelines...",
        "score": 6.8,
        "source_feed": "BioPharma News",
        "link": "https://example.com/fda-regs",
        "published": "2025-01-25"
    },
    {
        "title": "Tech Stocks Rally Continues",
        "summary": "Technology sector shows strong performance...",
        "score": 9.1,
        "source_feed": "Financial Times",
        "link": "https://example.com/tech-rally",
        "published": "2025-01-26"
    },
    {
        "title": "Clinical Trial Results Published",
        "summary": "Phase III trial shows promising outcomes...",
        "score": 7.9,
        "source_feed": "BioPharma News",
        "link": "https://example.com/clinical-trial",
        "published": "2025-01-25"
    }
]

def simulate_ui_grouping(articles):
    """Simulate how the UI will group and display articles"""
    print("🎯 CHOOSE MOST RELEVANT ARTICLE")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    # Find most relevant
    best_article = max(articles, key=lambda x: x["score"])
    print(f"Most relevant: {best_article['title']} (Score: {best_article['score']})")
    print()
    
    # Group by source
    articles_by_source = {}
    for article in articles:
        source = article["source_feed"]
        if source not in articles_by_source:
            articles_by_source[source] = []
        articles_by_source[source].append(article)
    
    # Display grouped articles
    print("📋 Available Articles")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    for source, source_articles in articles_by_source.items():
        print(f"**{source}**")
        
        # Sort by score and take top 3
        top_articles = sorted(source_articles, key=lambda x: x["score"], reverse=True)[:3]
        
        for article in top_articles:
            title = article["title"]
            score = article["score"]
            
            # Simulate button display
            display_title = title if len(title) <= 60 else title[:57] + "..."
            print(f"  📄 {display_title} (Score: {score})")
        
        print()

if __name__ == "__main__":
    print("✅ New UI Article Selection Demo")
    print("="*50)
    print()
    simulate_ui_grouping(mock_articles)
