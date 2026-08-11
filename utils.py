import os
import uuid
import pandas as pd
from datetime import datetime
from config import UPLOAD_DIR

def save_uploaded_file(uploaded_file):
    """Saves uploaded Streamlit image/evidence file with unique name and returns path."""
    if uploaded_file is None:
        return None
    
    ext = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"ev_{uuid.uuid4().hex[:10]}_{int(datetime.utcnow().timestamp())}{ext}"
    full_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(full_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return full_path

def format_datetime(dt):
    """Formats datetime nicely for UI display."""
    if dt is None:
        return "N/A"
    return dt.strftime("%b %d, %Y at %I:%M %p")

def export_to_csv(df: pd.DataFrame) -> bytes:
    """Converts a pandas DataFrame to CSV bytes for download button."""
    return df.to_csv(index=False).encode('utf-8')
