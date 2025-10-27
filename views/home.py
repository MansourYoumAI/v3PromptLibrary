"""Home page view."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp


def render():
    """Render the home page."""
    db = get_db()
    
    # Header
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        st.markdown(f"## {st.session_state.get('app_name', 'AI PROMPT STUDIO')}")
    with col3:
        if st.button("CREATE PROMPT", type="primary"):
            st.session_state['nav_view'] = 'new'
            st.rerun()
    
    # Search bar
    search_query = st.text_input("Search", placeholder="Search for prompts...")
    
    # Get categories
    metiers = db.list_metiers()
    if not metiers:
        st.info("No categories available.")
        return
    
    # Assume first metier for v1 (Sales)
    metier = metiers[0]
    categories = db.list_categories(metier["id"])
    
    # Build category cards with top prompts
    prompts = db.list_prompts(metier_id=metier["id"])
    
    # Apply search filter
    if search_query:
        search_terms = search_query.lower().split()
        filtered_prompts = []
        for p in prompts:
            search_text = f"{p.get('title', '')} {p.get('description', '')} {p.get('full_text', '')} {p.get('author_display_name_snapshot', '')}".lower()
            if all(term in search_text for term in search_terms):
                filtered_prompts.append(p)
        prompts = filtered_prompts
    
    # Create category cards
    st.markdown("### Prompt Categories")
    
    # Display in grid (3 columns)
    cols = st.columns(3)
    
    for idx, category in enumerate(categories[:6]):  # Limit to 6 categories
        col = cols[idx % 3]
        
        with col:
            # Get top 3 prompts for this category
            cat_prompts = [p for p in prompts if p.get("category_id") == category["id"]]
            cat_prompts = sorted(cat_prompts, key=lambda x: x.get("avg_rating", 0), reverse=True)[:3]
            
            with st.container():
                st.markdown(f"**{category['name']}**")
                for i, prompt in enumerate(cat_prompts):
                    if st.button(prompt.get("title", "Unnamed Prompt"), 
                               key=f"cat_{category['id']}_prompt_{i}",
                               use_container_width=True):
                        st.session_state['nav_view'] = 'prompt'
                        st.session_state['nav_id'] = prompt["id"]
                        st.rerun()
                
                if not cat_prompts:
                    st.markdown("*No prompts yet*")
                
                # Link to category page
                if st.button(f"View {category['name']}", key=f"view_cat_{category['id']}"):
                    st.session_state['nav_view'] = 'category'
                    st.session_state['nav_cat'] = category["id"]
                    st.rerun()

