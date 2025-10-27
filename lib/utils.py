"""Utility functions for logging, normalization, and helpers."""

import re
import csv
import os
from datetime import datetime
from typing import Optional
import streamlit as st

def normalize_key(name: str) -> str:
    """Normalize a name to a URL-friendly key.
    
    Args:
        name: The display name to normalize
        
    Returns:
        Lowercase key with special characters replaced by hyphens
    """
    if not name:
        return ""
    # Remove accents, convert to lowercase, replace non-alphanumeric with hyphens
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')
    return name


def write_log(event: str, user_key: str = "", meta: dict | None = None) -> None:
    """Write an event to the logs CSV file.
    
    Args:
        event: Event name (e.g., 'view_prompt', 'create_submission')
        user_key: User identifier
        meta: Optional metadata dictionary
    """
    if meta is None:
        meta = {}
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Get today's date for filename
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if we need to rotate (keep file size reasonable)
    log_file = f"logs/{today}.csv"
    part_num = 1
    
    # Find available filename
    while os.path.exists(log_file):
        file_size = os.path.getsize(log_file)
        if file_size > 10 * 1024 * 1024:  # 10 MB threshold
            part_num += 1
            log_file = f"logs/{today}_part{part_num}.csv"
        else:
            break
    
    # Prepare row data
    row = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "user_key": user_key,
        **meta
    }
    
    # Write to CSV
    file_exists = os.path.exists(log_file)
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['timestamp', 'event', 'user_key'] + list(meta.keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row)


def purge_old_logs(days: int = 90) -> None:
    """Remove log files older than specified days.
    
    Args:
        days: Number of days to keep logs (default 90)
    """
    if not os.path.exists("logs"):
        return
    
    cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
    
    for filename in os.listdir("logs"):
        file_path = os.path.join("logs", filename)
        if os.path.getmtime(file_path) < cutoff_date:
            try:
                os.remove(file_path)
            except OSError:
                pass


def toast(msg: str) -> None:
    """Display a toast notification with fallback.
    
    Args:
        msg: Message to display
    """
    try:
        st.toast(msg)
    except AttributeError:
        st.info(msg)


def link_btn(label: str, url: str) -> None:
    """Create a link button with fallback.
    
    Args:
        label: Button label
        url: URL to navigate to
    """
    try:
        st.link_button(label, url)
    except AttributeError:
        st.markdown(f"[{label}]({url})")


def qp(key: str, default: Optional[str] = None) -> Optional[str]:
    """Robust query parameter getter.
    
    Args:
        key: Parameter name
        default: Default value if not found
        
    Returns:
        Parameter value or default
    """
    try:
        value = st.query_params.get(key)
        if value is None:
            return default
        if isinstance(value, list):
            return value[0] if value else default
        return value
    except AttributeError:
        try:
            params = st.experimental_get_query_params()
            value = params.get(key, [default])
            return value[0] if isinstance(value, list) else value
        except AttributeError:
            return default


