from sqlalchemy.orm import Session

import schemas
from models import Event, User


# Event
def create_event(db: Session, schema: schemas.EventCreate):
    db_event = Event(**schema.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int):
    return db.query(Event).filter_by(id=event_id).first()


def update_event(db: Session, event_id: int, event_data: schemas.EventUpdate | dict):
    db_event = db.query(Event).filter_by(id=event_id).first()

    event_data = event_data if isinstance(event_data, dict) else event_data.model_dump()

    if db_event:
        for key, value in event_data.items():
            if hasattr(db_event, key):
                setattr(db_event, key, value)

        db.commit()
        db.refresh(db_event)

    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False


# User
def create_user(db: Session, schema: schemas.UserCreate):
    db_user = User(**schema.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).first()


def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate | dict):
    db_user = db.query(User).filter_by(id=user_id).first()

    user_data = user_data if isinstance(user_data, dict) else user_data.model_dump()

    if db_user:
        for key, value in user_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter_by(id=user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
