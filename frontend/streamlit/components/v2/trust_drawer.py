import streamlit as st
import pandas as pd
from datetime import datetime

def render_trust_drawer():
    with st.expander("System Logistics & Trust Audit Trail", expanded=False):
        
        tab_log, tab_raw = st.tabs(["Execution Trace", "Raw Data Preview"])
        
        with tab_log:
            # Mock Log Data
            log_data = [
                {"Time": "00:01:23", "Level": "INFO", "Module": "Scraper", "Message": "Completed crawl of domain: google.com"},
                {"Time": "00:01:25", "Level": "INFO", "Module": "Cleaner", "Message": "Stripped boilerplate footer content (size reduced by 40%)"},
                {"Time": "00:01:28", "Level": "WARN", "Module": "AI Engine", "Message": "Prompt token limit approaching (3800/4096)"},
                {"Time": "00:01:30", "Level": "SUCCESS", "Module": "Orchestrator", "Message": "Analysis pipeline executed in 8.5s"}
            ]
            st.dataframe(pd.DataFrame(log_data), use_container_width=True, hide_index=True)
            
            st.button("Reproduce Analysis", help="Re-run this exact analysis sequence to verify results")
            
        with tab_raw:
            st.json({
                "source_url": "https://www.example.com/product",
                "scraped_at": datetime.now().isoformat(),
                "content_hash": "a1b2c3d4e5f6",
                "metadata": {
                    "author": "System",
                    "tags": ["tech", "review", "verified"]
                }
            })
