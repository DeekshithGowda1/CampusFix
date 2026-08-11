import bcrypt
import streamlit as st

def hash_password(password: str) -> str:
    """Hashes a plain password using bcrypt directly."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_current_user():
    """Gets current logged-in user dict/object from Streamlit session state."""
    return st.session_state.get("user", None)

def login_user(user_obj):
    """Sets session state user."""
    st.session_state["user"] = {
        "id": user_obj.id,
        "name": user_obj.name,
        "email": user_obj.email,
        "role": user_obj.role,
        "department": user_obj.department,
        "phone": user_obj.phone
    }

def logout_user():
    """Clears user session state."""
    if "user" in st.session_state:
        del st.session_state["user"]

