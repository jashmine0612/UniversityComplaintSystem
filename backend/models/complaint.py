from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import text
from database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_code = Column(String(30), unique=True, nullable=False)

    roll_number = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=True)
    location = Column(String(255), nullable=False)

    category = Column(String(100), nullable=True)
    priority = Column(String(20), default="MEDIUM")
    department_id = Column(Integer, nullable=True)
    assigned_officer_id = Column(Integer, nullable=True)

    status = Column(String(50), default="PENDING")
    verification_token_hash = Column(String(255), nullable=False)

    resolution_remarks = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    deadline = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    closure_reason = Column(String(50), nullable=True)