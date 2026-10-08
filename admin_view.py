import streamlit as st
import pandas as pd
from config import COMPLAINT_CATEGORIES, PRIORITIES, STATUS_LIST
from analytics_service import (
    get_summary_kpis,
    get_complaints_dataframe,
    create_category_pie_chart,
    create_status_bar_chart,
    create_priority_donut_chart,
    get_staff_performance_dataframe
)
from complaint_service import (
    get_complaints,
    assign_complaint,
    update_complaint_status
)
from user_service import get_all_staff, get_all_users, create_staff_member
from utils import export_to_csv, format_datetime
from ui_elements import render_header, render_kpi_card, get_status_badge_html, get_priority_badge_html

def render_admin_view(current_user):
    """Renders Admin Dashboard & Operations Portal."""
    render_header(
        "👑 Administrator Command Center",
        "Overview campus analytics, assign technician tickets, manage users, and export reports."
    )

    # 1. Summary KPIs
    kpis = get_summary_kpis()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Complaints", str(kpis["total"]), "Lifetime registered")
    with c2:
        render_kpi_card("Active / Pending", str(kpis["submitted"] + kpis["in_progress"]), "Awaiting action")
    with c3:
        render_kpi_card("Resolution Rate", f"{kpis['resolution_rate']}%", f"{kpis['resolved']} resolved")
    with c4:
        render_kpi_card("Avg Resolution SLA", f"{kpis['avg_sla_hours']} hrs", "Turnaround time")

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Navigation Tabs
    tab_analytics, tab_assign, tab_users, tab_reports = st.tabs([
        "📊 Analytics & Charts",
        "🎯 Ticket Assignment Center",
        "👥 User Management",
        "📑 Reports & Data Export"
    ])

    # --- TAB 1: ANALYTICS & CHARTS ---
    with tab_analytics:
        st.subheader("Campus Issue Visual Analytics")
        df_complaints = get_complaints_dataframe()

        if df_complaints.empty:
            st.info("No complaint data available for analysis.")
        else:
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                fig_cat = create_category_pie_chart(df_complaints)
                st.plotly_chart(fig_cat, use_container_width=True)
            with g_col2:
                fig_prio = create_priority_donut_chart(df_complaints)
                st.plotly_chart(fig_prio, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            fig_status = create_status_bar_chart(df_complaints)
            st.plotly_chart(fig_status, use_container_width=True)

    # --- TAB 2: TICKET ASSIGNMENT CENTER ---
    with tab_assign:
        st.subheader("Assign & Manage Complaints")
        staff_members = get_all_staff()
        if not staff_members:
            st.warning("No staff members available. Please create staff accounts in the 'User Management' tab first.")
        
        staff_dict = {f"{s.name} ({s.department})": s.id for s in staff_members}
        
        # Filter controls
        af_col1, af_col2 = st.columns(2)
        with af_col1:
            assign_status_filter = st.selectbox("Filter Status", ["All", "Submitted", "Under Review", "Assigned", "In Progress"])
        with af_col2:
            assign_cat_filter = st.selectbox("Filter Category", ["All"] + COMPLAINT_CATEGORIES)

        assignable_complaints = get_complaints(
            user_role="ADMIN",
            category_filter=assign_cat_filter,
            status_filter=assign_status_filter
        )

        if not assignable_complaints:
            st.info("No complaints found for assignment.")
        else:
            for complaint in assignable_complaints:
                status_b = get_status_badge_html(complaint.status)
                prio_b = get_priority_badge_html(complaint.priority)
                curr_staff = complaint.assigned_staff.name if complaint.assigned_staff else "⚠️ Unassigned"
                
                with st.expander(f"📌 [{complaint.id}] {complaint.title} | Current Staff: {curr_staff}"):
                    ac1, ac2 = st.columns([2, 1])
                    with ac1:
                        st.markdown(f"**Status:** {status_b} &nbsp; {prio_b}", unsafe_allow_html=True)
                        st.markdown(f"**Category:** `{complaint.category}` | **Location:** `{complaint.location}`")
                        st.markdown(f"**Submitted By:** {complaint.student.name if complaint.student else 'Unknown'} ({format_datetime(complaint.created_at)})")
                        st.markdown(f"**Description:**\n>{complaint.description}")

                    with ac2:
                        st.markdown("##### 👥 Staff Assignment")
                        with st.form(f"assign_form_{complaint.id}"):
                            selected_staff_label = st.selectbox("Select Staff Member", list(staff_dict.keys()))
                            assign_note = st.text_input("Assignment Note", placeholder="e.g. Priority dispatch to room 204")
                            submit_assign = st.form_submit_button("Assign Staff", use_container_width=True)

                            if submit_assign:
                                target_staff_id = staff_dict[selected_staff_label]
                                a_ok, a_msg = assign_complaint(complaint.id, target_staff_id, current_user["id"], assign_note)
                                if a_ok:
                                    st.success(a_msg)
                                    st.rerun()

    # --- TAB 3: USER MANAGEMENT ---
    with tab_users:
        st.subheader("Manage System Users & Staff")
        
        u_tab1, u_tab2 = st.tabs(["➕ Add New Staff", "📋 User Directory"])
        
        with u_tab1:
            st.markdown("##### Create Staff Account")
            with st.form("create_staff_form", clear_on_submit=True):
                sc1, sc2 = st.columns(2)
                with sc1:
                    s_name = st.text_input("Staff Full Name *")
                    s_email = st.text_input("Staff Email *", placeholder="e.g. name@campusfix.edu")
                    s_pass = st.text_input("Initial Password *", type="password")
                with sc2:
                    s_dept = st.selectbox("Department *", COMPLAINT_CATEGORIES)
                    s_phone = st.text_input("Phone Number")

                submit_staff_btn = st.form_submit_button("Create Staff Member", use_container_width=True)

                if submit_staff_btn:
                    if not s_name or not s_email or not s_pass:
                        st.error("Please fill in all mandatory fields.")
                    else:
                        st_ok, st_res = create_staff_member(s_name, s_email, s_pass, s_dept, s_phone)
                        if st_ok:
                            st.success(f"Staff member **{s_name}** created successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to create staff member: {st_res}")

        with u_tab2:
            st.markdown("##### Registered User Directory")
            all_users = get_all_users()
            user_data = [{
                "ID": u.id,
                "Name": u.name,
                "Email": u.email,
                "Role": u.role,
                "Department": u.department or "N/A",
                "Phone": u.phone or "N/A",
                "Joined": format_datetime(u.created_at)
            } for u in all_users]
            
            st.dataframe(pd.DataFrame(user_data), use_container_width=True)

    # --- TAB 4: REPORTS & DATA EXPORT ---
    with tab_reports:
        st.subheader("Reports & Raw Data Export")
        
        df_all = get_complaints_dataframe()
        st.markdown("##### Master Complaints Dataset")
        st.dataframe(df_all, use_container_width=True)
        
        csv_bytes = export_to_csv(df_all)
        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv_bytes,
            file_name=f"CampusFix_Complaints_Report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("---")
        st.markdown("##### Staff Performance & Workload Metrics")
        df_staff_perf = get_staff_performance_dataframe()
        st.dataframe(df_staff_perf, use_container_width=True)
