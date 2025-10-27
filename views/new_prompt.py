"""Create new prompt page view."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp, toast


def render():
    """Render the create prompt page."""
    db = get_db()
    
    # Header
    st.markdown(f"## Create New Prompt")
    
    # Get current user
    user_key = st.session_state.get("user_key", "guest")
    
    # Get metiers and categories
    metiers = db.list_metiers()
    if not metiers:
        st.error("No metiers available.")
        st.stop()
    
    metier = metiers[0]  # v1: Sales only
    categories = db.list_categories(metier["id"])
    
    # Pre-selected category from session state or query param
    selected_cat_id = st.session_state.get('category_id') or qp("cat")
    if selected_cat_id:
        cat_names = {c["name"]: c["id"] for c in categories}
    else:
        cat_names = {c["name"]: c["id"] for c in categories}
        selected_cat_id = None
    
    # Form fields
    title = st.text_input("Prompt name")
    description = st.text_area("Description text", height=100)
    
    # Category selection
    cat_display_names = list(cat_names.keys()) + ["+ Create new category..."]
    cat_index = 0
    if selected_cat_id:
        for idx, cat in enumerate(categories):
            if cat["id"] == selected_cat_id:
                cat_index = idx
                break
    
    selected_cat_display = st.selectbox("Category", cat_display_names, index=cat_index)
    
    if selected_cat_display == "+ Create new category...":
        new_cat_name = st.text_input("New category name")
        if new_cat_name:
            category = db.get_or_create_category(metier["id"], new_cat_name)
            category_id = category["id"]
            category_name = category["name"]
    elif selected_cat_display in cat_names:
        category_id = cat_names[selected_cat_display]
        category_name = selected_cat_display
    else:
        st.warning("Please select a category.")
        category_id = None
        category_name = None
    
    # Author selection
    authors = db.list_authors()
    author_names = {a["display_name"]: a["id"] for a in authors}
    author_display = st.selectbox("Author", list(author_names.keys()) + ["+ Create new author..."])
    
    if author_display == "+ Create new author...":
        new_author_name = st.text_input("New author name")
        if new_author_name:
            author = db.get_or_create_author(new_author_name)
            author_id = author["id"]
            author_display_name_snapshot = author["display_name"]
    else:
        author_id = author_names.get(author_display)
        author_display_name_snapshot = author_display
    
    # CRAFT fields
    st.markdown("### CRAFT Fields")
    
    craft_context = st.text_area("[CONTEXT]", height=100)
    craft_role = st.text_area("[ROLE]", height=100)
    craft_action = st.text_area("[ACTION]", height=100)
    craft_format = st.text_area("[FORMAT]", height=100)
    craft_tone = st.text_area("[TONE]", height=100)
    
    # Count filled fields
    filled_fields = sum([
        bool(craft_context),
        bool(craft_role),
        bool(craft_action),
        bool(craft_format),
        bool(craft_tone)
    ])
    st.progress(filled_fields / 5)
    st.caption(f"Progress: {filled_fields}/5 fields filled")
    
    # Tags (optional)
    tags_input = st.text_input("Tags (5 max)", placeholder="tag1, tag2, tag3")
    
    # Preview full text
    if st.button("Preview Full Text"):
        full_text = f"{craft_context}\n\n{craft_role}\n\n{craft_action}\n\n{craft_format}\n\n{craft_tone}"
        st.text_area("Preview", full_text, height=300, disabled=True)
    
    # Save button
    if st.button("SAVE PROMPT", type="primary"):
        # Validation
        if not title:
            st.error("Please enter a prompt name.")
            return
        if not description:
            st.error("Please enter a description.")
            return
        if not category_id:
            st.error("Please select or create a category.")
            return
        if not author_id:
            st.error("Please select or create an author.")
            return
        if not all([craft_context, craft_role, craft_action, craft_format, craft_tone]):
            st.error("Please fill all CRAFT fields.")
            return
        
        # Build full text
        full_text = f"{craft_context}\n\n{craft_role}\n\n{craft_action}\n\n{craft_format}\n\n{craft_tone}"
        
        # Create submission
        payload = {
            "title": title,
            "description": description,
            "metier_id": metier["id"],
            "category_id": category_id,
            "category_name": category_name,
            "author_id": author_id,
            "author_display_name_snapshot": author_display_name_snapshot,
            "craft_context": craft_context,
            "craft_role": craft_role,
            "craft_action": craft_action,
            "craft_format": craft_format,
            "craft_tone": craft_tone,
            "full_text": full_text,
            "created_by": user_key
        }
        
        submission = db.create_submission(payload)
        
        toast("Prompt submitted for review!")
        st.balloons()
        
        st.success(f"Submission created! ID: {submission['id']}")
        
        if st.button("View My Submissions"):
            st.session_state['nav_view'] = 'my_submitted'
            st.rerun()

