"""Category page view."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp


def render():
    """Render the category page."""
    db = get_db()
    
    # Get category from session state or query params
    cat_id = st.session_state.get('category_id') or qp("cat")
    if not cat_id:
        st.error("Category not specified.")
        st.stop()
    
    category = db.get_category(cat_id)
    if not category:
        st.error("Category not found.")
        st.stop()
    
    # Header
    st.markdown(f"## {category['name']}")
    
    # Get prompts for this category
    prompts = db.list_prompts(category_id=cat_id)
    
    # Sort options
    sort_options = ["Highest rated", "Most used", "Recently added"]
    try:
        selected_sort = st.radio("Sort by", sort_options, horizontal=True, index=0)
    except TypeError:
        selected_sort = st.radio("Sort by", sort_options, index=0)
    
    # Apply sorting
    if selected_sort == "Highest rated":
        prompts = sorted(prompts, key=lambda x: x.get("avg_rating", 0), reverse=True)
    elif selected_sort == "Most used":
        prompts = sorted(prompts, key=lambda x: x.get("uses_total", 0), reverse=True)
    elif selected_sort == "Recently added":
        prompts = sorted(prompts, key=lambda x: x.get("created_at", ""), reverse=True)
    
    # Display prompts as cards
    if not prompts:
        st.info("No prompts in this category yet.")
        if st.button("Create one", type="primary"):
            st.session_state['nav_view'] = 'new'
            st.session_state['nav_cat'] = cat_id
            st.rerun()
        return
    
    # Get current user
    user_key = st.session_state.get("user_key", "guest")
    
    for prompt in prompts:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {prompt.get('title', 'Unnamed Prompt')}")
                st.markdown(prompt.get("description", "No description"))
                
                # Author and rating
                author = prompt.get("author_display_name_snapshot", "Unknown")
                rating = prompt.get("avg_rating", 0)
                uses = prompt.get("uses_total", 0)
                
                st.markdown(f"*{author}* | ⭐ {rating:.1f} | Uses: {uses}")
            
            with col2:
                if st.button("Open", key=f"open_{prompt['id']}", use_container_width=True):
                    st.session_state['nav_view'] = 'prompt'
                    st.session_state['nav_id'] = prompt["id"]
                    st.rerun()
                
                # Bookmark button
                is_bookmarked = db.is_bookmarked(user_key, prompt["id"])
                bookmark_label = "★ Bookmarked" if is_bookmarked else "☆ Bookmark"
                
                if st.button(bookmark_label, key=f"bookmark_{prompt['id']}", use_container_width=True):
                    added = db.toggle_bookmark(user_key, prompt["id"])
                    st.rerun()
            
            st.divider()

