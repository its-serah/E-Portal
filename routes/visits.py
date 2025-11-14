"""
Visit tracking routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Visit

router = APIRouter(prefix="/api/visits", tags=["visits"])


@router.get("/")
def list_visits(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent visits."""
    visits = db.query(Visit).order_by(Visit.timestamp.desc()).limit(limit).all()
    unknown_count = db.query(func.count(Visit.id)).filter(Visit.face_id == None).scalar()
    
    return {
        "visits": [
            {
                "id": v.id,
                "face_id": v.face_id,
                "person_name": v.person_name,
                "confidence": v.confidence,
                "is_allowed": v.is_allowed,
                "timestamp": v.timestamp
            }
            for v in visits
        ],
        "total": len(visits),
        "unknown_count": unknown_count or 0
    }
