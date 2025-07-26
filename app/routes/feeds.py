from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.rss import add_feed, get_all_feeds

router = APIRouter()

class FeedInput(BaseModel):
    name: str
    url: str

@router.post("/")
def create_feed(feed: FeedInput):
    return add_feed(feed)

@router.get("/")
def list_feeds():
    return get_all_feeds()


@router.delete("/")
def delete_feed(name: str):
    from app.services.rss import remove_feed
    return remove_feed(name)
