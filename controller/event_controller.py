from sqlalchemy.orm import Session
from schemas import event_schema
from my_models.event_model import Event


def create_event(db: Session, schema: event_schema.EventCreate):
    db_event = Event(**schema.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int):
    return db.query(Event).filter_by(id=event_id).first()


def update_event(db: Session, event_id: int, event_data: event_schema.EventUpdate | dict):
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
