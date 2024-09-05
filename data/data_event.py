from pydantic import BaseModel



class DataEvent(BaseModel):
    status: str
    type: int
    hash: str

