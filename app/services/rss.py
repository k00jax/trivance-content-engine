feeds_db = []

def add_feed(feed):
    feeds_db.append({"name": feed.name, "url": feed.url})
    return {"message": "Feed added", "total": len(feeds_db)}

def get_all_feeds():
    return feeds_db

def remove_feed(name: str):
    global feeds_db
    feeds_db = [f for f in feeds_db if f["name"] != name]
    return {"message": f"Feed '{name}' removed."}
