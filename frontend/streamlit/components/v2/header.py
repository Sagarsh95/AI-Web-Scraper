import streamlit as st
from datetime import datetime

def render_context_header():
    # CSS defined globally or here locally for specificity
    st.markdown("""
        <style>
        .context-chip {
            background-color: #262730;
            padding: 4px 12px;
            border-radius: 4px;
            border: 1px solid #464b5d;
            font-size: 0.8rem;
            color: #e0e0e0;
            margin-right: 8px;
            display: inline-flex;
            align-items: center;
            font-family: 'Inter', sans-serif;
        }
        .header-title {
            font-weight: 700;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        .header-caption {
            color: #a0a0a0;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="header-title">AI Intelligence Workspace</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-caption">Grounded sustainability insights from scraped web intelligence</div>', unsafe_allow_html=True)

        # Context Chips Layout
        c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
        
        with c1:
            st.markdown('<div class="context-chip">Domain: Consumer Tech</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="context-chip">Mode: Deep Analysis</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="context-chip">Coverage: High (85%)</div>', unsafe_allow_html=True)
        with c4:
            st.caption(f"Last Intelligence Update: {datetime.now().strftime('%H:%M:%S')}")
        
    st.markdown("---")
