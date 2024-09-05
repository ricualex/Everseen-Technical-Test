from fastapi import FastAPI, HTTPException
from typing import Dict, List
from data.cloud_event import CloudEvent
from data.cloud_error_object import CloudEventError
from data.data_event import DataEvent
from contextlib import asynccontextmanager
from httpx import AsyncClient, RequestError
from collections import defaultdict
from datetime import datetime, timezone
from utils.utils import _generate_id, _get_current_time, _get_spec_version, _get_event_type, subscribe, data_broker_url
import os
import threading
import time


incoming_cloud_events_hash = []
incoming_cloud_events = []

hash_sums: Dict[str, int] = defaultdict(int)
hash_events: Dict[str, List[CloudEvent]] = defaultdict(list)

def log_error(message: str, data: List[str]):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f%z')
    log_entry = f"{timestamp} ERROR: [ eValidator ] {message}: {data}\n"
    log_file_path = "log/evalidator-service.log"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await subscribe(name="evalidator", url="http://127.0.0.1:8082/api/v1/notification")
    yield
    
app = FastAPI(lifespan=lifespan)

delay = int(os.getenv("VALIDATION_WINDOW_MS", 30))

lock = threading.Lock()

def compare_hash(cloud_event: CloudEvent):
    with lock:
        print(f"Received object and comparing...")
        hash_value = cloud_event.data.hash
        type_value = int(cloud_event.data.type)
        
        if hash_value in incoming_cloud_events_hash:
            if hash_sums[hash_value] > 10:
                print(f"Hash '{hash_value}' has a total type sum greater than 10:")
                error_id = _generate_id()
                error_time = _get_current_time()
                spec_version = _get_spec_version()
                event_type = _get_event_type()
                error_data: List[str] = []
                for event in hash_events[hash_value]:
                    error_data.append(event.data.model_dump_json())
                cloud_event_error = CloudEventError(
                    specversion=spec_version,
                    type=event_type,
                    source="evalidator",
                    subject="ERROR",
                    id=error_id,
                    time=error_time,
                    datacontenttype="application/json",
                    data=error_data
                    )
                log_error(message="Objects data.type sum is greater than 10", data=error_data)
        else:
            print(f"Hash not found, taking no action...")
            incoming_cloud_events.append(cloud_event)
            incoming_cloud_events_hash.append(hash_value)
        
        hash_sums[hash_value] += type_value
        hash_events[hash_value].append(cloud_event)

def reset_list():
    while True:
        time.sleep(delay)
        with lock:
            print("Clearing the list...")
            incoming_cloud_events.clear()
            incoming_cloud_events_hash.clear()
            hash_sums.clear()
            hash_events.clear()

reset_thread = threading.Thread(target=reset_list, daemon=True)
reset_thread.start()

def process_incoming_string(cloud_event: CloudEvent):
    compare_hash(cloud_event)

@app.post("/api/v1/notification")
async def receive_subscription(cloud_event: CloudEvent):
    process_incoming_string(cloud_event)
    return {"message": "Received event!"}
