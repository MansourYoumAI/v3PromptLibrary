"""AI Prompt Studio - Main application."""

import streamlit as st
from lib.data_store import get_db
from lib.utils import qp
import config

# Page config
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject global CSS
def inject_css():
    """Inject global CSS and Google Fonts."""
    css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    * {
        font-family: 'Work Sans', sans-serif;
    }
    
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }
    
    /* Card hover effects */
    [data-testid="column"] {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    [data-testid="column"]:hover {
        transform: scale(1.01);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* CRAFT field styling */
    .craftfield textarea {
        background-color: #f5f5f5;
        border-radius: 8px;
    }
    
    /* Rounded corners */
    button, .stButton>button {
        border-radius: 8px;
    }
    
    /* Sticky region */
    .sticky {
        position: sticky;
        top: 0;
        background: white;
        z-index: 100;
        padding: 1rem 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_sidebar():
    """Render the persistent sidebar."""
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="font-size: 2rem; color: {config.PRIMARY_COLOR};">{config.APP_NAME}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo placeholder
    st.sidebar.markdown("---")
    st.sidebar.markdown("**LOGO**")
    st.sidebar.markdown("---")
    
    # Function selection (v1: Sales only)
    st.sidebar.markdown("### Function")
    st.sidebar.markdown("**Sales**")
    
    st.sidebar.markdown("---")
    
    # Categories
    db = get_db()
    metiers = db.list_metiers()
    if metiers:
        metier = metiers[0]
        categories = db.list_categories(metier["id"])
        
        with st.sidebar.expander("Categories"):
            for cat in categories:
                if st.button(cat["name"], key=f"sidebar_cat_{cat['id']}", use_container_width=True):
                    st.session_state['nav_view'] = 'category'
                    st.session_state['nav_cat'] = cat["id"]
                    st.rerun()
    
    st.sidebar.markdown("---")
    
    # My Prompts
    with st.sidebar.expander("My Prompts"):
        if st.button("My submitted prompts", key="sidebar_my_submitted", use_container_width=True):
            st.session_state['nav_view'] = 'my_submitted'
            st.rerun()
        
        if st.button("My saved prompts", key="sidebar_my_saved", use_container_width=True):
            st.session_state['nav_view'] = 'my_saved'
            st.rerun()


def main():
    """Main application entry point."""
    # Initialize session state
    if "user_key" not in st.session_state:
        st.session_state["user_key"] = "guest"
    
    if "app_name" not in st.session_state:
        st.session_state["app_name"] = config.APP_NAME
    
    if "copilot_url" not in st.session_state:
        st.session_state["copilot_url"] = config.COPILOT_URL
    
    # Handle navigation from session state (set query params and rerun)
    nav_view = st.session_state.get('nav_view')
    if nav_view:
        # Build query params
        params = {'view': nav_view}
        if 'nav_id' in st.session_state:
            params['id'] = st.session_state['nav_id']
        if 'nav_cat' in st.session_state:
            params['cat'] = st.session_state['nav_cat']
        
        # Update query params
        try:
            for key, value in params.items():
                st.query_params[key] = value
        except:
            # Fallback for older Streamlit
            st.experimental_set_query_params(**params)
        
        # Clear navigation flags
        st.session_state.pop('nav_view', None)
        st.session_state.pop('nav_id', None)
        st.session_state.pop('nav_cat', None)
        
        st.rerun()
        return
    
    # Inject CSS
    inject_css()
    
    # Render sidebar
    render_sidebar()
    
    # Router - check query params
    view = qp("view", "home")
    
    # Admin check
    if view == config.ADMIN_ROUTE or view == "admincoreteam50":
        from views import admin
        admin.render()
        return
    
    # Route to appropriate view
    try:
        if view == "home":
            from views import home
            home.render()
        elif view == "category":
            from views import category
            category.render()
        elif view == "prompt":
            from views import prompt_detail
            prompt_detail.render()
        elif view == "new":
            from views import new_prompt
            new_prompt.render()
        elif view == "my_saved":
            from views import my_saved
            my_saved.render()
        elif view == "my_submitted":
            from views import my_submitted
            my_submitted.render()
        else:
            st.error(f"Unknown view: {view}")
    except Exception as e:
        st.error(f"Error loading view: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()

