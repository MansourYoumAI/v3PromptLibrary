"""My submitted prompts page view."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp


def render():
    """Render my submitted prompts page."""
    db = get_db()
    
    # Get current user
    user_key = st.session_state.get("user_key", "guest")
    
    st.markdown("## My Submitted Prompts")
    
    # Get user's submissions
    all_subs = db.list_submissions()
    user_subs = [s for s in all_subs if s.get("created_by") == user_key]
    
    if not user_subs:
        st.info("You haven't submitted any prompts yet.")
        
        if st.button("Create Your First Prompt", type="primary"):
            st.query_params.view = "new"
            st.rerun()
        return
    
    # Display submissions with status
    for submission in user_subs:
        with st.container():
            status = submission.get("status", "pending")
            
            # Status chip
            if status == "pending":
                st.info("⏳ Pending Review")
            elif status == "approved":
                st.success("✓ Approved")
            elif status == "rejected":
                st.error("✗ Rejected")
            
            st.markdown(f"### {submission.get('title', 'Unnamed')}")
            st.markdown(submission.get("description", "No description"))
            
            # Expandable preview
            with st.expander("View Full Text"):
                st.text(submission.get("full_text", ""))
            
            if submission.get("review_comment"):
                st.caption(f"Review comment: {submission['review_comment']}")
            
            st.divider()

