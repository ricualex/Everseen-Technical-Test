from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
import json

app = FastAPI()

class PayloadModel(BaseModel):
    status: str
    type: int
    hash: str

def log_error(message: str, payload: PayloadModel):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f%z')
    payload_dict = payload.dict()
    log_entry = f"{timestamp} ERROR: [ eReceiver ] {message}: {json.dumps(payload_dict)}\n"
    log_file_path = "/home/ricu/Desktop/everseen/ereceiver-service.log"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)

@app.post("/api/v1/data")
async def receive_data(payload: PayloadModel):
    status = payload.status
    type_ = payload.type
    hash_ = payload.hash

    if status not in {"complete", "incomplete", "cancelled"}:
        log_error("Input data is not valid", payload)
        raise HTTPException(status_code=500, detail="Input data is not valid")

    if type_ not in {1, 2, 5, 11}:
        log_error("Input data is not valid", payload)
        raise HTTPException(status_code=500, detail="Input data is not valid")

    if not (isinstance(hash_, str) and len(hash_) == 32 and all(c in "0123456789abcdef" for c in hash_)):
        log_error("Input data is not valid", payload)
        raise HTTPException(status_code=500, detail="Input data is not valid")

    return {"message": "Valid payload"}
