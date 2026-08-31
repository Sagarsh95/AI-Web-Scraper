import streamlit as st
import sys
import os
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))



from components.v2.overview import render_overview
from components.v2.mission_control import render_mission_control
from components.v2.analytics_dashboard import render_analytics_dashboard
from components.v2.audit_log import render_audit_trail
from components.v2.data_explorer import render_data_explorer
from components.v2.recommendations import render_recommendations
from components.v2.intelligence_canvas import render_intelligence_canvas  # NEW UI

BACKEND_URL = "http://localhost:8001"

def get_backend_status():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
    except:
        pass
    return False, None

def main():
    st.set_page_config(
        page_title="AI-DRIVEN WEB SCRAPING FOR SUSTAINABLE INSIGHTS AND DECISION MAKING ON E-COMMERCE",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )

   
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        .stApp {
            background-color: #0E1117;
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3 {
            color: #FAFAFA !important;
            font-family: 'Inter', sans-serif;
        }
        
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Soft Glow for Cards */
        div[data-testid="stExpander"] {
            border: 1px solid #2d313c;
            border-radius: 8px;
            background-color: #171a21;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = "Data & Schema Explorer"

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.title("AI-DRIVEN WEB SCRAPING FOR SUSTAINABLE INSIGHTS AND DECISION MAKING ON E-COMMERCE")
        st.caption("Enterprise AI Intelligence")
        st.markdown("---")
        
        # KEY CHANGE: index logic for programmatic switching
        options = [
            "Intelligence Overview",
            "Scraping Operations",
            # "Data & Product Catalog",
            "AI Analytics",
            "Logs & Audit Trail"
        ]
        

        try:
            default_index = options.index(st.session_state['active_tab'])
        except ValueError:
            default_index = 0

        selection = st.radio(
            "Workspace",
            options,
            index=default_index,
            label_visibility="collapsed"
        )
        
        # Sync selection back to state if user changed it manually
        if selection != st.session_state['active_tab']:
            st.session_state['active_tab'] = selection
        
        st.markdown("---")
       

        # Backend Status in footer
        is_online, _ = get_backend_status()
        if is_online:
            st.success("System Online")
        else:
            st.error("System Offline")

    # --- MAIN CONTENT ---

    if selection == "Intelligence Overview":
        render_overview(BACKEND_URL)

    elif selection == "Scraping Operations":
        render_mission_control(BACKEND_URL)

    elif selection == "Data & Product Catalog":
        render_data_explorer(BACKEND_URL)

    elif selection == "AI Analytics":
       
        render_intelligence_canvas(BACKEND_URL)


    elif selection == "Recommendations Engine":
        render_recommendations(BACKEND_URL)

    elif selection == "Logs & Audit Trail":
        render_audit_trail(BACKEND_URL)
        
    elif selection == "System & Model Control":
        st.header("System Control")

        st.warning("Authorized Personnel Only")

if __name__ == "__main__":
    main()
