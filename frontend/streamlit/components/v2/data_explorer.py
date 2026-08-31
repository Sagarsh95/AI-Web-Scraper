import streamlit as st
import requests
import pandas as pd
import json

def navigate_to_comparison(product_data):
    """
    Helper to queue product for comparison and switch tabs.
    """
    if 'comparison_queue' not in st.session_state:
        st.session_state['comparison_queue'] = []
    
    # Add to queue if not present
    st.session_state['comparison_queue'] = [product_data] # For now, single select focus
    
    # Switch Tab
    st.session_state['active_tab'] = "AI Analytics & Comparisons"
    st.rerun()

def render_data_explorer(backend_url: str):
    st.markdown("## Data & Product Discovery")
    st.caption("Live view of the AI Knowledge Base")
    
    # --- 1. PRODUCT CATALOG (NEW) ---
    st.subheader("Product Catalog")
    
    # Filters
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        category_filter = st.selectbox("Category", ["All", "Laptops", "Phones", "Clothing", "Accessories"])
    with c2:
        price_filter = st.selectbox("Price Range", ["All", "Under $500", "$500 - $1000", "$1000+"])
    with c3:
        st.write("") # Spacer
        if st.button("Refresh Catalog", use_container_width=True):
            st.cache_data.clear()

    # Mock Data (Simulating Parsed Content)
    # in V2.1 this will come from the backend's structured parsing of semantic HTML
    mock_products = [
        {
            "id": "p1", "name": "Dell G15 Gaming Laptop", "category": "Laptops", "price": "$899", "rating": 4.5, 
            "desc": "High-performance gaming laptop with eco-conscious post-consumer recycled plastics.",
            "sustainability": 82, "pros": ["Recycled Materials", "Energy Star"], "cons": ["Heavy"]
        },
        {
            "id": "p2", "name": "Asus TUF Dash F15", "category": "Laptops", "price": "$950", "rating": 4.2, 
            "desc": "Durable military-grade construction. Claims ease of repairability.",
            "sustainability": 78, "pros": ["Repairable", "Durable"], "cons": ["Plastic Packaging"]
        },
        {
            "id": "p3", "name": "Patagonia Organic Tee", "category": "Clothing", "price": "$45", "rating": 4.8, 
            "desc": "100% Organic Cotton. Fair Trade Certified sewn.",
            "sustainability": 95, "pros": ["Organic", "Fair Trade", "Traceable"], "cons": ["Pricey"]
        },
        {
            "id": "p4", "name": "Fairphone 5", "category": "Phones", "price": "$700", "rating": 4.6, 
            "desc": "The most repairable phone on the market. Modular design.",
            "sustainability": 98, "pros": ["Modular", "Conflict-Free", "5yr Warranty"], "cons": ["Mid-range specs"]
        }
    ]
    
    # Filter Logic
    filtered_products = [
         p for p in mock_products 
         if (category_filter == "All" or p["category"] == category_filter)
    ]
    
    # Render Grid
    cols = st.columns(3)
    for idx, product in enumerate(filtered_products):
        with cols[idx % 3]:
            with st.container(border=True):
                st.subheader(product["name"])
                st.caption(f"{product['category']} • {product['rating']} ⭐")
                st.markdown(f"**{product['price']}**")
                st.write(product['desc'])
                
                if st.button("Analyze & Compare", key=f"btn_{product['id']}", use_container_width=True, type="primary"):
                    navigate_to_comparison(product)

    st.markdown("---")

    # --- 2. RAW DATA (LEGACY MOVED BOTTOM) ---
    with st.expander("Raw Scraping Data & Knowledge Graph"):
        # Fetch Data
        try:
            response = requests.get(f"{backend_url}/api/documents", timeout=5)
            if response.status_code == 200:
                docs = response.json().get("data", [])
            else:
                docs = []
        except:
            docs = []
            
        if not docs:
            st.info("No raw scraped data available.")
        else:
            # Process Data for Table
            table_data = []
            for d in docs:
                meta = d.get("metadata", {})
                table_data.append({
                    "ID": d.get("id"),
                    "Title": meta.get("title", "Unknown"),
                    "URL": meta.get("url", "N/A"),
                    "Preview": d.get("preview", "")[:100]
                })
                
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
