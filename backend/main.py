from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.department import Department
from models.user import User
from models.complaint import Complaint
from models.history import ComplaintHistory
from database import get_db
from routes.complaints import router as complaint_router


# 1. Create the FastAPI application first
app = FastAPI(
    title="University Complaint Management System",
    version="1.0"
)


# 2. Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Include complaint routes after creating app
app.include_router(complaint_router)


# 4. Home route
@app.get("/")
def home():
    return {
        "message": "University Complaint Management API is running"
    }


# 5. Database health check
@app.get("/db-health")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "success",
            "message": "MySQL connected successfully"
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="MySQL connection failed"
        )