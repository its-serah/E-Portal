"""
Pydantic schemas for request and response validation.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str
    password2: str
    
    @field_validator('password')
    @classmethod
    def password_length(cls, v):
        """Validate password minimum length."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @field_validator('password2')
    @classmethod
    def passwords_match(cls, v, info):
        """Validate that both passwords match."""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: int
    username: str


# Face Schemas
class FaceBase(BaseModel):
    """Base face schema."""
    name: str
    is_allowed: bool = True


class FaceCreate(FaceBase):
    """Schema for creating a face."""
    pass


class FaceUpdate(FaceBase):
    """Schema for updating a face."""
    pass


class FaceResponse(FaceBase):
    """Schema for face response."""
    id: int
    image: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FaceListResponse(BaseModel):
    """Schema for face list response."""
    faces: list[FaceResponse]
    total: int


class RecognitionResult(BaseModel):
    """Schema for face recognition result."""
    id: Optional[int] = None
    name: str
    filename: Optional[str] = None
    confidence: float
    box: list[int]  # [x1, y1, x2, y2]
    is_allowed: bool
    error: Optional[str] = None


class RecognitionResponse(BaseModel):
    """Schema for face recognition API response."""
    status: str
    recognized_people: list[RecognitionResult]
    people_count: int
