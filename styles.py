import streamlit as st

def apply_custom_css():
    """Injects modern, polished custom CSS for CampusFix UI."""
    css = """
    <style>
    /* Global Page Styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Header Gradient Banner */
    .cf-header-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1.8rem 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
    }
    
    .cf-header-banner h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .cf-header-banner p {
        font-size: 1.05rem;
        opacity: 0.9;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }
    
    /* KPI Card Component */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        font-weight: 600;
    }
    
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0.3rem;
        margin-bottom: 0.2rem;
    }
    
    .kpi-sub {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    /* Custom Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-submitted { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
    .badge-review { background-color: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
    .badge-assigned { background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
    .badge-inprogress { background-color: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .badge-resolved { background-color: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-rejected { background-color: #ffe4e6; color: #be123c; border: 1px solid #fecdd3; }
    
    /* Priority Badges */
    .badge-prio-low { background-color: #ecfdf5; color: #047857; font-weight: 600; }
    .badge-prio-medium { background-color: #f0f9ff; color: #0284c7; font-weight: 600; }
    .badge-prio-high { background-color: #fff7ed; color: #c2410c; font-weight: 600; }
    .badge-prio-critical { background-color: #fef2f2; color: #b91c1c; font-weight: 700; border: 1px solid #fecaca; }
    
    /* Complaint Card Container */
    .complaint-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Timeline Node Styling */
    .timeline-item {
        border-left: 3px solid #3b82f6;
        padding-left: 1.2rem;
        margin-left: 0.5rem;
        margin-bottom: 1.2rem;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 3px;
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background-color: #3b82f6;
    }

    .timeline-time {
        font-size: 0.78rem;
        color: #64748b;
    }

    .timeline-note {
        font-size: 0.9rem;
        color: #334155;
        margin-top: 0.2rem;
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 500;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
