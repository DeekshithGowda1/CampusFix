import streamlit as st
import os

# Set page configuration FIRST before any other streamlit commands
st.set_page_config(
    page_title="CampusFix – Smart College Issue Management System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database import init_db
from styles import apply_custom_css
from auth import get_current_user, logout_user
from auth_view import render_auth_page
from student_view import render_student_view
from staff_view import render_staff_view
from admin_view import render_admin_view

def main():
    # Initialize Database & Seed Data
    init_db()

    # Apply Custom Modern Styling
    apply_custom_css()

    # Check authentication state
    user = get_current_user()

    # Sidebar Header & Navigation
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align: center; padding-bottom: 1rem;'>
                <h2 style='color: #1e3c72; margin-bottom: 0;'>🏛️ CampusFix</h2>
                <span style='font-size: 0.85rem; color: #64748b;'>College Issue Management System</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        if user:
            role_emoji = "🎓" if user["role"] == "STUDENT" else ("🛠️" if user["role"] == "STAFF" else "👑")
            st.markdown(f"### {role_emoji} Logged In User")
            st.markdown(f"**Name:** {user['name']}")
            st.markdown(f"**Email:** `{user['email']}`")
            st.markdown(f"**Role:** `{user['role']}`")
            if user.get("department"):
                st.markdown(f"**Dept:** {user['department']}")
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
        else:
            st.markdown("🔒 **Please Sign In**")
            st.caption("Use the main window to log in or register a new student account.")
            
        st.markdown("---")
        st.markdown(
            """
            <div style='font-size: 0.78rem; color: #94a3b8; text-align: center;'>
                CampusFix v2.0 • Built with Streamlit & SQLAlchemy
            </div>
            """,
            unsafe_allow_html=True
        )

    # Main Area View Router
    if not user:
        render_auth_page()
    else:
        role = user["role"]
        if role == "STUDENT":
            render_student_view(user)
        elif role == "STAFF":
            render_staff_view(user)
        elif role == "ADMIN":
            render_admin_view(user)
        else:
            st.error("Unknown user role.")

if __name__ == "__main__":
    main()
