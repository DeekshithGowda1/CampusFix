import os
import streamlit as st
from config import COMPLAINT_CATEGORIES, STATUS_LIST, PRIORITIES
from services.complaint_service import (
    get_complaints,
    update_complaint_status,
    add_comment
)
from services.utils import format_datetime
from components.ui_elements import render_header, render_kpi_card, get_status_badge_html, get_priority_badge_html, render_timeline

def render_staff_view(current_user):
    """Renders Staff Portal Interface."""
    render_header(
        f"🛠️ Staff Workspace — {current_user['name']}",
        f"Department: {current_user.get('department', 'General Maintenance')} | Manage assigned tickets & update progress"
    )

    # Fetch complaints for this staff member or unassigned in department
    my_tasks = get_complaints(user_role="STAFF", user_id=current_user["id"])
    
    total_assigned = len(my_tasks)
    in_prog_count = sum(1 for c in my_tasks if c.status in ["In Progress", "Assigned", "Under Review"])
    resolved_count = sum(1 for c in my_tasks if c.status == "Resolved")

    # KPI Metrics
    c_k1, c_k2, c_k3 = st.columns(3)
    with c_k1:
        render_kpi_card("Assigned Complaints", str(total_assigned), "My total workload")
    with c_k2:
        render_kpi_card("Active Tasks", str(in_prog_count), "In Progress or Assigned")
    with c_k3:
        render_kpi_card("Resolved Tasks", str(resolved_count), "Completed tickets")

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Bar
    st.subheader("Complaint Management Queue")
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_q = st.text_input("🔍 Search Tickets", placeholder="Search by ID, title, student name, or location...")
    with f_col2:
        status_f = st.selectbox("Status Filter", ["All"] + STATUS_LIST)
    with f_col3:
        prio_f = st.selectbox("Priority Filter", ["All"] + PRIORITIES)

    filtered_tasks = get_complaints(
        user_role="STAFF",
        user_id=current_user["id"],
        priority_filter=prio_f,
        status_filter=status_f,
        search_query=search_q
    )

    if not filtered_tasks:
        st.info("No complaint tickets found in your queue.")
    else:
        for ticket in filtered_tasks:
            status_badge = get_status_badge_html(ticket.status)
            prio_badge = get_priority_badge_html(ticket.priority)
            student_name = ticket.student.name if ticket.student else "Unknown Student"
            
            with st.expander(f"⚙️ [{ticket.id}] {ticket.title} — Student: {student_name}"):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.markdown(f"**Status:** {status_badge} &nbsp; {prio_badge}", unsafe_allow_html=True)
                    st.markdown(f"**Category:** `{ticket.category}` | **Location:** `{ticket.location}`")
                    st.markdown(f"**Submitted By:** {student_name} ({ticket.student.department if ticket.student else 'N/A'})")
                    st.markdown(f"**Submitted Date:** {format_datetime(ticket.created_at)}")
                    st.markdown(f"**Issue Description:**\n>{ticket.description}")
                    
                    if ticket.image_path and os.path.exists(ticket.image_path):
                        st.image(ticket.image_path, caption="Uploaded Evidence Photo", width=350)
                        
                    if ticket.satisfaction_rating:
                        st.success(f"🌟 Student Rating: {'⭐' * ticket.satisfaction_rating} ({ticket.satisfaction_rating}/5)")
                        if ticket.satisfaction_feedback:
                            st.caption(f'"{ticket.satisfaction_feedback}"')

                with c2:
                    st.markdown("##### ✏️ Update Ticket Status")
                    with st.form(f"status_update_form_{ticket.id}"):
                        new_status_val = st.selectbox(
                            "New Status",
                            ["Under Review", "In Progress", "Resolved", "Rejected"],
                            index=1 if ticket.status == "Assigned" else 0
                        )
                        update_note = st.text_area("Status Note / Resolution Detail", placeholder="Explain actions taken or reason for status change...")
                        submit_status_btn = st.form_submit_button("Update Status", use_container_width=True)

                        if submit_status_btn:
                            if not update_note.strip():
                                st.error("Please provide a note detailing the status update.")
                            else:
                                u_ok, u_msg = update_complaint_status(ticket.id, new_status_val, current_user["id"], update_note)
                                if u_ok:
                                    st.success(u_msg)
                                    st.rerun()

                # --- Timeline & Comments Tabs ---
                st.markdown("---")
                t_tab1, t_tab2 = st.tabs(["📜 Status Audit Log", "💬 Public & Internal Notes"])
                
                with t_tab1:
                    render_timeline(ticket.history)
                    
                with t_tab2:
                    all_comments = ticket.comments
                    if not all_comments:
                        st.caption("No notes or comments posted yet.")
                    else:
                        for cm in all_comments:
                            u_name = cm.user.name if cm.user else "User"
                            u_role = f"[{cm.user.role}]" if cm.user else ""
                            tag = "🔒 [INTERNAL NOTE]" if cm.is_internal else "💬 [PUBLIC]"
                            tag_color = "#b45309" if cm.is_internal else "#0369a1"
                            
                            st.markdown(f"<span style='color:{tag_color}; font-weight:bold;'>{tag}</span> **{u_name}** {u_role} • <span style='font-size:0.8rem; color:#64748b;'>{format_datetime(cm.created_at)}</span>", unsafe_allow_html=True)
                            st.write(cm.message)
                            st.markdown("<hr style='margin:0.4rem 0;'>", unsafe_allow_html=True)
                            
                    with st.form(f"staff_comment_{ticket.id}"):
                        comment_txt = st.text_area("Post a note or student message", height=70)
                        is_internal_chk = st.checkbox("Mark as Staff-Only Internal Note (hidden from student)")
                        post_staff_cm = st.form_submit_button("Post Note")
                        
                        if post_staff_cm:
                            if not comment_txt.strip():
                                st.error("Note cannot be empty.")
                            else:
                                add_ok, add_msg = add_comment(ticket.id, current_user["id"], comment_txt, is_internal=is_internal_chk)
                                if add_ok:
                                    st.success(add_msg)
                                    st.rerun()
