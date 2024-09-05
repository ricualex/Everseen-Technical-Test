from fastapi import FastAPI, HTTPException, Request
from typing import List
from data.subscriber import Subscriber
from data.cloud_event import CloudEvent
from data.data_event import DataEvent
from datetime import datetime, timezone
from httpx import AsyncClient, RequestError
from utils.utils import _generate_id, _get_current_time


app = FastAPI()

spec_version = "1.0"
type="com.evertest.event"

cache: List[CloudEvent] = []

subscribers: List[Subscriber] = []

@app.get("/cache/{id}")
async def get_cache(id: str):
    for elem in cache:
        if elem.id == id:
            return elem
        else:
            raise HTTPException(status_code=404, detail="Object not found")

@app.post("/api/publish")
async def publish_cloud_event(request: Request):
    try:                
        body = await request.json()
        print(f"Received body: {body}")
        source = body.get("source")
        id = _generate_id()
        current_date_time = _get_current_time()
        data_event = DataEvent(status=body.get("status"), type=body.get("type"), hash=body.get("hash"))
        cloud_event_object = CloudEvent(specversion=spec_version, 
                                        type=type, 
                                        source=source, 
                                        subject="DATA", 
                                        id=id,
                                        time=current_date_time,
                                        datacontenttype="application/json",
                                        data=data_event
                                        )
        cache.append(cloud_event_object)
        await notify_subscribers(cloud_event=cloud_event_object)
        return {"message": f"Published successfuly"}
    except Exception as e:
        print(f"Error in /api/publish: {e}")
        raise HTTPException(status_code=500, detail="Failed to publish event")

@app.get("/cache/get_all")
async def get_all_cache():
    return cache

@app.post("/api/subscribe")
async def subscribe(request: Request):
    body = await request.json()
    subscriber_name = body.get("name")
    subscriber_url = body.get("url")
    if subscriber_url and subscriber_name and subscriber_url not in subscribers:
        subscribers.append(Subscriber(name=subscriber_name, url=subscriber_url))
        return {"message": f"Subscribed successfully: {subscriber_url}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or duplicate subscription URL")

async def notify_subscribers(cloud_event: CloudEvent):
    async with AsyncClient() as client:
        for subscriber in subscribers:
            try:
                cloud_event_dict = cloud_event.model_dump()
                response = await client.post(subscriber.url, json=cloud_event_dict)
                response.raise_for_status()
            except RequestError as e:
                print(f"Error notifying subscriber: {subscriber.url}: {e}")
