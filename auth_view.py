import streamlit as st
from services.user_service import authenticate_user, register_student
from auth import login_user

def render_auth_page():
    """Renders Login & Registration interface."""
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1rem 0;">
            <h1 style="color: #1e3c72; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.2rem;">🏛️ CampusFix</h1>
            <p style="color: #64748b; font-size: 1.1rem;">Smart College Issue & Complaint Management System</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Demo Quick Switcher Banner for rapid evaluation
    st.info("💡 **Quick Demo Credentials**: Click any button below to instantly log in as a demo user!")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    
    with col_d1:
        if st.button("🔑 Demo Student", use_container_width=True):
            user, msg = authenticate_user("alex@student.edu", "student123")
            if user:
                login_user(user)
                st.rerun()

    with col_d2:
        if st.button("🛠️ Demo IT Staff", use_container_width=True):
            user, msg = authenticate_user("staff.it@campusfix.edu", "staff123")
            if user:
                login_user(user)
                st.rerun()

    with col_d3:
        if st.button("🔧 Demo Infra Staff", use_container_width=True):
            user, msg = authenticate_user("staff.infra@campusfix.edu", "staff123")
            if user:
                login_user(user)
                st.rerun()

    with col_d4:
        if st.button("👑 Demo Admin", use_container_width=True):
            user, msg = authenticate_user("admin@campusfix.edu", "admin123")
            if user:
                login_user(user)
                st.rerun()

    st.markdown("---")

    # Tabs for Login vs Register
    tab_login, tab_register = st.tabs(["🔐 Sign In", "📝 Student Registration"])

    with tab_login:
        st.subheader("Account Login")
        with st.form("login_form"):
            email_input = st.text_input("Email Address", placeholder="e.g. alex@student.edu")
            password_input = st.text_input("Password", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Sign In", use_container_width=True)

            if submit_login:
                if not email_input or not password_input:
                    st.error("Please enter both email and password.")
                else:
                    user, msg = authenticate_user(email_input, password_input)
                    if user:
                        login_user(user)
                        st.success(f"Welcome back, {user.name}!")
                        st.rerun()
                    else:
                        st.error(msg)

    with tab_register:
        st.subheader("Create a Student Account")
        with st.form("register_form"):
            reg_name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
            reg_email = st.text_input("College Email Address", placeholder="e.g. jane@student.edu")
            reg_dept = st.selectbox("Department", [
                "Computer Science & Engineering",
                "Information Technology",
                "Electrical Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
                "Electronics & Communication",
                "Business Administration",
                "Other"
            ])
            reg_phone = st.text_input("Phone Number", placeholder="e.g. +1 555-0199")
            reg_pass1 = st.text_input("Password", type="password")
            reg_pass2 = st.text_input("Confirm Password", type="password")

            submit_reg = st.form_submit_button("Register Account", use_container_width=True)

            if submit_reg:
                if not reg_name or not reg_email or not reg_pass1:
                    st.error("Please fill in all required fields.")
                elif reg_pass1 != reg_pass2:
                    st.error("Passwords do not match.")
                elif len(reg_pass1) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    success, result = register_student(reg_name, reg_email, reg_pass1, reg_dept, reg_phone)
                    if success:
                        st.success("Registration successful! You can now sign in using your credentials.")
                    else:
                        st.error(f"Registration failed: {result}")
