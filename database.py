from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from settings import settings

engine = create_engine(url=settings.SQL_CONNECTION_URI, pool_pre_ping=True, echo=settings.SQL_DEBUG_ENABLED)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_session() -> Session:
    return SessionLocal()
