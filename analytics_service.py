import pandas as pd
import plotly.express as px
import plotly.graph_objects as bg
from database import SessionLocal
from models import Complaint, User

def get_complaints_dataframe():
    """Extracts all complaints from DB into a Pandas DataFrame for reports & exports."""
    db = SessionLocal()
    try:
        complaints = db.query(Complaint).all()
        data = []
        for c in complaints:
            student_name = c.student.name if c.student else "Unknown"
            staff_name = c.assigned_staff.name if c.assigned_staff else "Unassigned"
            
            # Calculate resolution SLA in hours if resolved
            sla_hours = None
            if c.resolved_at and c.created_at:
                sla_hours = round((c.resolved_at - c.created_at).total_seconds() / 3600.0, 1)
                
            data.append({
                "Complaint ID": c.id,
                "Student": student_name,
                "Category": c.category,
                "Title": c.title,
                "Location": c.location,
                "Priority": c.priority,
                "Status": c.status,
                "Assigned Staff": staff_name,
                "Rating (1-5)": c.satisfaction_rating if c.satisfaction_rating else "N/A",
                "Resolution Time (Hrs)": sla_hours if sla_hours is not None else "N/A",
                "Created At": c.created_at.strftime("%Y-%m-%d %H:%M"),
                "Resolved At": c.resolved_at.strftime("%Y-%m-%d %H:%M") if c.resolved_at else "N/A"
            })
        return pd.DataFrame(data)
    finally:
        db.close()

def get_summary_kpis():
    """Calculates top-level KPI metrics for dashboards."""
    db = SessionLocal()
    try:
        total = db.query(Complaint).count()
        submitted = db.query(Complaint).filter_by(status="Submitted").count()
        in_progress = db.query(Complaint).filter(Complaint.status.in_(["Assigned", "In Progress", "Under Review"])).count()
        resolved = db.query(Complaint).filter_by(status="Resolved").count()
        rejected = db.query(Complaint).filter_by(status="Rejected").count()
        
        resolution_rate = round((resolved / total * 100), 1) if total > 0 else 0.0
        
        # Calculate average SLA resolution time
        resolved_complaints = db.query(Complaint).filter(Complaint.resolved_at.isnot(None)).all()
        if resolved_complaints:
            diffs = [(c.resolved_at - c.created_at).total_seconds() / 3600.0 for c in resolved_complaints if c.created_at]
            avg_sla_hours = round(sum(diffs) / len(diffs), 1)
        else:
            avg_sla_hours = 0.0

        return {
            "total": total,
            "submitted": submitted,
            "in_progress": in_progress,
            "resolved": resolved,
            "rejected": rejected,
            "resolution_rate": resolution_rate,
            "avg_sla_hours": avg_sla_hours
        }
    finally:
        db.close()

def create_category_pie_chart(df: pd.DataFrame):
    """Generates Plotly Pie Chart for Category Distribution."""
    if df.empty:
        return px.pie(title="No Complaint Data Available")
        
    cat_counts = df["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    
    fig = px.pie(
        cat_counts,
        names="Category",
        values="Count",
        title="Complaints by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textinfo="percent+label", hovertemplate="<b>%{label}</b><br>Count: %{value}")
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10), legend=dict(orientation="h", y=-0.1))
    return fig

def create_status_bar_chart(df: pd.DataFrame):
    """Generates Plotly Bar Chart for Complaint Status Distribution."""
    if df.empty:
        return px.bar(title="No Complaint Data Available")
        
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    
    color_map = {
        "Submitted": "#6c757d",
        "Under Review": "#ffc107",
        "Assigned": "#17a2b8",
        "In Progress": "#0d6efd",
        "Resolved": "#198754",
        "Rejected": "#dc3545"
    }
    
    fig = px.bar(
        status_counts,
        x="Status",
        y="Count",
        title="Complaints by Current Status",
        color="Status",
        color_discrete_map=color_map,
        text="Count"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10), showlegend=False)
    return fig

def create_priority_donut_chart(df: pd.DataFrame):
    """Generates Plotly Donut Chart for Priority Breakdown."""
    if df.empty:
        return px.pie(title="No Complaint Data Available")
        
    prio_counts = df["Priority"].value_counts().reset_index()
    prio_counts.columns = ["Priority", "Count"]
    
    color_map = {
        "Low": "#28a745",
        "Medium": "#17a2b8",
        "High": "#fd7e14",
        "Critical": "#dc3545"
    }
    
    fig = px.pie(
        prio_counts,
        names="Priority",
        values="Count",
        title="Priority Breakdown",
        hole=0.5,
        color="Priority",
        color_discrete_map=color_map
    )
    fig.update_traces(textinfo="value+percent")
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    return fig

def get_staff_performance_dataframe():
    """Calculates staff workload, resolution stats, and feedback rating."""
    db = SessionLocal()
    try:
        staff_members = db.query(User).filter_by(role="STAFF").all()
        data = []
        for s in staff_members:
            assigned = db.query(Complaint).filter_by(assigned_staff_id=s.id).all()
            total_assigned = len(assigned)
            resolved_count = sum(1 for c in assigned if c.status == "Resolved")
            in_prog_count = sum(1 for c in assigned if c.status in ["In Progress", "Assigned", "Under Review"])
            
            ratings = [c.satisfaction_rating for c in assigned if c.satisfaction_rating is not None]
            avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else "N/A"
            
            data.append({
                "Staff Name": s.name,
                "Department": s.department,
                "Total Assigned": total_assigned,
                "In Progress": in_prog_count,
                "Resolved": resolved_count,
                "Avg Satisfaction": avg_rating
            })
        return pd.DataFrame(data)
    finally:
        db.close()
