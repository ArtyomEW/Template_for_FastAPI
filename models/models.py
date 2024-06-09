from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Column, JSON
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase): pass
class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer,  ForeignKey('role.id'))




