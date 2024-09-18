from sqlalchemy.orm import Session
from database import create_session


def get_session() -> Session:
    db = create_session()
    try:
        yield db
    finally:
        db.close()
