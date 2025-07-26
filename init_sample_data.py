"""
Sample data initialization script for development and testing.
Run this to populate the app with example feeds and data.
"""
import json
from pathlib import Path

def initialize_sample_data():
    """Initialize sample data for development."""
    
    # Sample RSS feeds
    sample_feeds = [
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/tag/artificial-intelligence/feed/"
        },
        {
            "name": "AI News",
            "url": "https://artificialintelligence-news.com/feed/"
        },
        {
            "name": "MIT Technology Review",
            "url": "https://www.technologyreview.com/feed/"
        }
    ]
    
    # Sample subscribers
    sample_subscribers = [
        "demo@example.com",
        "test@trivance.ai",
        "subscriber@techblog.com"
    ]
    
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Write sample data
    with open(data_dir / "feeds.json", "w") as f:
        json.dump(sample_feeds, f, indent=2)
    
    with open(data_dir / "subscribers.json", "w") as f:
        json.dump(sample_subscribers, f, indent=2)
    
    # Initialize empty posts file
    with open(data_dir / "posts.json", "w") as f:
        json.dump([], f, indent=2)
    
    print("✅ Sample data initialized successfully!")
    print(f"   - {len(sample_feeds)} sample feeds added")
    print(f"   - {len(sample_subscribers)} sample subscribers added")
    print("   - Empty posts.json created")
    print("\nTo use your own data, simply delete the files in the data/ directory")
    print("and the app will start fresh on the next run.")

if __name__ == "__main__":
    initialize_sample_data()
