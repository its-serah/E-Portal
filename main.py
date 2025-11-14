"""
FastAPI Face Recognition System
Main application entry point
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import init_db
from routes.auth import router as auth_router
from routes.faces import router as faces_router
from routes.frontend import router as frontend_router
from routes.visits import router as visits_router

# Initialize database
init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifespan - startup and shutdown."""
    # Startup
    print("🚀 Starting Face Recognition API")
    yield
    # Shutdown
    print("🛑 Shutting down Face Recognition API")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Face recognition and detection API using YOLO and DeepFace",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(frontend_router)  # Frontend pages
app.include_router(auth_router)  # Auth API
app.include_router(faces_router)  # Face detection API
app.include_router(visits_router)  # Visit tracking API

# Serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    pass

# Serve media files
try:
    app.mount("/media", StaticFiles(directory="media"), name="media")
except Exception:
    pass


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Face Recognition API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
