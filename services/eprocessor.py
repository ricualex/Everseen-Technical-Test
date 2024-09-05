from fastapi import FastAPI, HTTPException
from data.cloud_event import CloudEvent
from contextlib import asynccontextmanager
from utils.utils import subscribe
import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await subscribe(name="eprocessor", url="http://127.0.0.1:8083/api/v1/notification")
    yield
    
app = FastAPI(lifespan=lifespan)

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.post("/api/v1/notification")
async def receive_subscription(cloud_event: CloudEvent):
    hash_key = cloud_event.data.hash
    entry_type = cloud_event.data.type
    status = cloud_event.data.status
    update_or_create_entry(redis_conn, hash_key, entry_type, status)
    return {"message": "Received event!"}


def update_or_create_entry(redis_conn, hash_key, entry_type, status):
    if redis_conn.exists(hash_key):
        redis_conn.hset(hash_key, mapping={'type': entry_type, 'status': status})
    else:
        redis_conn.hset(hash_key, mapping={'type': entry_type, 'status': status})