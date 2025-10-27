"""Prompt detail page view."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp, toast


def render():
    """Render the prompt detail page."""
    db = get_db()
    
    # Get prompt ID from session state or query params
    prompt_id = st.session_state.get('prompt_id') or qp("id")
    if not prompt_id:
        st.error("Prompt not specified.")
        st.stop()
    
    prompt = db.get_prompt(prompt_id)
    if not prompt:
        st.error("Prompt not found.")
        st.stop()
    
    # Header with metadata
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# {prompt.get('title', 'Unnamed Prompt')}")
        st.markdown(prompt.get("description", "No description"))
    
    with col2:
        author = prompt.get("author_display_name_snapshot", "Unknown")
        rating = prompt.get("avg_rating", 0)
        uses = prompt.get("uses_total", 0)
        st.markdown(f"**By:** {author}")  
        st.markdown(f"**Rating:** ⭐ {rating:.1f}")
        st.markdown(f"**Uses:** {uses}")
    
    # View toggle
    view_options = ["CRAFT", "Full"]
    try:
        view_mode = st.radio("View", view_options, horizontal=True, index=0)
    except TypeError:
        # Fallback for older Streamlit
        view_mode = st.radio("View", view_options, index=0)
    
    # Get current user
    user_key = st.session_state.get("user_key", "guest")
    
    # Display content based on view mode
    if view_mode == "CRAFT":
        st.markdown("### Prompt Structure (CRAFT)")
        
        craft_sections = [
            ("Context", "craft_context"),
            ("Role", "craft_role"),
            ("Action", "craft_action"),
            ("Format", "craft_format"),
            ("Tone", "craft_tone")
        ]
        
        for label, field in craft_sections:
            st.markdown(f"**{label}:**")
            st.text_area(
                field,
                prompt.get(field, ""),
                key=f"view_{field}",
                disabled=True,
                label_visibility="collapsed"
            )
    else:
        # Full text view
        full_text = prompt.get("full_text", "")
        st.text_area("Full Text", full_text, disabled=True, height=300, label_visibility="collapsed")
    
    # Rating section
    st.markdown("### Rate this prompt")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        rating = st.slider("Your rating", 1, 5, 3)
        if st.button("Submit rating"):
            db.rate_prompt(user_key, prompt_id, rating)
            toast("Rating submitted!")
            st.rerun()
    
    with col2:
        avg_rating = prompt.get("avg_rating", 0)
        st.markdown(f"**Average rating:** ⭐ {avg_rating:.1f}")
    
    # Action buttons
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        full_text = prompt.get("full_text", "")
        
        # Try clipboard
        try:
            if st.button("COPY PROMPT", type="primary", use_container_width=True):
                st.clipboard(full_text)
                toast("Copied to clipboard!")
        except AttributeError:
            st.text_area("Copy manually:", full_text, height=100, key="copy_area")
    
    with col2:
        copilot_url = st.session_state.get("copilot_url", "https://copilot.microsoft.com")
        if st.button("OPEN COPILOT", use_container_width=True):
            import webbrowser
            webbrowser.open(copilot_url)
    
    with col3:
        is_bookmarked = db.is_bookmarked(user_key, prompt_id)
        bookmark_label = "♥ Save prompt" if is_bookmarked else "♡ Save prompt"
        
        if st.button(bookmark_label, use_container_width=True):
            added = db.toggle_bookmark(user_key, prompt_id)
            if added:
                toast("Saved to bookmarks!")
            else:
                toast("Removed from bookmarks!")
            st.rerun()

