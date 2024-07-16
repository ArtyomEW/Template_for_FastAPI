from datetime import datetime
from sqlalchemy import Integer, String, TIMESTAMP, Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass


class Message(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    message = Column(String)

