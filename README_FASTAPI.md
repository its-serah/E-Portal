# FastAPI Face Recognition System

This is a complete conversion of the Django Face Recognition system to FastAPI.

## Changes Made

### Framework Migration
- **Django → FastAPI**: Replaced Django framework with FastAPI for better performance and async support
- **Django ORM → SQLAlchemy**: Migrated from Django models to SQLAlchemy with SQLite/PostgreSQL support
- **Django Auth → JWT**: Implemented JWT-based authentication instead of Django sessions
- **Django Forms → Pydantic**: Replaced Django forms with Pydantic schemas for validation

### New Structure

```
Face-Recognition/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── database.py            # Database setup and session management
├── models.py              # SQLAlchemy models (User, Face)
├── schemas.py             # Pydantic schemas for validation
├── auth.py               # JWT authentication utilities
├── routes/
│   ├── __init__.py
│   ├── auth.py           # Authentication routes (login, register, logout)
│   └── faces.py          # Face management and recognition routes
├── .env                  # Environment variables (copy from .env.example)
├── requirements.txt      # Python dependencies
└── face/                 # Original Django app (kept for utils)
    └── utils.py          # Utility functions (align_face, Telegram notifications)
```

## Installation

1. **Create virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application**:
```bash
python3 main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user info

### Face Management
- `GET /api/faces/` - List all faces
- `POST /api/faces/` - Add new face (multipart form-data with image)
- `GET /api/faces/{face_id}` - Get face details
- `PUT /api/faces/{face_id}` - Update face
- `DELETE /api/faces/{face_id}` - Delete face

### Face Recognition
- `POST /api/faces/detect` - Detect and recognize faces in image

## Database

### SQLite (Default)
- Database file: `face_recognition.db`
- No additional setup required

### PostgreSQL
- Update `.env` with:
  ```
  USE_POSTGRESQL=True
  DB_HOST=your_host
  DB_PORT=5432
  DB_NAME=face_recognition
  DB_USER=postgres
  DB_PASSWORD=your_password
  ```

Tables are automatically created on first run.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: POST to `/api/auth/register`
   ```json
   {
     "username": "user",
     "email": "user@example.com",
     "password": "securepassword",
     "password2": "securepassword"
   }
   ```

2. **Login**: POST to `/api/auth/login`
   ```json
   {
     "username": "user",
     "password": "securepassword"
   }
   ```
   Returns:
   ```json
   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "token_type": "bearer"
   }
   ```

3. **Use token**: Include in request headers:
   ```
   Authorization: Bearer {access_token}
   ```

## Face Recognition

### Upload and Detect
```bash
curl -X POST "http://localhost:8000/api/faces/detect" \
  -H "Authorization: Bearer {token}" \
  -F "image=@photo.jpg" \
  -F "model=yolov8n"
```

### Available Models
- `yolov8n` - YOLOv8 nano (general)
- `yolov8m` - YOLOv8 medium (general)
- `yolov8n-face` - YOLOv8 nano (face-specific)
- `yolov8m-face` - YOLOv8 medium (face-specific)
- `yolov8l-face` - YOLOv8 large (face-specific)
- `yolov10s-face` - YOLOv10 small
- `yolov11m-face` - YOLOv11 medium
- `yolov11l-face` - YOLOv11 large

## Configuration

Key settings in `.env`:

- `DEBUG` - Enable debug mode (development only)
- `SECRET_KEY` - JWT signing key (must be changed in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time
- `TELEGRAM_BOT_TOKEN` - Telegram bot token for notifications
- `TELEGRAM_CHANNEL_ID` - Telegram channel for alerts

## Features

✅ User authentication with JWT
✅ Face detection using YOLO
✅ Face recognition using DeepFace
✅ Face alignment for better accuracy
✅ Telegram notifications
✅ SQLite/PostgreSQL support
✅ Async request handling
✅ Automatic API documentation (Swagger/OpenAPI)

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Performance Improvements Over Django

1. **Async Support** - Non-blocking requests for better throughput
2. **Automatic Validation** - Pydantic handles input validation
3. **Better Documentation** - Auto-generated OpenAPI/Swagger docs
4. **Simpler Deployment** - No WSGI/ASGI conversion layer needed

## Original Django Code

The original Django apps (`core/` and `face/` directories) are kept for reference and utilities like `align_face()` and Telegram functionality.

To completely remove Django dependencies:
- Delete `manage.py`, `frecog/` directory, and `core/` directory
- Move necessary utilities from `face/utils.py` to `app/utils.py`

## Troubleshooting

### ImportError: No module named 'deepface'
Install all requirements:
```bash
pip install -r requirements.txt
```

### Database locked error
This occurs with SQLite under concurrent writes. For production, use PostgreSQL:
```bash
USE_POSTGRESQL=True
```

### Telegram notifications not sending
Check that `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHANNEL_ID` are set in `.env`

## License

Same as original project
