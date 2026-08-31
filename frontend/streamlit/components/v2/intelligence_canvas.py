import streamlit as st
from .header import render_context_header
from .reasoning_panel import render_reasoning_panel

def render_intelligence_canvas(backend_url: str):
    """
    Main orchestration component for the Redesigned Intelligence Hub.
    """
    
    # 1. Sticky-like Context Header
    render_context_header()
    
    # 2. Reasoning Panel (Full Width)
    render_reasoning_panel(backend_url)

