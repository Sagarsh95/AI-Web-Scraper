import streamlit as st
import requests

def render_overview(backend_url: str):
    st.markdown("## Intelligence Overview")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Status", "ONLINE", delta="Stable")
    with col2:
        st.metric("Active Model", "Llama 3.2", delta="Local")
    with col3:
        st.metric("Scraped Pages", "12", delta="+2 today") # Mock data for V1
    with col4:
        st.metric("Risk Alerts", "0", delta="Clean")

    st.markdown("---")

    # Main Dashboard Area
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Recent Insights")
        st.info("Sustainability Insight: Product X uses 100% organic cotton but lacks Fair Trade certification.")
        st.info("Greenwashing Alert: 'Eco-friendly' tag detected on synthetic polyester item.")
        
    with c2:
        st.subheader("Quick Actions")
        if st.button("Start New Mission", use_container_width=True):
            st.toast("Navigating to Scraper...")
        if st.button("View Analytics", use_container_width=True):
            st.toast("Opening Analytics...")
        st.markdown("### System Health")
        try:
            resp = requests.get(f"{backend_url}/health", timeout=5)
            if resp.status_code == 200:
                st.success("Backend API: Connected")
            else:
                st.error(f"Backend API: Error {resp.status_code}")
        except:
             st.error("Backend API: Disconnected")
