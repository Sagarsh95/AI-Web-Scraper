import streamlit as st
import requests

def render_mission_control(backend_url: str):
    st.markdown("## Scraping Operations")
    st.caption("Deploy autonomous agents to gather intelligence.")

    # 1. Mission Parameters
    with st.container(border=True):
        st.subheader("1. Mission Configuration")
        
        # Simple URL Input
        url_input = st.text_input("Target URL", placeholder="https://example.com/product")

    # 2. Deployment
    st.markdown("---")
    if st.button("Deploy Agent", use_container_width=True, type="primary"):
        if not url_input:
            st.error("Please provide a target.")
            return

        with st.status("Mission Active...", expanded=True) as status:
            st.write("Initializing Orchestrator...")
            try:
                # Defaulting to single_page mode as per simplification
                payload = {"url": url_input, "mode": "single_page"} 
                st.write(f"Requesting backend: {url_input}")
                
                response = requests.post(f"{backend_url}/api/scrape", json=payload, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    status.update(label="Mission Complete!", state="complete", expanded=False)
                    
                    st.success(f"Successfully processed document.")
                    
                    # 3. Data Display Section
                    st.markdown("### Scraped Data Intelligence")
                    
                    tab_raw, tab_cleaned, tab_html = st.tabs(["Raw Data (JSON)", "Cleaned Data (Structured)", "Raw HTML"])
                    
                    with tab_raw:
                        st.caption("Full raw payload from scraping engine.")
                        st.json(data)
                        
                    with tab_cleaned:
                        st.caption("Key extracted intelligence fields.")
                        # Display specific fields if available, else show data in a clearer way
                        if "data" in data:
                             st.write(data["data"])
                        else:
                             st.write("No specific structure detected. View Raw Data.")

                    with tab_html:
                        st.caption("Raw HTML Content")
                        html_content = data.get("html_content", "<!-- No HTML returned -->")
                        st.code(html_content, language="html")

                else:
                    status.update(label="Mission Failed", state="error")
                    st.error(f"Backend Error: {response.text}")
                    
            except Exception as e:
                status.update(label="Connection Error", state="error")
                st.error(f"Failed to connect: {e}")
