"""Admin monitoring and review page view."""

import streamlit as st
import pandas as pd
from lib.data_store import get_db
from lib.utils import qp, toast
import os


def render():
    """Render the admin page."""
    db = get_db()
    
    # Header
    st.markdown("# AI PROMPT STUDIO - ADMIN")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Pending", "Published", "Categories", "Logs"])
    
    # TAB 1: Pending Submissions
    with tab1:
        st.markdown("## All Prompts - Pending Review")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Export all data (.csv)"):
                # Export logic would go here
                toast("Export functionality coming soon")
        
        # View filter
        submissions = db.list_submissions()
        
        # Display submissions
        if not submissions:
            st.info("No pending submissions.")
        else:
            for sub in submissions:
                with st.container():
                    status = sub.get("status", "pending")
                    status_color = {
                        "pending": "🟠",
                        "approved": "🟢",
                        "rejected": "🔴"
                    }.get(status, "⚪")
                    
                    col1, col2, col3 = st.columns([4, 1, 1])
                    
                    with col1:
                        st.markdown(f"{status_color} **{sub.get('title', 'Unnamed')}**")
                        st.caption(sub.get("description", "No description"))
                    
                    with col2:
                        if st.button("Review", key=f"review_{sub['id']}", use_container_width=True):
                            st.session_state["admin_review_id"] = sub["id"]
                            st.rerun()
                    
                    with col3:
                        if status == "pending":
                            if st.button("Approve", key=f"approve_{sub['id']}", use_container_width=True, type="primary"):
                                db.approve_submission(sub["id"])
                                toast("Approved and published!")
                                st.rerun()
                        elif status == "rejected":
                            st.caption("Rejected")
                    
                    st.divider()
    
    # TAB 2: Published Prompts
    with tab2:
        st.markdown("## All Published Prompts")
        
        prompts = db.list_prompts()
        
        if not prompts:
            st.info("No published prompts.")
        else:
            # Create dataframe
            data = []
            for p in prompts:
                data.append({
                    "ID": p["id"][:8] + "...",
                    "Title": p.get("title", ""),
                    "Category": p.get("category_name", ""),
                    "Author": p.get("author_display_name_snapshot", ""),
                    "Rating": f"{p.get('avg_rating', 0):.1f}",
                    "Uses": p.get("uses_total", 0),
                    "Version": p.get("version", "1.0")
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Export button
            if st.button("Export as CSV", key="export_published"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "published_prompts.csv", "text/csv")
    
    # TAB 3: Categories
    with tab3:
        st.markdown("## All Categories")
        
        metiers = db.list_metiers()
        if not metiers:
            st.info("No metiers available.")
        else:
            metier = metiers[0]  # v1: Sales only
            
            # List existing categories
            categories = db.list_categories(metier["id"])
            
            if categories:
                st.markdown("### Existing Categories")
                for cat in categories:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"- {cat['name']}")
                    with col2:
                        st.caption(cat["id"])
            
            st.divider()
            
            # Create new category
            st.markdown("### Create New Category")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                new_cat_name = st.text_input("Category name", placeholder="Enter category name")
            
            with col2:
                if st.button("CREATE CATEGORY", type="primary"):
                    if new_cat_name:
                        db.get_or_create_category(metier["id"], new_cat_name)
                        toast(f"Category '{new_cat_name}' created!")
                        st.rerun()
    
    # TAB 4: Logs
    with tab4:
        st.markdown("## Logs")
        
        log_files = []
        if os.path.exists("logs"):
            log_files = [f for f in os.listdir("logs") if f.endswith(".csv")]
        
        if not log_files:
            st.info("No log files yet.")
        else:
            selected_log = st.selectbox("Select log file", log_files)
            
            if selected_log:
                df = pd.read_csv(f"logs/{selected_log}")
                st.dataframe(df, use_container_width=True)
                
                # Export button
                csv = df.to_csv(index=False)
                st.download_button("Export CSV", csv, selected_log, "text/csv")


def render_review():
    """Render the detailed review/edit view."""
    db = get_db()
    
    review_id = st.session_state.get("admin_review_id")
    if not review_id:
        st.error("No submission selected for review.")
        if st.button("Back to Admin"):
            st.session_state.pop("admin_review_id", None)
            st.rerun()
        return
    
    submission = db.get_submission(review_id)
    if not submission:
        st.error("Submission not found.")
        return
    
    # Header with actions
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# Review Prompt: {submission.get('title', 'Unnamed')}")
    with col2:
        if submission.get("status") == "pending":
            if st.button("✓ Publish", type="primary"):
                db.approve_submission(review_id)
                toast("Published!")
                st.session_state.pop("admin_review_id", None)
                st.rerun()
            
            if st.button("✗ Reject"):
                db.reject_submission(review_id)
                toast("Rejected")
                st.rerun()
    
    # Edit title and description
    st.markdown("### Prompt Information")
    st.text_input("Prompt name", value=submission.get("title", ""), disabled=True)
    st.text_area("Description text", value=submission.get("description", ""), disabled=True)
    
    # View toggle
    try:
        view_mode = st.radio("View", ["CRAFT", "Full"], horizontal=True, index=0)
    except TypeError:
        view_mode = st.radio("View", ["CRAFT", "Full"], index=0)
    
    # Display content (view_mode set from radio button above)
    if view_mode == "CRAFT":
        for field_name, field_label in [
            ("craft_context", "[CONTEXT]"),
            ("craft_role", "[ROLE]"),
            ("craft_action", "[ACTION]"),
            ("craft_format", "[FORMAT]"),
            ("craft_tone", "[TONE]")
        ]:
            st.text_area(field_label, value=submission.get(field_name, ""), disabled=True)
    else:
        st.text_area("Full Text", value=submission.get("full_text", ""), disabled=True, height=300)
    
    # Back button
    if st.button("← Back to Admin"):
        st.session_state.pop("admin_review_id", None)
        st.rerun()

