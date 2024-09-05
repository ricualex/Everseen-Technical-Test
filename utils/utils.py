from datetime import datetime, timezone
import uuid

from fastapi import HTTPException
from httpx import AsyncClient, RequestError
from datetime import datetime, timezone

ereceiver_url = "http://0.0.0.0:8080/api"
data_broker_url = "http://0.0.0.0:8081/api"
evalidator_url = "http://0.0.0.0:8082/api"
eprocessor_url = "http://0.0.0.0:8083/api"

eprocessor_notification_api_url = "http://0.0.0.0:8083/api/v1/notification"
ereceiver_notification_api_url = "http://0.0.0.0:8080/api/v1/notification"
evalidator_notification_api_url = "http://0.0.0.0:8082/api/v1/notification"

spec_version = "1.0"
event_type = "com.evertest.event"


def _get_spec_version():
    return spec_version

def _get_event_type():
    return event_type

def _generate_id() -> str:
    return str(uuid.uuid4())

def _get_current_time() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")

async def subscribe(name: str, url: str):
    async with AsyncClient() as client:
        subscriber = {
            "url": url,
            "name": name
        }
        try:
            response = await client.post(data_broker_url + "/subscribe", json=subscriber)
            response.raise_for_status()
            print("Subscribed successfully!")
        except RequestError as e:
            raise HTTPException(status_code=500, detail="Subscription failed")
