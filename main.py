from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="E-Portal API", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
faces = []
users = []
visits = []

@app.get("/")
def root():
    return {
        "message": "Welcome to E-Portal",
        "version": "1.0.0",
        "endpoints": {
            "faces": "/api/faces",
            "users": "/api/users",
            "visits": "/api/visits",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# FACES ENDPOINTS
@app.get("/api/faces")
def get_faces():
    return {"faces": faces, "count": len(faces)}

@app.post("/api/faces")
def add_face(name: str, description: str = ""):
    face = {
        "id": len(faces) + 1,
        "name": name,
        "description": description
    }
    faces.append(face)
    return {"status": "success", "face": face}

@app.get("/api/faces/{face_id}")
def get_face(face_id: int):
    for face in faces:
        if face["id"] == face_id:
            return face
    return {"error": "Face not found"}

@app.delete("/api/faces/{face_id}")
def delete_face(face_id: int):
    global faces
    faces = [f for f in faces if f["id"] != face_id]
    return {"status": "deleted"}

# USERS ENDPOINTS
@app.get("/api/users")
def get_users():
    return {"users": users, "count": len(users)}

@app.post("/api/users")
def add_user(username: str, email: str):
    user = {
        "id": len(users) + 1,
        "username": username,
        "email": email
    }
    users.append(user)
    return {"status": "success", "user": user}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}

# VISITS ENDPOINTS
@app.get("/api/visits")
def get_visits():
    return {"visits": visits, "count": len(visits)}

@app.post("/api/visits")
def add_visit(user_id: int, face_id: int):
    visit = {
        "id": len(visits) + 1,
        "user_id": user_id,
        "face_id": face_id
    }
    visits.append(visit)
    return {"status": "success", "visit": visit}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
