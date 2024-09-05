from data.data_event import DataEvent
from pydantic import BaseModel


class CloudEvent(BaseModel):
    specversion: str
    type: str
    source: str
    subject: str
    id: str
    time: str
    datacontenttype: str
    data: DataEvent