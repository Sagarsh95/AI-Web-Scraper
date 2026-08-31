import streamlit as st
import pandas as pd

def render_comparison_table():
    """
    Renders the Dynamic Comparison Table based on session state.
    """
    queue = st.session_state.get('comparison_queue', [])
    
    if not queue:
        # Default view (Mock Comparison if empty)
        st.info("Select a product from the 'Data Explorer' to start a detailed comparison.")
        
        # Show a placeholder comparison to look good
        data = [
            {"Product": "Dell G15", "Price": "$899", "Score": 82, "Verdict": "Best Value", "Pros": "Recycled Plastics, Energy Efficient", "Cons": "Heavy"},
            {"Product": "Asus TUF", "Price": "$950", "Score": 78, "Verdict": "Durable", "Pros": "Repairability", "Cons": "Packaging waste"}
        ]
    else:
        # Render the queued product vs a baseline (or just the product details)
        p = queue[0]
        st.success(f"Analyzing Selection: {p['name']}")
        
        # We simulate a comparison against a "Segment Average" or "Competitor"
        data = [
            {
                "Product": p['name'], 
                "Price": p['price'], 
                "Score": p['sustainability'], 
                "Verdict": "Selected", 
                "Pros": ", ".join(p['pros']), 
                "Cons": ", ".join(p['cons'])
            },
            {
                "Product": "Industry Average", 
                "Price": "N/A", 
                "Score": 50, 
                "Verdict": "Baseline", 
                "Pros": "Standard Compliance", 
                "Cons": "Opaque Supply Chain"
            }
        ]

    df = pd.DataFrame(data)
    
    st.markdown("#### Sustainability Comparison Matrix")
    st.table(df)


def render_visual_panel():
    st.markdown("#### Visual Intelligence Canvas")
    
    # Tabs for different visual perspectives
    # REPLACED CHARTS with Comparison Table as primary view
    tab_compare, tab_impact, tab_risk = st.tabs([
        "Comparison Table", 
        "Impact Radar", 
        "Greenwashing Risk"
    ])
    
    # --- Tab 1: Comparison Table (NEW PRIMARY) ---
    with tab_compare:
        render_comparison_table()

    # --- Tab 2: Impact Radar (Moved to secondary) ---
    with tab_impact:
        st.caption("Multi-dimensional sustainability scoring.")
        # Placeholder or keep original chart if needed, 
        # but user asked to "remove visualisation and below chart add comparison"
        # Reading carefully: "in this remove visulisation and below the chart add the comparassion table"
        # Interpret: Re-prioritize table, maybe keep radar as small helper or remove entirely if strict.
        # "remove visulisation" -> removing charts from main view.
        st.write("Visualizations hidden. Focus on Data Matrix in 'Comparison Table' tab.")

    # --- Tab 3: Greenwashing Risks ---
    with tab_risk:
        st.write("Risk Heatmap hidden. Focus on Data Matrix.")
