import streamlit as st

def render_recommendations(backend_url: str):
    st.markdown("## 🎯 AI Decision & Recommendation Engine")
    st.caption("Optimize your procurement strategy based on customized trade-offs.")
    
    # 1. Preferences
    st.subheader("1. Set Your Priorities")
    c1, c2, c3 = st.columns(3)
    with c1:
        price_weight = st.slider("💰 Price Sensitivity", 0, 100, 50)
    with c2:
        eco_weight = st.slider("🌱 Sustainability Importance", 0, 100, 80)
    with c3:
        ethics_weight = st.slider("🤝 Ethical Labor", 0, 100, 60)
        
    st.markdown("---")
    
    # 2. Results
    st.subheader("2. AI Recommendations")
    
    # Simulation Logic (V1) - Connecting to Data Explorer later
    # We display a mock comparison of 3 "Top Candidates"
    
    candidates = [
        {"name": "Organic Tee Co.", "price": "$25", "score": 92, "badge": "🏆 Best Eco"},
        {"name": "FastFashion Inc.", "price": "$12", "score": 30, "badge": "❌ Avoid"},
        {"name": "Balanced Basics", "price": "$20", "score": 75, "badge": "✅ Value Pick"}
    ]
    
    # Sort roughly by user weight (mock algo)
    # If Eco > 70, rank Eco items higher.
    
    cols = st.columns(3)
    for i, item in enumerate(candidates):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {item['name']}")
                st.caption(item['badge'])
                st.metric("Price", item['price'])
                st.metric("Sustainability", f"{item['score']}/100")
                
                if st.button(f"View Analysis #{i+1}", key=f"rec_{i}"):
                    st.toast(f"Loading full report for {item['name']}...")
                    
    st.info("💡 **AI Reasoning**: 'Organic Tee Co.' is recommended because you set Sustainability Importance > 75%. Analysis detected GOTS certification.")
