from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import feeds, posts, subscribers
from app.services.scheduler import start_scheduler

# Load environment variables from .env file
load_dotenv()
start_scheduler()  # Uncomment to activate scheduling on app start

app = FastAPI(title="Trivance Content Engine")

app.include_router(feeds.router, prefix="/feeds", tags=["Feeds"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(subscribers.router, prefix="/subscribers", tags=["Subscribers"])
