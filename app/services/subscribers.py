subscribers_db = []

def add_subscriber(email: str):
    if email not in subscribers_db:
        subscribers_db.append(email)
        return {"message": "Subscribed!", "total": len(subscribers_db)}
    return {"message": "Already subscribed."}

def list_subscribers():
    return subscribers_db
