"""My saved bookmarks page view."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp


def render():
    """Render my saved bookmarks page."""
    db = get_db()
    
    # Get current user
    user_key = st.session_state.get("user_key", "guest")
    
    st.markdown("## My Saved Prompts")
    
    bookmarks = db.list_bookmarks(user_key)
    
    if not bookmarks:
        st.info("You haven't saved any prompts yet.")
        return
    
    # Display bookmarks
    for prompt in bookmarks:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {prompt.get('title', 'Unnamed Prompt')}")
                st.markdown(prompt.get("description", "No description"))
                st.markdown(f"*{prompt.get('category_name', 'Unknown')}*")
            
            with col2:
                if st.button("Open", key=f"open_{prompt['id']}", use_container_width=True):
                    st.session_state['nav_view'] = 'prompt'
                    st.session_state['nav_id'] = prompt["id"]
                    st.rerun()
                
                if st.button("Remove", key=f"remove_{prompt['id']}", use_container_width=True):
                    db.toggle_bookmark(user_key, prompt["id"])
                    st.rerun()
            
            st.divider()

