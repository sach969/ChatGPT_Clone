from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship,DeclarativeBase
from pgvector.sqlalchemy import Vector
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String,nullable=False)
    sessions = relationship("Session",back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    user = relationship("User", back_populates="sessions")
    chats = relationship("Chat", back_populates="session")


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    content = Column(Text,nullable=False)
    embedding = Column(Vector(768))
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    session = relationship("Session", back_populates="chats")