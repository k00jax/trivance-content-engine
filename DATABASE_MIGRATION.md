# Database Migration Guide

This document outlines the process for migrating from JSON file storage to a proper database system (SQLite, PostgreSQL, Supabase, etc.).

## Current JSON Schema

### feeds.json
```json
[
  {
    "name": "string",
    "url": "string"
  }
]
```

### subscribers.json
```json
[
  "email1@example.com",
  "email2@example.com"
]
```

### posts.json
```json
[
  {
    "id": "ISO timestamp string",
    "title": "string",
    "summary": "string", 
    "source": "string",
    "link": "string",
    "generated_content": "string",
    "created_at": "ISO timestamp string",
    "timestamp": "unix timestamp number"
  }
]
```

## Database Migration Steps

### 1. Choose Database System
- **SQLite**: For single-user, local deployments
- **PostgreSQL**: For multi-user, production deployments  
- **Supabase**: For hosted solution with real-time features

### 2. Create Database Schema
```sql
-- Example SQLite/PostgreSQL schema
CREATE TABLE feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE posts (
    id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    source VARCHAR(255),
    link TEXT,
    generated_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Update persistence.py
Replace JSON functions with database calls:

```python
from sqlalchemy import create_engine, text
# or: from supabase import create_client

class DatabasePersistence:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    
    def save_feed(self, name, url):
        with self.engine.connect() as conn:
            conn.execute(text(
                "INSERT INTO feeds (name, url) VALUES (:name, :url)"
            ), {"name": name, "url": url})
    
    def load_feeds(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name, url FROM feeds"))
            return [{"name": row[0], "url": row[1]} for row in result]
    
    # Similar methods for subscribers and posts...
```

### 4. Migration Script
Create a migration script to transfer existing JSON data:

```python
def migrate_json_to_db():
    # Load existing JSON data
    feeds = load_json("feeds.json", [])
    subscribers = load_json("subscribers.json", [])
    posts = load_json("posts.json", [])
    
    # Create database persistence instance
    db = DatabasePersistence("sqlite:///data/trivance.db")
    
    # Migrate data
    for feed in feeds:
        db.save_feed(feed["name"], feed["url"])
    
    for email in subscribers:
        db.save_subscriber(email)
    
    for post in posts:
        db.save_post(**post)
    
    print("Migration completed successfully!")
```

### 5. Update Service Layer
Modify service files to use the new persistence layer:

```python
# app/services/rss.py
from .persistence import DatabasePersistence

db = DatabasePersistence(os.getenv("DATABASE_URL"))

def add_feed(feed):
    db.save_feed(feed.name, feed.url)
    return {"message": "Feed added"}

def get_all_feeds():
    return db.load_feeds()
```

### 6. Environment Configuration
Add database configuration to environment:

```bash
# .env file
DATABASE_URL=sqlite:///data/trivance.db
# or for PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost/trivance
# or for Supabase:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key
```

### 7. Add Database Dependencies
Update requirements.txt:
```
sqlalchemy>=2.0.0
alembic>=1.13.0
# For PostgreSQL:
# psycopg2-binary>=2.9.0
# For Supabase:
# supabase>=2.0.0
```

## Testing Migration

1. Backup current JSON files
2. Run migration script
3. Test all CRUD operations
4. Verify data integrity
5. Update deployment scripts

## Rollback Plan

Keep JSON files as backup during migration. The current `persistence.py` module provides a clean interface that makes switching between storage backends straightforward.
