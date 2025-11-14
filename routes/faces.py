"""
Face recognition and face management routes with REAL detection.
"""

import os
import cv2
import numpy as np
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form
from sqlalchemy.orm import Session
from ultralytics import YOLO
from deepface import DeepFace

from database import get_db
from models import User, Face, Visit
from schemas import FaceResponse, FaceListResponse, RecognitionResponse, RecognitionResult
from auth import get_current_user
from config import settings

router = APIRouter(prefix="/api/faces", tags=["faces"])

AVAILABLE_MODELS = {
    "yolov8n": "yolov8n.pt",
    "yolov8m": "yolov8m.pt",
    "yolov8n-face": "yolov8n-face.pt",
    "yolov8m-face": "yolov8m-face.pt",
    "yolov8l-face": "yolov8l-face.pt",
    "yolov10s-face": "yolov10s-face.pt",
    "yolov11m-face": "yolov11m-face.pt",
    "yolov11l-face": "yolov11l-face.pt",
}


@router.post("/detect", response_model=RecognitionResponse)
async def detect_faces(
    image: UploadFile = File(...),
    model: str = Form(default="yolov8n"),
    db: Session = Depends(get_db)
):
    """Detect and recognize faces in uploaded image."""
    try:
        model_path = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS["yolov8n"])
        
        contents = await image.read()
        np_img = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image")
        
        yolo_model = YOLO(model_path)
        results = yolo_model(img)
        recognized_people = []
        
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        temp_path = os.path.join(settings.MEDIA_ROOT, "temp_detection.jpg")
        cv2.imwrite(temp_path, img)
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                face_img = img[y1:y2, x1:x2]
                
                try:
                    faces_dir = os.path.join(settings.MEDIA_ROOT, "faces")
                    os.makedirs(faces_dir, exist_ok=True)
                    
                    df_results = DeepFace.find(
                        face_img, 
                        db_path=faces_dir, 
                        model_name="Facenet"
                    )
                    
                    if df_results and len(df_results) > 0 and len(df_results[0]) > 0:
                        best_match = df_results[0].iloc[0]
                        face_path = best_match["identity"]
                        filename = os.path.basename(face_path)
                        
                        face_obj = db.query(Face).filter(Face.image.contains(filename)).first()
                        
                        if face_obj:
                            person_data = RecognitionResult(
                                id=face_obj.id,
                                name=face_obj.name,
                                filename=f"/media/faces/{filename}",
                                confidence=float(best_match["distance"]),
                                box=[int(x1), int(y1), int(x2), int(y2)],
                                is_allowed=face_obj.is_allowed
                            )
                            # Log visit
                            visit = Visit(
                                face_id=face_obj.id,
                                person_name=face_obj.name,
                                confidence=f"{100*(1-float(best_match['distance'])):.1f}%",
                                is_allowed=face_obj.is_allowed
                            )
                            db.add(visit)
                            db.commit()
                        else:
                            person_data = RecognitionResult(
                                name="Unknown (Match found but not in database)",
                                filename=f"/media/faces/{filename}",
                                confidence=float(best_match["distance"]),
                                box=[int(x1), int(y1), int(x2), int(y2)],
                                is_allowed=False
                            )
                        recognized_people.append(person_data)
                    else:
                        person_data = RecognitionResult(
                            name="Unknown",
                            confidence=1.0,
                            box=[int(x1), int(y1), int(x2), int(y2)],
                            is_allowed=False
                        )
                        recognized_people.append(person_data)
                        # Log unknown visit
                        visit = Visit(
                            face_id=None,
                            person_name="Unknown",
                            confidence="N/A",
                            is_allowed=False
                        )
                        db.add(visit)
                        db.commit()
                
                except Exception as e:
                    person_data = RecognitionResult(
                        name="Error",
                        confidence=0.0,
                        box=[int(x1), int(y1), int(x2), int(y2)],
                        is_allowed=False,
                        error=str(e)
                    )
                    recognized_people.append(person_data)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return RecognitionResponse(
            status="success",
            recognized_people=recognized_people,
            people_count=len(recognized_people)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/", response_model=FaceListResponse)
def list_faces(db: Session = Depends(get_db)):
    """Get all stored faces."""
    faces = db.query(Face).all()
    return FaceListResponse(faces=faces, total=len(faces))


@router.post("/", response_model=FaceResponse, status_code=201)
async def create_face(
    name: str = Form(...),
    is_allowed: bool = Form(default=True),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Add a new face."""
    try:
        faces_dir = os.path.join(settings.MEDIA_ROOT, "faces")
        os.makedirs(faces_dir, exist_ok=True)
        
        filename = f"{name}_{image.filename}"
        file_path = os.path.join(faces_dir, filename)
        
        contents = await image.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        new_face = Face(name=name, image=f"faces/{filename}", is_allowed=is_allowed)
        db.add(new_face)
        db.commit()
        db.refresh(new_face)
        
        return new_face
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{face_id}", response_model=FaceResponse)
def get_face(face_id: int, db: Session = Depends(get_db)):
    """Get a specific face."""
    face = db.query(Face).filter(Face.id == face_id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Face not found")
    return face


@router.put("/{face_id}", response_model=FaceResponse)
async def update_face(
    face_id: int,
    name: Optional[str] = Form(None),
    is_allowed: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Update a face."""
    face = db.query(Face).filter(Face.id == face_id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Face not found")
    
    try:
        if name:
            face.name = name
        if is_allowed is not None:
            face.is_allowed = is_allowed
        
        if image:
            faces_dir = os.path.join(settings.MEDIA_ROOT, "faces")
            os.makedirs(faces_dir, exist_ok=True)
            
            old_path = os.path.join(settings.MEDIA_ROOT, face.image)
            if os.path.exists(old_path):
                os.remove(old_path)
            
            filename = f"{face.name}_{image.filename}"
            file_path = os.path.join(faces_dir, filename)
            
            contents = await image.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            
            face.image = f"faces/{filename}"
        
        db.commit()
        db.refresh(face)
        return face
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{face_id}", status_code=204)
def delete_face(face_id: int, db: Session = Depends(get_db)):
    """Delete a face."""
    face = db.query(Face).filter(Face.id == face_id).first()
    if not face:
        raise HTTPException(status_code=404, detail="Face not found")
    
    try:
        image_path = os.path.join(settings.MEDIA_ROOT, face.image)
        if os.path.exists(image_path):
            os.remove(image_path)
        
        db.delete(face)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
