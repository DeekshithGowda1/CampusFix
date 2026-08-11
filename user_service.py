from database import SessionLocal
from models import User
from auth import hash_password, verify_password

def register_student(name: str, email: str, password: str, department: str = "", phone: str = ""):
    """Registers a new student account."""
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(email=email.strip().lower()).first()
        if existing:
            return False, "An account with this email address already exists."
        
        user = User(
            name=name.strip(),
            email=email.strip().lower(),
            password_hash=hash_password(password),
            role="STUDENT",
            department=department.strip(),
            phone=phone.strip()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return True, user
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def create_staff_member(name: str, email: str, password: str, department: str, phone: str = ""):
    """Admin function to create a new Staff account."""
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(email=email.strip().lower()).first()
        if existing:
            return False, "An account with this email address already exists."
        
        staff = User(
            name=name.strip(),
            email=email.strip().lower(),
            password_hash=hash_password(password),
            role="STAFF",
            department=department.strip(),
            phone=phone.strip()
        )
        db.add(staff)
        db.commit()
        db.refresh(staff)
        return True, staff
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

def authenticate_user(email: str, password: str):
    """Authenticates user by email and password."""
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email.strip().lower()).first()
        if not user:
            return None, "Invalid email or password."
        
        if verify_password(password, user.password_hash):
            return user, "Success"
        return None, "Invalid email or password."
    finally:
        db.close()

def get_all_staff():
    """Returns list of all staff members."""
    db = SessionLocal()
    try:
        return db.query(User).filter_by(role="STAFF").order_by(User.name).all()
    finally:
        db.close()

def get_all_users():
    """Returns list of all users."""
    db = SessionLocal()
    try:
        return db.query(User).order_by(User.role, User.name).all()
    finally:
        db.close()

def get_user_by_id(user_id: int):
    """Fetches user model by ID."""
    db = SessionLocal()
    try:
        return db.query(User).get(user_id)
    finally:
        db.close()
