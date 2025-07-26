from .persistence import save_json, load_json

# Load subscribers from persistent storage on startup
subscribers_db = load_json("subscribers.json", [])

def add_subscriber(email: str):
    global subscribers_db
    if email not in subscribers_db:
        subscribers_db.append(email)
        save_json("subscribers.json", subscribers_db)
        return {"message": "Subscribed!", "total": len(subscribers_db)}
    return {"message": "Already subscribed."}

def list_subscribers():
    return subscribers_db
