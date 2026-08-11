from datetime import datetime
from sqlalchemy import or_, desc
from database import SessionLocal
from models import Complaint, ComplaintHistory, Comment, User

def generate_complaint_id(db_session) -> str:
    """Generates unique sequential Complaint ID like CF-2026-0001."""
    year = datetime.utcnow().year
    prefix = f"CF-{year}-"
    
    # Query latest complaint ID matching the prefix
    latest = db_session.query(Complaint).filter(Complaint.id.like(f"{prefix}%")).order_by(desc(Complaint.id)).first()
    
    if latest:
        try:
            seq_num = int(latest.id.split("-")[-1]) + 1
        except ValueError:
            seq_num = db_session.query(Complaint).count() + 1
    else:
        seq_num = 1
        
    return f"{prefix}{seq_num:04d}"

def create_complaint(student_id: int, category: str, title: str, description: str, location: str, priority: str = "Medium", image_path: str = None):
    """Creates a new complaint and logs initial history record."""
    db = SessionLocal()
    try:
        complaint_id = generate_complaint_id(db)
        
        complaint = Complaint(
            id=complaint_id,
            student_id=student_id,
            category=category,
            title=title.strip(),
            description=description.strip(),
            location=location.strip(),
            priority=priority,
            status="Submitted",
            image_path=image_path,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(complaint)
        
        # Log initial history
        history = ComplaintHistory(
            complaint_id=complaint_id,
            status="Submitted",
            status_note="Complaint registered by student.",
            updated_by_id=student_id,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        
        db.commit()
        db.refresh(complaint)
        return True, complaint
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def get_complaint_by_id(complaint_id: str):
    """Retrieves a single complaint with full details."""
    db = SessionLocal()
    try:
        return db.query(Complaint).filter_by(id=complaint_id).first()
    finally:
        db.close()

def get_complaints(
    user_role: str = "ADMIN",
    user_id: int = None,
    category_filter: str = "All",
    priority_filter: str = "All",
    status_filter: str = "All",
    search_query: str = ""
):
    """Fetches complaints based on user role and filters."""
    db = SessionLocal()
    try:
        query = db.query(Complaint)
        
        # Role-based restriction
        if user_role == "STUDENT" and user_id:
            query = query.filter(Complaint.student_id == user_id)
        elif user_role == "STAFF" and user_id:
            query = query.filter(or_(Complaint.assigned_staff_id == user_id, Complaint.assigned_staff_id == None))
            
        # Filters
        if category_filter and category_filter != "All":
            query = query.filter(Complaint.category == category_filter)
            
        if priority_filter and priority_filter != "All":
            query = query.filter(Complaint.priority == priority_filter)
            
        if status_filter and status_filter != "All":
            query = query.filter(Complaint.status == status_filter)
            
        if search_query:
            sq = f"%{search_query.strip()}%"
            query = query.filter(
                or_(
                    Complaint.id.like(sq),
                    Complaint.title.like(sq),
                    Complaint.description.like(sq),
                    Complaint.location.like(sq)
                )
            )
            
        return query.order_by(desc(Complaint.created_at)).all()
    finally:
        db.close()

def assign_complaint(complaint_id: str, staff_id: int, updated_by_id: int, note: str = ""):
    """Assigns or reassigns a complaint to a staff member."""
    db = SessionLocal()
    try:
        complaint = db.query(Complaint).filter_by(id=complaint_id).first()
        staff = db.query(User).filter_by(id=staff_id).first()
        if not complaint or not staff:
            return False, "Complaint or staff member not found."
            
        complaint.assigned_staff_id = staff_id
        complaint.status = "Assigned"
        complaint.updated_at = datetime.utcnow()
        
        note_text = f"Assigned to {staff.name} ({staff.department}). {note}".strip()
        history = ComplaintHistory(
            complaint_id=complaint_id,
            status="Assigned",
            status_note=note_text,
            updated_by_id=updated_by_id,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        return True, "Complaint assigned successfully."
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def update_complaint_status(complaint_id: str, new_status: str, updated_by_id: int, note: str = ""):
    """Updates complaint status and appends timeline log."""
    db = SessionLocal()
    try:
        complaint = db.query(Complaint).filter_by(id=complaint_id).first()
        if not complaint:
            return False, "Complaint not found."
            
        complaint.status = new_status
        complaint.updated_at = datetime.utcnow()
        if new_status == "Resolved":
            complaint.resolved_at = datetime.utcnow()
            
        history = ComplaintHistory(
            complaint_id=complaint_id,
            status=new_status,
            status_note=note.strip() if note else f"Status changed to {new_status}.",
            updated_by_id=updated_by_id,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        return True, f"Status updated to {new_status}."
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def reopen_complaint(complaint_id: str, student_id: int, reason: str):
    """Allows student to reopen a resolved complaint."""
    db = SessionLocal()
    try:
        complaint = db.query(Complaint).filter_by(id=complaint_id).first()
        if not complaint:
            return False, "Complaint not found."
            
        if complaint.status != "Resolved":
            return False, "Only resolved complaints can be reopened."
            
        complaint.status = "In Progress"
        complaint.reopen_count += 1
        complaint.resolved_at = None
        complaint.updated_at = datetime.utcnow()
        
        history = ComplaintHistory(
            complaint_id=complaint_id,
            status="Reopened",
            status_note=f"Reopened by student: {reason.strip()}",
            updated_by_id=student_id,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        return True, "Complaint reopened and sent back to staff."
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def submit_satisfaction_rating(complaint_id: str, rating: int, feedback: str = ""):
    """Submits student satisfaction rating (1-5) and feedback for resolved complaint."""
    db = SessionLocal()
    try:
        complaint = db.query(Complaint).filter_by(id=complaint_id).first()
        if not complaint:
            return False, "Complaint not found."
            
        complaint.satisfaction_rating = rating
        complaint.satisfaction_feedback = feedback.strip()
        db.commit()
        return True, "Rating submitted successfully!"
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def add_comment(complaint_id: str, user_id: int, message: str, is_internal: bool = False):
    """Adds a public or internal comment to a complaint."""
    db = SessionLocal()
    try:
        comment = Comment(
            complaint_id=complaint_id,
            user_id=user_id,
            message=message.strip(),
            is_internal=is_internal,
            created_at=datetime.utcnow()
        )
        db.add(comment)
        db.commit()
        return True, "Comment posted."
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()
