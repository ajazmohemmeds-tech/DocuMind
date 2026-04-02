import streamlit as st
import requests
from typing import List, Dict, Any

# --- CONFIGURATION ---
st.set_page_config(page_title="DocuMind | Your Research Partner", layout="wide")

# --- CUSTOM THEME (Research Hub Aesthetic) ---
def apply_hero_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        .main {
            background-color: #FFFFFF !important;
            font-family: 'Inter', sans-serif;
        }

        /* Gradient Typography */
        .hero-title {
            font-size: 80px;
            font-weight: 800;
            text-align: center;
            color: #202124;
            margin-top: 50px;
            letter-spacing: -2px;
            line-height: 1.1;
        }
        .gradient-text {
            background: linear-gradient(90deg, #34A853 0%, #4285F4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            font-size: 20px;
            color: #5F6368;
            text-align: center;
            max-width: 650px;
            margin: 20px auto 40px auto;
            line-height: 1.5;
        }

        /* Black CTA Button */
        .stButton>button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 12px !important;
            padding: 12px 32px !important;
            font-weight: 600 !important;
            border: none !important;
            transition: transform 0.2s ease;
            margin: 0 auto;
            display: block;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background-color: #333333 !important;
        }

        /* Custom Card Grid */
        .source-card {
            background-color: #FFFFFF;
            border: 1px solid #DADCE0;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            transition: all 0.2s ease;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .source-card:hover {
            border-color: #4285F4;
            box-shadow: 0 4px 12px rgba(66, 133, 244, 0.12);
        }

        /* Header Re-styling */
        .workspace-header {
            font-size: 32px;
            font-weight: 700;
            color: #202124;
            margin-bottom: 24px;
            text-align: center;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F8F9FA !important;
            border-right: 1px solid #E0E0E0 !important;
        }
        
        /* Unified Input */
        [data-testid="stChatInput"] {
            max-width: 800px;
            border: 1px solid #DADCE0 !important;
            border-radius: 24px !important;
            background-color: #F1F3F4 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Application States: 'landing' or 'chat'
if 'view_state' not in st.session_state:
    st.session_state.view_state = 'landing'

apply_hero_css()
API_URL = "http://localhost:8000"

# --- SIDEBAR: NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color: #202124;'>DocuMind</h2>", unsafe_allow_html=True)
    st.caption("Your AI Research Partner")
    st.markdown("---")
    
    if st.button("⬅️ Back to Discovery"):
        st.session_state.view_state = 'landing'
        st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Workspace", use_container_width=True):
        try:
            requests.delete(f"{API_URL}/clear")
            st.session_state.messages = []
            st.success("Grounding data reset.")
        except:
            st.error("Reset failed.")

# --- VIEW 1: LANDING/DISCOVERY ---
if st.session_state.view_state == 'landing':
    # Hero Section
    st.markdown("<div class='hero-title'>Understand <span class='gradient-text'>Anything</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Your research and thinking partner, grounded in the information you trust, built with the latest DocuMind models.</div>", unsafe_allow_html=True)
    
    if st.button("Try DocuMind"):
        st.session_state.view_state = 'chat'
        st.rerun()

    st.markdown("<div style='text-align: center; margin-top: 60px; font-weight: 600; font-size: 24px;'>Your AI-Powered Research Partner</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Value Prop & Source Grid
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Synthesize insights from **your documents**</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='source-card'>
                <h3 style='font-size: 18px; margin-bottom: 12px;'>Upload Files</h3>
                <p style='font-size: 14px; color: #5F6368;'>PDF, Docs, and Images</p>
            </div>
        """, unsafe_allow_html=True)
        pdf_file = st.file_uploader("Upload PDF", type=['pdf'], label_visibility="collapsed")
        if pdf_file and st.button("Index Document", key="btn_pdf"):
            with st.spinner("Analyzing..."):
                files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
                r = requests.post(f"{API_URL}/upload/pdf", files=files)
                if r.status_code == 200:
                    st.session_state.view_state = 'chat'
                    st.rerun()

    with col2:
        st.markdown("""
            <div class='source-card'>
                <h3 style='font-size: 18px; margin-bottom: 12px;'>Websites</h3>
                <p style='font-size: 14px; color: #5F6368;'>Extract from any URL</p>
            </div>
        """, unsafe_allow_html=True)
        url_in = st.text_input("Enter URL", label_visibility="collapsed")
        if url_in and st.button("Crawl Website", key="btn_url"):
            with st.spinner("Grounding..."):
                r = requests.post(f"{API_URL}/upload/url", json={"url": url_in})
                if r.status_code == 200:
                    st.session_state.view_state = 'chat'
                    st.rerun()

    with col3:
        st.markdown("""
            <div class='source-card'>
                <h3 style='font-size: 18px; margin-bottom: 12px;'>How it works</h3>
                <p style='font-size: 14px; color: #5F6368;'>See the source, not just the answer.</p>
            </div>
        """, unsafe_allow_html=True)
        st.info("DocuMind provides clear citations for its work, showing you exact quotes.")

    # Lower Value Props
    st.markdown("---")
    vcol1, vcol2, vcol3 = st.columns(3)
    with vcol1:
        st.markdown("🎓 **Power study**\n\nExplain complex concepts in simple terms with real-world examples.")
    with vcol2:
        st.markdown("📂 **Organize thinking**\n\nCreate polished outlines and talking points from your source material.")
    with vcol3:
        st.markdown("💡 **Spark new ideas**\n\nIdentify trends and uncover hidden opportunities in your data.")

# --- VIEW 2: ACTIVE RESEARCH WORKSPACE ---
elif st.session_state.view_state == 'chat':
    st.markdown("<div class='workspace-header'>Research Workspace</div>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Centered conversation flow
    chat_col_left, chat_col_mid, chat_col_right = st.columns([1, 4, 1])
    
    with chat_col_mid:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("📖 Grounded Sources"):
                        for idx, src in enumerate(message["sources"]):
                            st.markdown(f"**Evidence [{idx+1}]:**")
                            st.caption(f"Source: {src['metadata'].get('source', 'Trusted Local File')}")
                            st.markdown(f"_{src['page_content']}_")

        if prompt := st.chat_input("Initiate research synthesis..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                res_area = st.empty()
                full_raw = ""
                
                try:
                    # Streamed Synthesis
                    with requests.post(f"{API_URL}/query", json={"query": prompt}, stream=True) as r:
                        if r.status_code == 200:
                            for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                                if chunk:
                                    full_raw += chunk
                                    res_area.markdown(full_raw + "▌")
                            res_area.markdown(full_raw)
                        else:
                            st.error("Research engine unreachable.")
                    
                    # Evidence Retrieval
                    ev_res = requests.post(f"{API_URL}/query/full", json={"query": prompt})
                    sources = ev_res.json().get("sources", []) if ev_res.status_code == 200 else []
                    
                    st.session_state.messages.append({"role": "assistant", "content": full_raw, "sources": sources})
                    
                    if sources:
                        with st.expander("📖 Grounded Sources"):
                            for idx, src in enumerate(sources):
                                st.markdown(f"**Evidence [{idx+1}]:**")
                                st.caption(f"Source: {src['metadata'].get('source', 'Trusted Local File')}")
                                st.markdown(f"_{src['page_content']}_")
                except Exception as e:
                    st.error(f"Sync error: {e}")
