import os
import streamlit as st
from config import COMPLAINT_CATEGORIES, PRIORITIES, STATUS_LIST
from services.complaint_service import (
    create_complaint,
    get_complaints,
    get_complaint_by_id,
    reopen_complaint,
    submit_satisfaction_rating,
    add_comment
)
from services.utils import save_uploaded_file, format_datetime
from components.ui_elements import render_header, render_kpi_card, get_status_badge_html, get_priority_badge_html, render_timeline

def render_student_view(current_user):
    """Renders Student Portal Interface."""
    render_header(
        f"🎓 Welcome, {current_user['name']}",
        "Report campus issues, track resolution timelines, and give feedback."
    )

    # Fetch student's complaints
    all_my_complaints = get_complaints(user_role="STUDENT", user_id=current_user["id"])
    
    total_cnt = len(all_my_complaints)
    in_prog_cnt = sum(1 for c in all_my_complaints if c.status in ["Submitted", "Under Review", "Assigned", "In Progress"])
    resolved_cnt = sum(1 for c in all_my_complaints if c.status == "Resolved")

    # KPI Summary Cards
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        render_kpi_card("Total Submitted", str(total_cnt), "All time complaints")
    with col_k2:
        render_kpi_card("Active / In Progress", str(in_prog_cnt), "Awaiting resolution")
    with col_k3:
        render_kpi_card("Resolved Issues", str(resolved_cnt), "Completed repairs")

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Navigation Tabs
    tab_track, tab_create = st.tabs(["📋 My Complaints & Status", "➕ Submit New Complaint"])

    # --- TAB 1: TRACK & VIEW COMPLAINTS ---
    with tab_track:
        st.subheader("Submitted Complaints")
        
        # Search & Filter controls
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search Complaints", placeholder="Search by ID, title, or location...")
        with f_col2:
            status_filter = st.selectbox("Status Filter", ["All"] + STATUS_LIST)
        with f_col3:
            category_filter = st.selectbox("Category Filter", ["All"] + COMPLAINT_CATEGORIES)

        filtered_complaints = get_complaints(
            user_role="STUDENT",
            user_id=current_user["id"],
            category_filter=category_filter,
            status_filter=status_filter,
            search_query=search_query
        )

        if not filtered_complaints:
            st.info("No complaints found matching your filters.")
        else:
            for complaint in filtered_complaints:
                status_html = get_status_badge_html(complaint.status)
                prio_html = get_priority_badge_html(complaint.priority)
                
                with st.expander(f"📌 [{complaint.id}] {complaint.title} — {complaint.category}"):
                    c_left, c_right = st.columns([2, 1])
                    
                    with c_left:
                        st.markdown(f"**Status:** {status_html} &nbsp; {prio_html}", unsafe_allow_html=True)
                        st.markdown(f"**Location:** `{complaint.location}`")
                        st.markdown(f"**Submitted On:** {format_datetime(complaint.created_at)}")
                        st.markdown(f"**Description:**\n>{complaint.description}")
                        
                        if complaint.image_path and os.path.exists(complaint.image_path):
                            st.image(complaint.image_path, caption="Uploaded Evidence", width=350)
                            
                    with c_right:
                        staff_name = complaint.assigned_staff.name if complaint.assigned_staff else "Not Assigned Yet"
                        staff_dept = f"({complaint.assigned_staff.department})" if complaint.assigned_staff else ""
                        st.markdown(f"**Assigned Technician:**\n{staff_name} {staff_dept}")
                        
                        # Satisfaction Rating section if resolved
                        if complaint.status == "Resolved":
                            st.markdown("---")
                            st.markdown("##### 🌟 Resolution Feedback")
                            if complaint.satisfaction_rating:
                                st.success(f"Rated: {'⭐' * complaint.satisfaction_rating} ({complaint.satisfaction_rating}/5)")
                                if complaint.satisfaction_feedback:
                                    st.caption(f'"{complaint.satisfaction_feedback}"')
                            else:
                                with st.form(f"rate_form_{complaint.id}"):
                                    rating_val = st.slider("Rate satisfaction (1-5)", 1, 5, 5)
                                    feedback_txt = st.text_input("Feedback notes (optional)")
                                    submit_rate = st.form_submit_button("Submit Rating")
                                    if submit_rate:
                                        s_ok, s_msg = submit_satisfaction_rating(complaint.id, rating_val, feedback_txt)
                                        if s_ok:
                                            st.success(s_msg)
                                            st.rerun()
                                            
                                # Reopen Complaint option
                                with st.popover("🔄 Reopen Issue"):
                                    reopen_reason = st.text_area("Reason for reopening")
                                    if st.button("Confirm Reopen", key=f"reopen_btn_{complaint.id}"):
                                        if not reopen_reason.strip():
                                            st.error("Please provide a reason.")
                                        else:
                                            ro_ok, ro_msg = reopen_complaint(complaint.id, current_user["id"], reopen_reason)
                                            if ro_ok:
                                                st.success(ro_msg)
                                                st.rerun()

                    # --- Timeline & Comments Accordion ---
                    st.markdown("---")
                    sub_t1, sub_t2 = st.tabs(["📜 Resolution Timeline", "💬 Discussion & Notes"])
                    
                    with sub_t1:
                        render_timeline(complaint.history)
                        
                    with sub_t2:
                        # Display public comments
                        pub_comments = [cm for cm in complaint.comments if not cm.is_internal]
                        if not pub_comments:
                            st.caption("No comments posted yet.")
                        else:
                            for cm in pub_comments:
                                u_name = cm.user.name if cm.user else "User"
                                u_role = f"[{cm.user.role}]" if cm.user else ""
                                st.markdown(f"**{u_name}** {u_role} • <span style='font-size:0.8rem; color:#64748b;'>{format_datetime(cm.created_at)}</span>", unsafe_allow_html=True)
                                st.write(cm.message)
                                st.markdown("<hr style='margin:0.4rem 0;'>", unsafe_allow_html=True)
                                
                        # Post new comment form
                        with st.form(f"comment_form_{complaint.id}"):
                            new_msg = st.text_area("Add a response/comment", height=70)
                            post_btn = st.form_submit_button("Post Comment")
                            if post_btn:
                                if not new_msg.strip():
                                    st.error("Comment cannot be empty.")
                                else:
                                    c_ok, c_msg = add_comment(complaint.id, current_user["id"], new_msg, is_internal=False)
                                    if c_ok:
                                        st.success(c_msg)
                                        st.rerun()

    # --- TAB 2: CREATE NEW COMPLAINT ---
    with tab_create:
        st.subheader("Lodge a New Campus Complaint")
        with st.form("create_complaint_form", clear_on_submit=True):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                cat_input = st.selectbox("Category *", COMPLAINT_CATEGORIES)
                prio_input = st.selectbox("Priority Level *", PRIORITIES, index=1)
            with col_c2:
                location_input = st.text_input("Exact Location *", placeholder="e.g., CS Block, 3rd Floor, Room 305")
                uploaded_image = st.file_uploader("Upload Evidence Photo (Optional)", type=["png", "jpg", "jpeg", "webp"])

            title_input = st.text_input("Complaint Title *", placeholder="e.g. Projector power failure during morning lectures")
            desc_input = st.text_area("Detailed Description *", placeholder="Describe the issue, frequency, and impact on classes/living conditions...")

            submit_complaint_btn = st.form_submit_button("🚀 Submit Complaint", use_container_width=True)

            if submit_complaint_btn:
                if not title_input or not desc_input or not location_input:
                    st.error("Please fill in all mandatory fields (Category, Priority, Location, Title, Description).")
                else:
                    saved_path = None
                    if uploaded_image:
                        saved_path = save_uploaded_file(uploaded_image)

                    success, res = create_complaint(
                        student_id=current_user["id"],
                        category=cat_input,
                        title=title_input,
                        description=desc_input,
                        location=location_input,
                        priority=prio_input,
                        image_path=saved_path
                    )
                    
                    if success:
                        st.balloons()
                        st.success(f"🎉 Complaint submitted successfully! Generated Ticket ID: **{res.id}**")
                    else:
                        st.error(f"Failed to submit complaint: {res}")
