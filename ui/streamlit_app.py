import streamlit as st
import requests
import os
from typing import List, Dict, Any

# --- CONFIGURATION ---
st.set_page_config(page_title="DocuMind | Research Reimagined", layout="wide")

# --- EARTH TONE ASSET PATHS ---
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_IMG = "file:///Users/ajazmohemmed/.gemini/antigravity/brain/937e0fa2-466a-4107-907a-0fbaf1649557/earth_documind_hero_background_1774922946725.png"
CARD_IMG = "file:///Users/ajazmohemmed/.gemini/antigravity/brain/937e0fa2-466a-4107-907a-0fbaf1649557/earth_documind_card_illustration_1774922963446.png"
LIB_IMG = "file:///Users/ajazmohemmed/.gemini/antigravity/brain/937e0fa2-466a-4107-907a-0fbaf1649557/earth_documind_architecture_render_1774922980206.png"

# --- EARTH TONE DESIGN SYSTEM ---
def apply_earth_palette():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;600&display=swap');
        
        :root {{
            --white-rock: #EAE0D2;
            --akaroa: #D7C9AE;
            --barley-corn: #A68763;
            --mine-shaft: #2D2D2D;
        }}

        body, .stApp {{
            background-color: var(--white-rock) !important;
            font-family: 'Outfit', sans-serif;
            color: var(--mine-shaft);
        }}

        /* Fixed Header Alignment (NO Glass Bar) */
        [data-testid="stHorizontalBlock"] {{
            align-items: center !important;
            width: 100% !important;
        }}
        
        .nav-links span {{
            margin: 0 20px;
            font-size: 14px;
            font-weight: 600;
            color: var(--mine-shaft);
            cursor: pointer;
            opacity: 0.7;
            white-space: nowrap;
        }}
        .nav-links span:hover {{ opacity: 1; color: var(--barley-corn); }}
        
        .launch-btn {{
            background: var(--mine-shaft);
            color: #FFFFFF;
            padding: 12px 28px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 600;
            display: inline-block;
            line-height: 1;
        }}

        /* Ghost Logo Button (Earth Tone Edit - NO BOX) */
        div.stButton > button[key="nav_logo"], 
        div.stButton > button[key="ws_logo"] {{
            background: none !important;
            border: none !important;
            padding: 0 !important;
            font-size: 26px !important;
            font-weight: 800 !important;
            color: var(--mine-shaft) !important;
            box-shadow: none !important;
            text-transform: none !important;
        }}

        /* Hero Container (White Rock Stone) */
        .hero-container {{
            position: relative;
            height: 85vh;
            border-radius: 48px;
            margin: 20px 40px;
            overflow: hidden;
            background: url('{HERO_IMG}') no-repeat center center;
            background-size: cover;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            border: 1px solid var(--akaroa);
            box-shadow: 0 20px 50px rgba(166, 135, 99, 0.1);
        }}
        .hero-title {{
            font-size: 100px;
            font-weight: 800;
            margin-bottom: 20px;
            letter-spacing: -4px;
            line-height: 0.95;
            color: var(--mine-shaft);
        }}
        .hero-subtitle {{
            font-size: 22px;
            max-width: 600px;
            margin-bottom: 48px;
            color: var(--mine-shaft);
            opacity: 0.8;
            line-height: 1.5;
        }}

        /* LARGE Barley Corn Try DocuMind Button */
        div.stButton > button {{
            background-color: var(--barley-corn) !important;
            color: #FFFFFF !important;
            border-radius: 40px !important;
            padding: 24px 72px !important;
            font-weight: 700 !important;
            font-size: 24px !important;
            border: none !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 10px 30px rgba(166, 135, 99, 0.3) !important;
            width: auto !important;
            margin: 0 auto !important;
            display: block !important;
        }}
        div.stButton > button:hover {{
            transform: translateY(-5px) scale(1.02);
            background-color: var(--mine-shaft) !important;
        }}

        /* Section 2: Product Breakdown (Akaroa Base) */
        .section-2 {{ padding: 140px 80px; background-color: var(--white-rock); }}
        .sec2-title {{ font-size: 56px; font-weight: 700; color: var(--mine-shaft); }}
        .sec2-desc {{ font-size: 22px; color: var(--mine-shaft); opacity: 0.7; }}
        
        .p-card {{ border-radius: 32px; padding: 48px; border: 1px solid var(--akaroa); }}
        .card-light {{ background: var(--akaroa); position: relative; overflow: hidden; }}
        .card-dark {{ background: var(--mine-shaft); color: var(--white-rock); }}
        
        .floating-flower {{ position: absolute; right: -20px; bottom: -20px; width: 250px; opacity: 0.9; }}

        /* Partner Logos Strip (Charcoal) */
        .partner-strip {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 80px;
            opacity: 0.5;
            color: var(--mine-shaft);
            font-weight: 700;
            letter-spacing: 2px;
        }}

        /* Section 3: Use Cases (Akaroa Split-Screen) */
        .section-3 {{ padding: 120px 80px; display: flex; gap: 80px; align-items: center; background-color: var(--akaroa); }}
        .sec3-right {{ background: var(--white-rock); border: 1px solid var(--barley-corn); border-radius: 40px; padding: 60px; }}
        .lib-render {{ width: 100%; border-radius: 24px; filter: sepia(0.2) contrast(1.1); }}
        
        /* Workspace Overrides (Earth Tone Panels) */
        [data-testid="stSidebar"] {{ display: none; }}
        .workspace-container {{
            background-color: var(--white-rock);
            border: 1px solid var(--akaroa);
            border-radius: 32px;
            padding: 30px;
            min-height: 80vh;
            color: var(--mine-shaft);
        }}
        
        /* Chat Input Fix */
        [data-testid="stChatInput"] {{
            background-color: var(--akaroa) !important;
            border: 1px solid var(--barley-corn) !important;
            color: var(--mine-shaft) !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# State Management
if 'view_state' not in st.session_state:
    st.session_state.view_state = 'landing'
if 'messages' not in st.session_state:
    st.session_state.messages = []

apply_earth_palette()
API_URL = "http://localhost:8000"

# --- VIEW 1: LANDING EARTH OVERHAUL ---
if st.session_state.view_state == 'landing':
    
    # 1. Functional Branding & Navigation (Simplified)
    cols = st.columns([1.5, 4, 1])
    with cols[0]:
        if st.button("DocuMind", key="nav_logo"):
            st.session_state.view_state = 'landing'
            st.rerun()
    with cols[1]:
        st.markdown("<div class='nav-links' style='text-align: center; margin-top: 10px;'><span>Insight Hub</span><span>Capabilities</span><span>Enterprise</span><span>Docs</span><span>Community</span></div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("<div class='launch-btn' style='text-align: center;'>Launch BETA</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Hero
    st.markdown(f"""
        <div class='hero-container'>
            <div style='font-size: 40px; color: var(--barley-corn); margin-bottom: 24px;'>✦</div>
            <div class='hero-title'>Stop Searching<br>Start Asking</div>
            <div class='hero-subtitle'>Your research and thinking partner, grounded in the information you trust, built with premium DocuMind synthesis.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # Redirecting to the high-fidelity React Workspace
        st.markdown(f"""
            <a href="http://localhost:5173" target="_self">
                <div style="background-color: var(--barley-corn); color: #FFFFFF; border-radius: 40px; padding: 18px 0; text-align: center; font-weight: 700; font-size: 24px; cursor: pointer; text-decoration: none; box-shadow: 0 10px 30px rgba(166, 135, 99, 0.3); transition: transform 0.2s ease;">
                    Try DocuMind
                </div>
            </a>
        """, unsafe_allow_html=True)

    # Capabilities
    st.markdown(f"""
        <div class='section-2'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 80px;'>
                <div class='sec2-title'>What is DocuMind?</div>
                <div class='sec2-desc'>DocuMind is an insight-bearing research hub that helps your synthesis grow while staying grounded in verified sources.</div>
            </div>
            <div class='card-grid'>
                <div class='p-card card-light'>
                    <div style='font-size: 28px; font-weight: 600; color: var(--mine-shaft);'>Insights that grow</div>
                    <div style='font-size: 16px; opacity: 0.7; max-width: 240px;'>Transform passive data into high-performing research protocols.</div>
                    <img src='{CARD_IMG}' class='floating-flower'>
                </div>
                <div class='p-card card-dark'>
                    <div style='font-size: 28px; font-weight: 600;'>Always grounded,<br>Always verified</div>
                    <div style='font-size: 16px; opacity: 0.7;'>Stay fully source-pegged with instant access to your citations — no hallucinations.</div>
                </div>
                <div class='p-card card-dark'>
                    <div style='font-size: 28px; font-weight: 600;'>100%<br>Hands-free</div>
                    <div style='font-size: 16px; opacity: 0.7;'>No need to manage chunks manually. DocuMind works in the background for you.</div>
                </div>
            </div>
            <div class='partner-strip'>
                <span>OPENAI</span><span>FAISS</span><span>LANGCHAIN</span><span>PYMUPDF</span><span>RAGAS</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Use Cases
    st.markdown(f"""
        <div class='section-3'>
            <div style='flex: 1;'>
                <div style='font-size: 16px; color: var(--barley-corn); margin-bottom: 16px;'>DocuMind in Action</div>
                <div style='font-size: 56px; font-weight: 700; color: var(--mine-shaft); margin-bottom: 32px;'>Use cases</div>
                <div style='font-size: 20px; color: var(--mine-shaft); line-height: 1.6; opacity: 0.8;'>DocuMind offers a variety of use cases for researchers, students, and businesses seeking secure and accurate knowledge synthesis.</div>
            </div>
            <div class='sec3-right' style='flex: 1.5;'>
                <div style='font-size: 36px; font-weight: 700; color: var(--mine-shaft); margin-bottom: 24px;'>Scholarly Hub</div>
                <div style='font-size: 18px; opacity: 0.8; color: var(--mine-shaft); margin-bottom: 40px;'>Boost your engagement by offering a secure, source-backed synthesis with high fidelity, allowing you to learn effortlessly.</div>
                <img src='{LIB_IMG}' class='lib-render'>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- VIEW 2: WORKSPACE EARTH OVERHAUL ---
elif st.session_state.view_state == 'workspace':
    head_cols = st.columns([1, 4, 1])
    with head_cols[0]:
        if st.button("DocuMind", key="ws_logo"):
            st.session_state.view_state = 'landing'
            st.rerun()
    with head_cols[1]:
        st.markdown("<div style='text-align: center; margin-top: 10px; font-weight: 700; font-size: 20px; color: var(--mine-shaft);'>Research Hub Workspace</div>", unsafe_allow_html=True)
    with head_cols[2]:
        st.markdown("<div class='launch-btn' style='text-align: center;'>BETA</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_src, col_chat = st.columns([1.5, 3.5])
    
    with col_src:
        st.markdown("<div class='workspace-container'>", unsafe_allow_html=True)
        st.markdown("### Sources", unsafe_allow_html=True)
        up = st.file_uploader("+ Add sources", type=['pdf'], label_visibility="collapsed")
        if up:
            with st.spinner("Ingesting..."):
                files = {"file": (up.name, up, "application/pdf")}
                requests.post(f"{API_URL}/upload/pdf", files=files)
                st.rerun()
        st.markdown("---")
        if st.button("⬅️ Back to Home"):
            st.session_state.view_state = 'landing'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chat:
        st.markdown("<div class='workspace-container'>", unsafe_allow_html=True)
        st.markdown("### Research Synthesis", unsafe_allow_html=True)
        if not st.session_state.messages:
            st.info("Initiate a query to start synthesis. Add sources on the left to ground the engine.")
        else:
            for m in st.session_state.messages:
                with st.chat_message(m["role"]): st.markdown(m["content"])
        prompt = st.chat_input("Ground your research...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                res_area = st.empty()
                full_raw = ""
                with requests.post(f"{API_URL}/query", json={"query": prompt}, stream=True) as r:
                    if r.status_code == 200:
                        for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                            if chunk:
                                full_raw += chunk
                                res_area.markdown(full_raw + "▌")
                        res_area.markdown(full_raw); st.session_state.messages.append({"role": "assistant", "content": full_raw})
        st.markdown("</div>", unsafe_allow_html=True)
