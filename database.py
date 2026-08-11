from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_URL, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASS
from models import Base, User, Complaint, ComplaintHistory, Comment
from auth import hash_password

# Database Engine & Session Factory
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Context manager or session getter for database operations."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def init_db():
    """Initializes database tables and seeds demo dataset if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).count() == 0:
            seed_demo_data(db)
    finally:
        db.close()

def seed_demo_data(db):
    """Populates initial realistic demo data for immediate application readiness."""
    print("Seeding database with demo users and realistic complaints...")

    # Password hashes
    admin_pass = hash_password(DEFAULT_ADMIN_PASS)
    staff_pass = hash_password("staff123")
    student_pass = hash_password("student123")

    # 1. Users
    admin = User(
        name="Chief Admin (Dean Office)",
        email=DEFAULT_ADMIN_EMAIL,
        password_hash=admin_pass,
        role="ADMIN",
        department="Campus Operations",
        phone="+1 555-0100"
    )

    staff_infra = User(
        name="Marcus Vance",
        email="staff.infra@campusfix.edu",
        password_hash=staff_pass,
        role="STAFF",
        department="Infrastructure",
        phone="+1 555-0101"
    )
    staff_it = User(
        name="Elena Rostova",
        email="staff.it@campusfix.edu",
        password_hash=staff_pass,
        role="STAFF",
        department="Internet/Wi-Fi",
        phone="+1 555-0102"
    )
    staff_elec = User(
        name="David Miller",
        email="staff.elec@campusfix.edu",
        password_hash=staff_pass,
        role="STAFF",
        department="Electrical",
        phone="+1 555-0103"
    )
    staff_clean = User(
        name="Sarah Jenkins",
        email="staff.clean@campusfix.edu",
        password_hash=staff_pass,
        role="STAFF",
        department="Cleanliness",
        phone="+1 555-0104"
    )

    student1 = User(
        name="Alex Chen",
        email="alex@student.edu",
        password_hash=student_pass,
        role="STUDENT",
        department="Computer Science",
        phone="+1 555-0201"
    )
    student2 = User(
        name="Priya Sharma",
        email="priya@student.edu",
        password_hash=student_pass,
        role="STUDENT",
        department="Mechanical Engineering",
        phone="+1 555-0202"
    )
    student3 = User(
        name="Rahul Verma",
        email="rahul@student.edu",
        password_hash=student_pass,
        role="STUDENT",
        department="Electrical Engineering",
        phone="+1 555-0203"
    )

    db.add_all([admin, staff_infra, staff_it, staff_elec, staff_clean, student1, student2, student3])
    db.commit()

    # Retrieve committed users to get IDs
    student1 = db.query(User).filter_by(email="alex@student.edu").first()
    student2 = db.query(User).filter_by(email="priya@student.edu").first()
    student3 = db.query(User).filter_by(email="rahul@student.edu").first()
    
    staff_infra = db.query(User).filter_by(email="staff.infra@campusfix.edu").first()
    staff_it = db.query(User).filter_by(email="staff.it@campusfix.edu").first()
    staff_elec = db.query(User).filter_by(email="staff.elec@campusfix.edu").first()
    staff_clean = db.query(User).filter_by(email="staff.clean@campusfix.edu").first()
    admin = db.query(User).filter_by(email=DEFAULT_ADMIN_EMAIL).first()

    now = datetime.utcnow()

    # 2. Sample Complaints
    c1 = Complaint(
        id="CF-2026-0001",
        student_id=student1.id,
        category="Internet/Wi-Fi",
        title="Wi-Fi Signal Drops Repeatedly in Central Library 2nd Floor",
        description="The Wi-Fi access point near study cubicle 14 disconnects every 15 minutes during peak hours. High latency disrupts online video lectures and submission portals.",
        location="Library Building, 2nd Floor Quiet Zone",
        priority="High",
        status="In Progress",
        assigned_staff_id=staff_it.id,
        created_at=now - timedelta(days=2, hours=5),
        updated_at=now - timedelta(hours=3)
    )

    c2 = Complaint(
        id="CF-2026-0002",
        student_id=student2.id,
        category="Electrical",
        title="Ceiling Fan Making Loud Noise in LH-302",
        description="The front row ceiling fan has a loose bearing causing grinding metallic noise during morning lectures. Difficult to hear the lecturer.",
        location="Academic Block A, Lecture Hall 302",
        priority="Medium",
        status="Resolved",
        assigned_staff_id=staff_elec.id,
        satisfaction_rating=5,
        satisfaction_feedback="Fixed within 24 hours! Technician replaced the motor bearing cleanly.",
        created_at=now - timedelta(days=4),
        updated_at=now - timedelta(days=1),
        resolved_at=now - timedelta(days=1)
    )

    c3 = Complaint(
        id="CF-2026-0003",
        student_id=student3.id,
        category="Water",
        title="Water Cooler Filter Replacement Required in Hostel Block B",
        description="Water output from 1st floor cooler is yellowish with strange odor. Urgent maintenance required for student health safety.",
        location="Hostel Block B, 1st Floor East Wing",
        priority="Critical",
        status="Assigned",
        assigned_staff_id=staff_infra.id,
        created_at=now - timedelta(hours=10),
        updated_at=now - timedelta(hours=2)
    )

    c4 = Complaint(
        id="CF-2026-0004",
        student_id=student1.id,
        category="Infrastructure",
        title="Broken Window Latch in CS Lab 4",
        description="Window frame latch is broken, causing rain water to leak onto computer workstation desks during storms.",
        location="IT Building, Lab 4",
        priority="Medium",
        status="Submitted",
        assigned_staff_id=None,
        created_at=now - timedelta(hours=3)
    )

    c5 = Complaint(
        id="CF-2026-0005",
        student_id=student2.id,
        category="Cleanliness",
        title="Overflowing Waste Bins Near Student Cafeteria",
        description="Trash containers near cafeteria outdoor seating are full and spilling over. Needs immediate sanitation attention.",
        location="Student Activity Center Exterior",
        priority="Low",
        status="Resolved",
        assigned_staff_id=staff_clean.id,
        satisfaction_rating=4,
        satisfaction_feedback="Area cleaned up nicely.",
        created_at=now - timedelta(days=5),
        updated_at=now - timedelta(days=3),
        resolved_at=now - timedelta(days=3)
    )

    db.add_all([c1, c2, c3, c4, c5])
    db.commit()

    # 3. Complaint Histories
    h1 = ComplaintHistory(
        complaint_id="CF-2026-0001",
        status="Submitted",
        status_note="Complaint registered by student.",
        updated_by_id=student1.id,
        timestamp=now - timedelta(days=2, hours=5)
    )
    h2 = ComplaintHistory(
        complaint_id="CF-2026-0001",
        status="Assigned",
        status_note="Assigned to IT Network team.",
        updated_by_id=admin.id,
        timestamp=now - timedelta(days=1, hours=8)
    )
    h3 = ComplaintHistory(
        complaint_id="CF-2026-0001",
        status="In Progress",
        status_note="Replaced Ethernet patch cable on AP #4; testing signal stability.",
        updated_by_id=staff_it.id,
        timestamp=now - timedelta(hours=3)
    )

    h4 = ComplaintHistory(
        complaint_id="CF-2026-0002",
        status="Submitted",
        status_note="Complaint registered by student.",
        updated_by_id=student2.id,
        timestamp=now - timedelta(days=4)
    )
    h5 = ComplaintHistory(
        complaint_id="CF-2026-0002",
        status="Assigned",
        status_note="Assigned to Electrical Dept.",
        updated_by_id=admin.id,
        timestamp=now - timedelta(days=3)
    )
    h6 = ComplaintHistory(
        complaint_id="CF-2026-0002",
        status="Resolved",
        status_note="Replaced fan assembly unit.",
        updated_by_id=staff_elec.id,
        timestamp=now - timedelta(days=1)
    )

    db.add_all([h1, h2, h3, h4, h5, h6])

    # 4. Comments
    cm1 = Comment(
        complaint_id="CF-2026-0001",
        user_id=student1.id,
        message="Please check AP #4 specifically, it seems to go offline when 30+ devices connect.",
        is_internal=False,
        created_at=now - timedelta(days=1, hours=12)
    )
    cm2 = Comment(
        complaint_id="CF-2026-0001",
        user_id=staff_it.id,
        message="Configured load balancing on AP #4 and ordered a high-density Cisco access point as replacement.",
        is_internal=False,
        created_at=now - timedelta(hours=3)
    )
    cm3 = Comment(
        complaint_id="CF-2026-0003",
        user_id=staff_infra.id,
        message="Internal note: Filter cartridge stock requested from central store.",
        is_internal=True,
        created_at=now - timedelta(hours=1)
    )

    db.add_all([cm1, cm2, cm3])
    db.commit()
    print("Database seeding completed successfully!")
