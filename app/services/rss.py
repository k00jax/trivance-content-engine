feeds_db = []

def add_feed(feed):
    feeds_db.append({"name": feed.name, "url": feed.url})
    return {"message": "Feed added", "total": len(feeds_db)}

def get_all_feeds():
    return feeds_db
