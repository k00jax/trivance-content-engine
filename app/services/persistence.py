"""
Data persistence utilities for local JSON storage.
Future-ready for migration to Supabase or SQLite.
"""
import json
import os
from pathlib import Path
from typing import Any, List, Dict

# Define data directory path
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_json(filepath: str, data: Any) -> None:
    """Save data to JSON file with proper error handling."""
    try:
        full_path = DATA_DIR / filepath
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")

def load_json(filepath: str, default: Any = None) -> Any:
    """Load data from JSON file with fallback to default."""
    try:
        full_path = DATA_DIR / filepath
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default if default is not None else []
    except Exception as e:
        print(f"Error loading from {filepath}: {e}")
        return default if default is not None else []

def append_to_json(filepath: str, new_item: Dict) -> None:
    """Append new item to JSON array file."""
    try:
        data = load_json(filepath, [])
        data.append(new_item)
        save_json(filepath, data)
    except Exception as e:
        print(f"Error appending to {filepath}: {e}")

# Future-ready database integration stubs
class DatabaseInterface:
    """
    Interface for future database integration (Supabase/SQLite).
    
    To migrate from JSON to database:
    1. Implement these methods with actual DB calls
    2. Replace persistence calls in services
    3. Add connection management and migrations
    """
    
    def save_feeds(self, feeds: List[Dict]) -> None:
        """Future: Save feeds to database table."""
        pass
    
    def load_feeds(self) -> List[Dict]:
        """Future: Load feeds from database table."""
        pass
    
    def save_subscribers(self, subscribers: List[str]) -> None:
        """Future: Save subscribers to database table."""
        pass
    
    def load_subscribers(self) -> List[str]:
        """Future: Load subscribers from database table."""
        pass
    
    def save_post(self, post: Dict) -> None:
        """Future: Save generated post to database table."""
        pass
    
    def load_posts(self) -> List[Dict]:
        """Future: Load posts from database table."""
        pass
