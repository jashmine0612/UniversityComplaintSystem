from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import text
from database import Base


class ComplaintHistory(Base):
    __tablename__ = "complaint_history"

    id = Column(Integer, primary_key=True, index=True)

    complaint_id = Column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=False
    )

    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    remarks = Column(Text, nullable=True)

    changed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    changed_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )