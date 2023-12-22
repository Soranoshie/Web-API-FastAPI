from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    name: Optional[str] = None


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
