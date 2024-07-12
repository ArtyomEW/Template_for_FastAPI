from datetime import datetime
from sqlalchemy import Integer, String, TIMESTAMP, Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP, default=datetime.utcnow())
    type = Column(String)
