from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from auth import verify_password, create_access_token

router = APIRouter(prefix="/officer", tags=["Officer"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    officer_id: int
    name: str


@router.post("/login", response_model=LoginResponse)
def officer_login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    # Same message for wrong username/password so we don't reveal which one failed
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    if user.role != "OFFICER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: officer accounts only",
        )

    token = create_access_token(user.id, user.role)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        officer_id=user.id,
        name=user.name,
    )


from dependencies import get_current_officer


@router.get("/me")
def officer_me(current_officer: User = Depends(get_current_officer)):
    return {
        "id": current_officer.id,
        "name": current_officer.name,
        "username": current_officer.username,
        "role": current_officer.role,
    }


from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from models.complaint import Complaint


class ComplaintListItem(BaseModel):
    id: int
    complaint_code: str
    category: Optional[str] = None
    priority: Optional[str] = None
    location: str
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.get("/complaints", response_model=List[ComplaintListItem])
def get_my_complaints(
    status: Optional[str] = None,
    current_officer: User = Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    query = db.query(Complaint).filter(
        Complaint.assigned_officer_id == current_officer.id
    )
    if status:
        query = query.filter(Complaint.status == status)
    return query.order_by(Complaint.created_at.desc()).all()


from fastapi import HTTPException
from models.history import ComplaintHistory


class HistoryItem(BaseModel):
    id: int
    old_status: Optional[str] = None
    new_status: str
    remarks: Optional[str] = None
    changed_by: Optional[int] = None
    changed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComplaintDetail(BaseModel):
    id: int
    complaint_code: str
    roll_number: str
    description: str
    image_path: Optional[str] = None
    location: str
    category: Optional[str] = None
    priority: Optional[str] = None
    department_id: Optional[int] = None
    status: str
    resolution_remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    history: List[HistoryItem] = []

    class Config:
        from_attributes = True


@router.get("/complaints/{complaint_id}", response_model=ComplaintDetail)
def get_complaint_details(
    complaint_id: int,
    current_officer: User = Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint.assigned_officer_id != current_officer.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this complaint",
        )

    history = (
        db.query(ComplaintHistory)
        .filter(ComplaintHistory.complaint_id == complaint.id)
        .order_by(ComplaintHistory.changed_at.asc())
        .all()
    )

    return ComplaintDetail(
        id=complaint.id,
        complaint_code=complaint.complaint_code,
        roll_number=complaint.roll_number,
        description=complaint.description,
        image_path=complaint.image_path,
        location=complaint.location,
        category=complaint.category,
        priority=complaint.priority,
        department_id=complaint.department_id,
        status=complaint.status,
        resolution_remarks=complaint.resolution_remarks,
        created_at=complaint.created_at,
        deadline=complaint.deadline,
        history=[HistoryItem.model_validate(h) for h in history],
    )


ALLOWED_TRANSITIONS = {
    "PENDING": "IN_PROGRESS",
    "IN_PROGRESS": "AWAITING_VERIFICATION",
}


class StatusUpdateRequest(BaseModel):
    new_status: str
    remarks: Optional[str] = None


class StatusUpdateResponse(BaseModel):
    id: int
    complaint_code: str
    old_status: str
    new_status: str
    message: str


@router.put("/complaints/{complaint_id}/status", response_model=StatusUpdateResponse)
def update_complaint_status(
    complaint_id: int,
    data: StatusUpdateRequest,
    current_officer: User = Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint.assigned_officer_id != current_officer.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this complaint",
        )

    old_status = complaint.status
    new_status = data.new_status.strip().upper()

    if ALLOWED_TRANSITIONS.get(old_status) != new_status:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status change: {old_status} -> {new_status}",
        )

    remarks = data.remarks.strip() if data.remarks else None
    if new_status == "AWAITING_VERIFICATION" and not remarks:
        raise HTTPException(
            status_code=400,
            detail="Resolution remarks are required to submit a resolution",
        )

    complaint.status = new_status
    if remarks:
        complaint.resolution_remarks = remarks
    if new_status == "AWAITING_VERIFICATION":
        complaint.resolved_at = datetime.now()

    db.add(
        ComplaintHistory(
            complaint_id=complaint.id,
            old_status=old_status,
            new_status=new_status,
            remarks=remarks,
            changed_by=current_officer.id,
        )
    )
    db.commit()

    return StatusUpdateResponse(
        id=complaint.id,
        complaint_code=complaint.complaint_code,
        old_status=old_status,
        new_status=new_status,
        message="Status updated successfully",
    )
