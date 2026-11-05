
import os
import uuid
import hashlib
import secrets
import traceback

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)
from sqlalchemy.orm import Session

from database import get_db
from models.complaint import Complaint
from models.history import ComplaintHistory


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp"
]

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/")
async def submit_complaint(
    roll_number: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    # 1. Validate required fields
    if not roll_number.strip():
        raise HTTPException(
            status_code=400,
            detail="Roll number is required"
        )

    if not description.strip():
        raise HTTPException(
            status_code=400,
            detail="Description is required"
        )

    if not location.strip():
        raise HTTPException(
            status_code=400,
            detail="Location is required"
        )

    image_path = None

    try:
        # 2. Handle optional image
        if image and image.filename:

            if image.content_type not in ALLOWED_TYPES:
                raise HTTPException(
                    status_code=400,
                    detail="Only JPG, PNG and WEBP images are allowed"
                )

            content = await image.read()

            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="Image must be smaller than 5 MB"
                )

            extension = {
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "image/webp": ".webp"
            }[image.content_type]

            filename = f"{uuid.uuid4().hex}{extension}"

            image_path = os.path.join(
                UPLOAD_DIR,
                filename
            )

            with open(image_path, "wb") as file:
                file.write(content)

        # 3. Generate complaint ID
        complaint_code = (
            "CMP" + secrets.token_hex(8).upper()
        )

        # 4. Generate secure verification token
        verification_token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            verification_token.encode("utf-8")
        ).hexdigest()

        # 5. Create complaint record
        complaint = Complaint(
            complaint_code=complaint_code,
            roll_number=roll_number.strip(),
            description=description.strip(),
            location=location.strip(),
            image_path=image_path,
            status="PENDING",
            priority="MEDIUM",
            verification_token_hash=token_hash
        )

        db.add(complaint)

        # Get the generated complaint ID
        db.flush()

        # 6. Add initial complaint history
        history = ComplaintHistory(
            complaint_id=complaint.id,
            old_status=None,
            new_status="PENDING",
            remarks="Complaint submitted successfully"
        )

        db.add(history)

        # 7. Save both records
        db.commit()
        db.refresh(complaint)

        # 8. Return successful response
        return {
            "message": "Complaint submitted successfully",
            "complaint_id": complaint.complaint_code,
            "verification_token": verification_token,
            "status": complaint.status
        }

    except HTTPException:
        db.rollback()

        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        raise

    except Exception:
        traceback.print_exc()

        db.rollback()

        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        raise HTTPException(
            status_code=500,
            detail="Could not submit complaint"
        )

@router.get("/{complaint_code}")
def track_complaint(
    complaint_code: str,
    db: Session = Depends(get_db)
):
    # 1. Find complaint
    complaint = db.query(Complaint).filter(
        Complaint.complaint_code == complaint_code.upper()
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    # 2. Fetch complaint history
    history_records = db.query(ComplaintHistory).filter(
        ComplaintHistory.complaint_id == complaint.id
    ).order_by(
        ComplaintHistory.changed_at.asc(),
        ComplaintHistory.id.asc()
    ).all()

    # 3. Prepare timeline
    timeline = []

    for record in history_records:
        timeline.append({
            "old_status": record.old_status,
            "new_status": record.new_status,
            "remarks": record.remarks,
            "changed_at": (
                record.changed_at.isoformat()
                if record.changed_at else None
            )
        })

    # 4. Return tracking information
    return {
        "complaint_id": complaint.complaint_code,
        "description": complaint.description,
        "location": complaint.location,
        "category": complaint.category,
        "priority": complaint.priority,
        "status": complaint.status,
        "created_at": (
            complaint.created_at.isoformat()
            if complaint.created_at else None
        ),
        "resolution_remarks": complaint.resolution_remarks,
        "timeline": timeline
    }
