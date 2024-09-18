from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, Float
from database import Base


class Notification(Base):
    __tablename__ = "notifications"
    email = Column(String(128), primary_key=True, unique=True, index=True, nullable=False)
    device = Column(String(128), nullable=False)
    last = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow())


class Device(Base):
    __tablename__ = "devices"
    id = Column(String(128), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    disabled = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow())


class Reading(Base):
    __tablename__ = "readings"
    id = Column(String(128), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    device = Column(String(128), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow())
