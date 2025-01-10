from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    nickname = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
