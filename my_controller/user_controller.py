from sqlalchemy.orm import Session
from my_schemas import user_schema
from my_models.user_model import User


def create_user(db: Session, schema: user_schema.UserCreate):
    db_user = User(**schema.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).first()


def update_user(db: Session, user_id: int, user_data: user_schema.UserUpdate | dict):
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
