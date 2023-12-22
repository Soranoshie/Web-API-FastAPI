from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Event
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


# User
class UserBase(BaseModel):
    name: str
    event_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None
    event_id: Optional[int] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
