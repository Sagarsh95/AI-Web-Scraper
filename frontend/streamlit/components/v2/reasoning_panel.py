import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

def render_chart_from_json(chart_data):
    """
    Helper to render Plotly charts from backend JSON description.
    """
    try:
        chart_type = chart_data.get("type", "bar")
        title = chart_data.get("title", "")
        labels = chart_data.get("labels", [])
        datasets = chart_data.get("datasets", [])
        
        if not datasets:
            return
            
        # Standard Data Structure for simple charts
        # Assumes single dataset for now for simplicity, or loops
        
        df = pd.DataFrame({
            "Label": labels,
            "Value": datasets[0]["data"]
        })
        
        if chart_type == "bar":
            fig = px.bar(df, x="Label", y="Value", title=title, template="plotly_dark")
        elif chart_type == "line":
            fig = px.line(df, x="Label", y="Value", title=title, template="plotly_dark")
        elif chart_type == "pie":
            fig = px.pie(df, names="Label", values="Value", title=title, template="plotly_dark")
        elif chart_type == "radar":
            # Radar needs slightly different structure for plotly express
            fig = px.line_polar(df, r='Value', theta='Label', line_close=True, title=title, template="plotly_dark")
            fig.update_traces(fill='toself')
        else:
            st.warning(f"Unsupported chart type: {chart_type}")
            return

        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error rendering chart: {e}")

def render_reasoning_panel(backend_url: str): # Renamed function signature kept for app.py compatibility
    """
    Now actually a Chat Interface.
    """
    st.markdown("#### AI Analyst Chat")
    st.caption("Ask questions, compare products, or request charts.")
    
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # If there was a chart in this message, render it
            if "chart" in message:
                render_chart_from_json(message["chart"])

    # Chat Input
    if prompt := st.chat_input("Ask about sustainability..."):
        # Add User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI Response
        # Generate AI Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            chart_json = None
            
            try:
                payload = {"query": prompt}
                # Use stream=True
                with requests.post(f"{backend_url}/api/chat/stream", json=payload, timeout=600, stream=True) as response:
                    if response.status_code == 200:
                        
                        # We expect the first line to be metadata JSON, then the rest is text tokens
                        # iter_lines() is blocking if no newlines, so we use iter_content and manual buffer
                        iterator = response.iter_content(chunk_size=None)
                        buffer = b""
                        metadata_processed = False
                        
                        for chunk in iterator:
                            if not chunk: continue
                            
                            if not metadata_processed:
                                buffer += chunk
                                if b"\n" in buffer:
                                    # Split at first newline
                                    parts = buffer.split(b"\n", 1)
                                    metadata_line = parts[0]
                                    remaining = parts[1] if len(parts) > 1 else b""
                                    
                                    # Try parse metadata
                                    try:
                                        meta = json.loads(metadata_line)
                                        # Could show sources here if we wanted
                                    except:
                                        # Failed to parse, maybe just text?
                                        full_response += metadata_line.decode("utf-8", errors="ignore")
                                    
                                    metadata_processed = True
                                    
                                    # Process the rest of this chunk
                                    text_part = remaining.decode("utf-8", errors="ignore")
                                    full_response += text_part
                                    message_placeholder.markdown(full_response + "▌")
                            else:
                                # Standard token
                                text_part = chunk.decode("utf-8", errors="ignore")
                                full_response += text_part
                                message_placeholder.markdown(full_response + "▌")
                        
                        # Final render without cursor
                        message_placeholder.markdown(full_response)
                        
                        # Check for Chart JSON (Client-side extraction)
                        import re
                        json_match = re.search(r'\*\*\*CHART_JSON_START\*\*\*(.*?)\*\*\*CHART_JSON_END\*\*\*', full_response, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1).strip()
                            try:
                                chart_json = json.loads(json_str)
                                # Remove JSON block from display
                                clean_ans = full_response.replace(json_match.group(0), "").strip()
                                message_placeholder.markdown(clean_ans)
                                full_response = clean_ans
                            except:
                                pass # Failed to parse chart
                        
                        if chart_json:
                            render_chart_from_json(chart_json)
                        
                        # Save Assistant Message
                        msg_obj = {"role": "assistant", "content": full_response}
                        if chart_json:
                            msg_obj["chart"] = chart_json
                        st.session_state.messages.append(msg_obj)
                        
                    else:
                        st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
