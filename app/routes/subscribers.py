from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.subscribers import add_subscriber, list_subscribers

router = APIRouter()

class SubscriberInput(BaseModel):
    email: str

@router.post("/")
def subscribe(subscriber: SubscriberInput):
    return add_subscriber(subscriber.email)

@router.get("/")
def get_subscribers():
    return list_subscribers()
