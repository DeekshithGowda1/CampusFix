import streamlit as st
from services.utils import format_datetime

def render_header(title: str, subtitle: str):
    """Renders the top gradient header banner."""
    st.markdown(
        f"""
        <div class="cf-header-banner">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpi_card(title: str, value: str, subtext: str = ""):
    """Renders a styled KPI metric box."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def get_status_badge_html(status: str) -> str:
    """Returns HTML for status badge."""
    mapping = {
        "Submitted": "badge-submitted",
        "Under Review": "badge-review",
        "Assigned": "badge-assigned",
        "In Progress": "badge-inprogress",
        "Resolved": "badge-resolved",
        "Rejected": "badge-rejected"
    }
    css_class = mapping.get(status, "badge-submitted")
    return f'<span class="status-badge {css_class}">{status}</span>'

def get_priority_badge_html(priority: str) -> str:
    """Returns HTML for priority badge."""
    mapping = {
        "Low": "badge-prio-low",
        "Medium": "badge-prio-medium",
        "High": "badge-prio-high",
        "Critical": "badge-prio-critical"
    }
    css_class = mapping.get(priority, "badge-prio-medium")
    return f'<span class="status-badge {css_class}">Priority: {priority}</span>'

def render_timeline(history_items):
    """Renders visual complaint audit trail / timeline."""
    if not history_items:
        st.info("No status history available yet.")
        return
        
    for h in history_items:
        updater_name = h.updated_by.name if h.updated_by else "System"
        updater_role = f"({h.updated_by.role})" if h.updated_by else ""
        time_str = format_datetime(h.timestamp)
        badge_html = get_status_badge_html(h.status)
        
        st.markdown(
            f"""
            <div class="timeline-item">
                <div>{badge_html} <strong>by {updater_name}</strong> {updater_role}</div>
                <div class="timeline-time">⏱️ {time_str}</div>
                <div class="timeline-note">{h.status_note or ''}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
