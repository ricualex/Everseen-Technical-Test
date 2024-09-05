from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from data.cloud_event import CloudEvent

import json
from httpx import AsyncClient, RequestError
from utils.utils import data_broker_url



app = FastAPI()

class PayloadModel(BaseModel):
    status: str
    type: int
    hash: str

def log_error(message: str, payload: PayloadModel):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f%z')
    payload_dict = payload.model_dump_json()
    log_entry = f"{timestamp} ERROR: [ eReceiver ] {message}: {json.dumps(payload_dict)}\n"
    log_file_path = "log/ereceiver-service.log"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)

@app.post("/api/v1/data")
async def receive_data(payload: PayloadModel):
    status = payload.status
    _type = payload.type
    _hash = payload.hash

    if status not in {"complete", "incomplete", "cancelled"}:
        log_error("Input data is not valid", payload)
        raise HTTPException(status_code=500, detail="Input data is not valid")

    if _type not in {1, 2, 5, 11}:
        log_error("Input data is not valid", payload)
        raise HTTPException(status_code=500, detail="Input data is not valid")

    if not (isinstance(_hash, str) and len(_hash) == 32 and all(c in "0123456789abcdef" for c in _hash)):
        log_error("Input data is not valid", payload)
        raise HTTPException(status_code=500, detail="Input data is not valid")
    
    async with AsyncClient() as client:
        subscriber = {
            "url": "http://127.0.0.1:8080/api/v1/notification",
            "name": "ereceiver"
        }
        try:
            response = await client.post(data_broker_url + "/subscribe", json=subscriber)
            response.raise_for_status()
        except RequestError as e:
            await log_error(f"Error subscribing: {e}", payload)
            raise HTTPException(status_code=500, detail="Subscription failed")

        data = {
            "source": "ereceiver", 
            "status": status,
            "type": _type,
            "hash": _hash
        }
        try:
            response = await client.post(data_broker_url + "/publish", json=data)
            response.raise_for_status()
        except RequestError as e:
            await log_error(f"Error publishing data: {e}", payload)
            raise HTTPException(status_code=500, detail="Publishing failed")

    return {"message": "Valid payload"}
    
@app.post("/api/v1/notification")
async def receive_subscription(cloud_event: CloudEvent):
    return {"message": "Received event!"}
