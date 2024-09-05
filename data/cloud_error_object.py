from pydantic import BaseModel
from typing import List


class CloudEventError(BaseModel):
    specversion: str
    type: str
    source: str
    subject: str
    id: str
    time: str
    datacontenttype: str
    data: List[str]