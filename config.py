import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///./campusfix.db")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_campusfix_2026")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@campusfix.edu")
DEFAULT_ADMIN_PASS = os.getenv("DEFAULT_ADMIN_PASS", "admin123")
APP_NAME = os.getenv("APP_NAME", "CampusFix")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Complaint Categories
COMPLAINT_CATEGORIES = [
    "Infrastructure",
    "Electrical",
    "Water",
    "Internet/Wi-Fi",
    "Hostel",
    "Library",
    "Classroom",
    "Transport",
    "Cleanliness",
    "Security",
    "Other"
]

# Priorities
PRIORITIES = ["Low", "Medium", "High", "Critical"]

# Status Flow
STATUS_LIST = [
    "Submitted",
    "Under Review",
    "Assigned",
    "In Progress",
    "Resolved",
    "Rejected"
]

# Role types
ROLE_STUDENT = "STUDENT"
ROLE_STAFF = "STAFF"
ROLE_ADMIN = "ADMIN"
ROLES = [ROLE_STUDENT, ROLE_STAFF, ROLE_ADMIN]
