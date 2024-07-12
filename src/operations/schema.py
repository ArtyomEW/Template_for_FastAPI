from pydantic import BaseModel

from datetime import datetime


class OperationAdd(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

