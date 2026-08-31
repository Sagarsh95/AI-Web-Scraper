import streamlit as st
import json
import os
import pandas as pd

def render_audit_trail(backend_url: str):
    st.markdown("## 📜 Trust & Transparency Log")
    st.caption("Immutable Record of AI Decisions and System Events")
    
    # Load Logs
    log_path = os.path.join(os.path.dirname(__file__), "../../../data/sample_audit.json")
    try:
        with open(log_path, "r") as f:
            logs = json.load(f)
    except:
        logs = []
        st.error("No audit logs found.")

    tab1, tab2 = st.tabs(["🔒 System Activity", "🧬 Decision Lineage"])
    
    with tab1:
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(
                df, 
                column_config={
                    "timestamp": "Time",
                    "level": st.column_config.TextColumn("Level", width="small"),
                    "source": "Component",
                    "message": "Event Detail"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("System is ready. Start a mission to generate logs.")

    with tab2:
        st.subheader("AI Reasoning Trace")
        st.markdown("Visualizing the flow from raw data to insight.")
        
        # Graphviz Visualization using raw DOT string
        dot_code = """
        digraph Lineage {
            rankdir=LR;
            bgcolor="#0E1117";
            node [shape=box, style=filled, color="#262730", fontcolor="white", fontname="sans-serif"];
            edge [color="#555555", fontcolor="#aaaaaa", fontsize=10];

            A [label="🌐 Target URL\n(example.com)"];
            B [label="🕷️ Scraper Agent\n(Playwright)"];
            C [label="🧹 Cleaner\n(HTML to Text)"];
            D [label="🗄️ Vector DB\n(Chroma)"];
            E [label="🧠 RAG Engine\n(Llama 3.2)"];
            F [label="📊 Insight\n(Sustainability Score)"];

            A -> B [label="  GET"];
            B -> C [label="  Raw HTML"];
            C -> D [label="  Embeddings"];
            D -> E [label="  Retrieved Context"];
            E -> F [label="  Generate"];
        }
        """

        st.graphviz_chart(dot_code)
        
        st.markdown("#### Sample Verification Trace")
        st.code("""
Query: "Is this product fair trade?"
1. Retrieval: Found 3 chunks (Confidence: 0.89)
   - Source A: "Certifications" section (doc_123)
   - Source B: "Footer" (doc_123)
2. Reasoning: 
   - Chunk A explicitly mentions "Fair Trade Certified Factory".
   - No contradictory evidence found.
3. Conclusion: TRUE (High Confidence).
        """, language="yaml")
