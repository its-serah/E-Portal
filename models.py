"""
SQLAlchemy models for the face recognition system.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary
from sqlalchemy.sql import func
from database import Base
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """User model for authentication."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def set_password(self, password: str):
        """Hash and set the user's password."""
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches the stored hash."""
        return pwd_context.verify(password, self.hashed_password)


class Face(Base):
    """Face model for storing recognized faces."""
    
    __tablename__ = "faces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    image = Column(String(500), nullable=False)  # Path to image file
    is_allowed = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Visit(Base):
    """Visit model for tracking face detection events."""
    
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(Integer, nullable=True)  # Null if unknown person
    person_name = Column(String(100), nullable=False)
    confidence = Column(String(50))
    is_allowed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
