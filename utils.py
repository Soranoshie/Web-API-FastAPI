from sqlalchemy.orm import Session
from models.user_model import User


def get_user_data_by_name(db: Session, username: str):
    user = db.query(User).filter_by(name=username).first()
    return user
