from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    create_event, get_events, get_event, update_event, delete_event,
    create_user, get_users, get_user, update_user, delete_user
)

router_websocket = APIRouter()
router_events = APIRouter(prefix='/events', tags=['event'])
router_users = APIRouter(prefix='/users', tags=['user'])


# WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


# Events
@router_events.post("/", response_model=schemas.Event)
async def create_event_route(event_data: schemas.EventCreate, db: Session = Depends(get_db)):
    event = create_event(db, event_data)
    await notify_clients(f"Event added: {event.name}")
    return event


@router_events.get("/", response_model=List[schemas.Event])
async def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = get_events(db, skip=skip, limit=limit)
    return events


@router_events.get("/{event_id}", response_model=schemas.Event)
async def read_event(event_id: int, db: Session = Depends(get_db)):
    event = get_event(db, event_id)
    return event


@router_events.patch("/{event_id}", response_model=schemas.Event)
async def update_event_route(event_id: int, event_data: schemas.EventUpdate, db: Session = Depends(get_db)):
    updated_event = update_event(db, event_id, event_data)
    if updated_event:
        await notify_clients(f"Event updated: {updated_event.name}")
        return updated_event
    return {"message": "Event not found"}


@router_events.delete("/{event_id}")
async def delete_event_route(event_id: int, db: Session = Depends(get_db)):
    deleted = delete_event(db, event_id)
    if deleted:
        await notify_clients(f"Event deleted: ID {event_id}")
        return {"message": "Event deleted"}
    return {"message": "Event not found"}


# Users
@router_users.post("/", response_model=schemas.User)
async def create_user_route(schema: schemas.UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, schema)
    await notify_clients(f"User added: {user.name}")
    return user


@router_users.get("/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router_users.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user


@router_users.patch("/{user_id}")
async def update_user_route(user_id: int, schema: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, schema)
    if updated_user:
        await notify_clients(f"User updated: {updated_user.name}")
        return updated_user
    return {"message": "User not found"}


@router_users.delete("/{user_id}")
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if deleted:
        await notify_clients(f"User deleted: ID {user_id}")
        return {"message": "User deleted"}
    return {"message": "User not found"}

