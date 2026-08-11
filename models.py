from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="STUDENT")  # STUDENT, STAFF, ADMIN
    department = Column(String(100), nullable=True)  # e.g., IT, Maintenance, Hostel, CS Dept
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    submitted_complaints = relationship("Complaint", foreign_keys="Complaint.student_id", back_populates="student")
    assigned_complaints = relationship("Complaint", foreign_keys="Complaint.assigned_staff_id", back_populates="assigned_staff")
    comments = relationship("Comment", back_populates="user")
    history_entries = relationship("ComplaintHistory", back_populates="updated_by")

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String(20), primary_key=True)  # e.g., CF-2026-0001
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(50), nullable=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(150), nullable=False)
    priority = Column(String(20), nullable=False, default="Medium")  # Low, Medium, High, Critical
    status = Column(String(30), nullable=False, default="Submitted")  # Submitted, Under Review, Assigned, In Progress, Resolved, Rejected
    assigned_staff_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_path = Column(String(255), nullable=True)
    
    # Rating & Feedback
    satisfaction_rating = Column(Integer, nullable=True)  # 1 to 5
    satisfaction_feedback = Column(Text, nullable=True)
    reopen_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    student = relationship("User", foreign_keys=[student_id], back_populates="submitted_complaints")
    assigned_staff = relationship("User", foreign_keys=[assigned_staff_id], back_populates="assigned_complaints")
    history = relationship("ComplaintHistory", back_populates="complaint", cascade="all, delete-orphan", order_by="ComplaintHistory.timestamp.asc()")
    comments = relationship("Comment", back_populates="complaint", cascade="all, delete-orphan", order_by="Comment.created_at.asc()")

    def __repr__(self):
        return f"<Complaint {self.id}: {self.title} [{self.status}]>"


class ComplaintHistory(Base):
    __tablename__ = "complaint_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(String(20), ForeignKey("complaints.id"), nullable=False)
    status = Column(String(30), nullable=False)
    status_note = Column(Text, nullable=True)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    complaint = relationship("Complaint", back_populates="history")
    updated_by = relationship("User", back_populates="history_entries")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(String(20), ForeignKey("complaints.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # True if staff-only internal note
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    complaint = relationship("Complaint", back_populates="comments")
    user = relationship("User", back_populates="comments")
