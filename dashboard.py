import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="IntelliBank | Intelligent Banking System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - GLASSMORPHISM + HOVERS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 20%, #0a1929 0%, #0e1117 40%, #000000 100%);
        color: #e6edf3;
    }

    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #00d4ff 0%, #7b61ff 50%, #00c853 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
        animation: shineHeader 4s linear infinite;
    }

    @keyframes shineHeader {
        to { background-position: 200% center; }
    }

    .sub-header {
        text-align: center;
        color: #8b9cb3;
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 0.05em;
        margin-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.7) 0%, rgba(15, 20, 25, 0.5) 100%);
        backdrop-filter: blur(20px);
        padding: 1.4rem 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(0, 212, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.35s ease;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 212, 255, 0.4);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.15);
    }

    div[data-testid="stMetricLabel"] {
        color: #8b9cb3 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #00d4ff, #7b61ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    /* ============================================ */
    /* ENHANCED TRANSACTION CARDS - Dashboard      */
    /* ============================================ */
    .txn-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.7) 0%, rgba(15, 20, 25, 0.5) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 75, 75, 0.2);
        border-left: 4px solid #ff4b4b;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .txn-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 75, 75, 0.08), transparent);
        transition: left 0.6s;
    }

    .txn-card:hover::before {
        left: 100%;
    }

    .txn-card:hover {
        transform: translateX(6px);
        border-color: rgba(255, 75, 75, 0.5);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.25);
    }

    .txn-card.medium {
        border-left-color: #ffaa00;
        border-color: rgba(255, 170, 0, 0.2);
    }

    .txn-card.medium:hover {
        border-color: rgba(255, 170, 0, 0.5);
        box-shadow: 0 8px 30px rgba(255, 170, 0, 0.25);
    }

    .txn-icon {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        background: rgba(255, 75, 75, 0.12);
        border: 1px solid rgba(255, 75, 75, 0.3);
        flex-shrink: 0;
    }

    .txn-icon.medium {
        background: rgba(255, 170, 0, 0.12);
        border-color: rgba(255, 170, 0, 0.3);
    }

    .txn-body {
        flex: 1;
        margin-left: 14px;
        min-width: 0;
    }

    .txn-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #e6edf3;
        margin-bottom: 3px;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
    }

    .txn-meta {
        color: #8b9cb3;
        font-size: 0.78rem;
        display: flex;
        gap: 12px;
        align-items: center;
        flex-wrap: wrap;
    }

    .txn-meta-item {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .txn-right {
        text-align: right;
        flex-shrink: 0;
    }

    .txn-amount {
        font-size: 1.15rem;
        font-weight: 800;
        color: #e6edf3;
        margin-bottom: 3px;
        font-family: 'JetBrains Mono', monospace;
    }

    .txn-score {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        background: rgba(255, 75, 75, 0.15);
        color: #ff4b4b;
        border: 1px solid rgba(255, 75, 75, 0.3);
    }

    .txn-score.medium {
        background: rgba(255, 170, 0, 0.15);
        color: #ffaa00;
        border-color: rgba(255, 170, 0, 0.3);
    }

    /* ============================================ */
    /* FLAGGED CARDS - Fraud Alerts page           */
    /* ============================================ */
    .flagged-card {
        background: linear-gradient(135deg, rgba(61, 26, 26, 0.75) 0%, rgba(42, 15, 15, 0.55) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 75, 75, 0.25);
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 14px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .flagged-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #ff4b4b, #ffaa00);
    }

    .flagged-card::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 75, 75, 0.08) 0%, transparent 60%);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.4s;
    }

    .flagged-card:hover::after {
        opacity: 1;
    }

    .flagged-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 75, 75, 0.5);
        box-shadow: 0 12px 40px rgba(255, 75, 75, 0.3);
    }

    .flagged-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
    }

    .flagged-id {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.05rem;
        color: #ff4b4b;
    }

    .flagged-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        background: rgba(255, 75, 75, 0.15);
        color: #ff4b4b;
        border: 1px solid rgba(255, 75, 75, 0.35);
        animation: pulseBorder 2s infinite;
    }

    @keyframes pulseBorder {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.4); }
        50% { box-shadow: 0 0 0 6px rgba(255, 75, 75, 0); }
    }

    .flagged-body {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin-top: 12px;
    }

    .flagged-item {
        background: rgba(15, 20, 25, 0.5);
        border: 1px solid rgba(255, 75, 75, 0.15);
        border-radius: 10px;
        padding: 10px 12px;
    }

    .flagged-label {
        color: #8b9cb3;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
        font-weight: 600;
    }

    .flagged-value {
        color: #e6edf3;
        font-size: 0.95rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    .flagged-value.amount {
        color: #ff4b4b;
        font-size: 1.1rem;
    }

    .flagged-value.score {
        color: #ff4b4b;
    }

    /* Risk gauge bar */
    .risk-bar {
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 12px;
    }

    .risk-bar-fill {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #ffaa00, #ff4b4b);
        transition: width 0.6s ease;
    }

    /* ============================================ */
    /* PDF READY CARD - Glassmorphism              */
    /* ============================================ */
    .pdf-ready-card {
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg,
            rgba(0, 212, 255, 0.12) 0%,
            rgba(123, 97, 255, 0.12) 50%,
            rgba(0, 200, 83, 0.08) 100%);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(0, 212, 255, 0.35);
        border-radius: 18px;
        padding: 22px 26px;
        margin-top: 20px;
        position: relative;
        overflow: hidden;
        animation: glowPulse 3s ease-in-out infinite;
    }

    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 8px 40px rgba(0, 212, 255, 0.15),
                        inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }
        50% {
            box-shadow: 0 12px 50px rgba(123, 97, 255, 0.25),
                        inset 0 1px 0 rgba(255, 255, 255, 0.08);
        }
    }

    .pdf-ready-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 30%,
            rgba(0, 212, 255, 0.15) 0%, transparent 40%);
        animation: rotateGlow 8s linear infinite;
        pointer-events: none;
    }

    @keyframes rotateGlow {
        to { transform: rotate(360deg); }
    }

    .pdf-ready-logo {
        width: 60px;
        height: 60px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #00d4ff, #7b61ff);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
        flex-shrink: 0;
        position: relative;
        z-index: 1;
        animation: logoFloat 3s ease-in-out infinite;
    }

    @keyframes logoFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }

    .pdf-ready-logo img {
        width: 36px;
        height: 36px;
        filter: brightness(0) invert(1);
    }

    .pdf-ready-content {
        flex: 1;
        position: relative;
        z-index: 1;
    }

    .pdf-ready-title {
        font-size: 1.15rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #7b61ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
        letter-spacing: -0.01em;
    }

    .pdf-ready-desc {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .pdf-ready-desc b {
        color: #7b61ff;
        font-weight: 700;
    }

    .pdf-ready-badge {
        position: absolute;
        top: 14px;
        right: 14px;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        background: rgba(0, 200, 83, 0.15);
        color: #00c853;
        border: 1px solid rgba(0, 200, 83, 0.4);
        z-index: 1;
    }

    /* OLD STYLES (keep for compatibility) */
    .fraud-alert {
        background: linear-gradient(135deg, rgba(61, 26, 26, 0.7) 0%, rgba(42, 15, 15, 0.5) 100%);
        backdrop-filter: blur(15px);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.1);
    }

    .safe-alert {
        background: linear-gradient(135deg, rgba(26, 61, 42, 0.7) 0%, rgba(15, 42, 26, 0.5) 100%);
        backdrop-filter: blur(15px);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #00c853;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 20px rgba(0, 200, 83, 0.1);
    }

    h2, h3 {
        color: #e6edf3 !important;
        font-weight: 700 !important;
    }

    h2 {
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0, 212, 255, 0.15);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 20, 25, 0.98) 0%, rgba(10, 15, 20, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 212, 255, 0.1);
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        background: rgba(26, 31, 46, 0.6) !important;
        border: 1px solid rgba(0, 212, 255, 0.15) !important;
        color: #cbd5e1 !important;
        padding: 0.7rem 1rem !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
        box-shadow: none !important;
        margin-bottom: 4px !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 212, 255, 0.15) !important;
        border-color: rgba(0, 212, 255, 0.5) !important;
        color: #00d4ff !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #7b61ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(0, 212, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    div[data-testid="stChatMessage"] {
        background: rgba(26, 31, 46, 0.5);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(0, 212, 255, 0.1);
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    div[data-testid="stChatInput"] {
        background: rgba(26, 31, 46, 0.8) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: rgba(15, 20, 25, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff, #7b61ff);
        border-radius: 4px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .pulse-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00c853;
        margin-right: 6px;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 200, 83, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 200, 83, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 200, 83, 0); }
    }

    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(0, 200, 83, 0.12);
        color: #00c853;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        border: 1px solid rgba(0, 200, 83, 0.3);
        margin-bottom: 1rem;
    }

    div[data-testid="stAudioInput"] button {
        border-radius: 50% !important;
        background: linear-gradient(135deg, #00d4ff, #7b61ff) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================
def load_data():
    db = SessionLocal()
    try:
        accounts = db.query(Account).all()
        transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).all()
        users = db.query(User).all()
        return accounts, transactions, users
    finally:
        db.close()


accounts, transactions, users = load_data()


# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🏦 IntelliBank</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent Banking System • AI-Powered Fraud Detection</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:1.5rem;">
    <span class="live-badge"><span class="pulse-dot"></span>SYSTEM LIVE</span>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size:3rem;">🏦</div>
        <div style="font-size:1.5rem; font-weight:800; 
                    background: linear-gradient(135deg,#00d4ff,#7b61ff);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            IntelliBank
        </div>
        <div style="color:#64748b; font-size:0.75rem; letter-spacing:0.1em; margin-top:4px;">
            v1.0 • AI BANKING
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="color:#8b9cb3; font-size:0.8rem; letter-spacing:0.1em; font-weight:600; margin-bottom:8px;">NAVIGATION</p>', unsafe_allow_html=True)

    nav_items = [
        ("🏠", "Dashboard"),
        ("💳", "Accounts"),
        ("📜", "Transactions"),
        ("🚨", "Fraud Alerts"),
        ("📈", "Analytics"),
        ("🎮", "Simulator"),
        ("📄", "PDF Analysis"),
        ("🤖", "Jarvis Chat"),
        ("📋", "Audit Log"),
    ]

    for icon, name in nav_items:
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="color:#64748b; font-size:0.75rem; text-align:center; line-height:1.8;">
        <div>🎓 AI & Data Science</div>
        <div>Final Year Project</div>
        <div style="margin-top:8px; color:#00d4ff;">⚡ Powered by XGBoost</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# LOGIN GATE
# ============================================================
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    # ===== Login Page =====
    st.markdown("""
    <div style="
        max-width: 420px;
        margin: 60px auto;
        background: rgba(26, 31, 46, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 40px 32px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    ">
        <div style="text-align:center; margin-bottom: 24px;">
            <div style="font-size: 3rem;">🏦</div>
            <div style="font-size: 1.8rem; font-weight: 800;
                        background: linear-gradient(135deg,#00d4ff,#7b61ff);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        background-clip:text; margin-top: 8px;">
                IntelliBank
            </div>
            <div style="color:#8b9cb3; font-size: 0.85rem; margin-top: 6px;">
                AI-Powered Banking System
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        with st.form("login_form"):
            st.markdown("### 🔐 Sign In")
            username = st.text_input("Username", placeholder="admin or user")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                from app.utils.auth import authenticate
                user = authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"✅ Welcome, {user['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        st.markdown("---")
        st.markdown("""
        <div style="
            background: rgba(0, 212, 255, 0.08);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 0.85rem;
            color: #cbd5e1;
        ">
            <b style="color:#00d4ff;">🔑 Demo Credentials</b><br><br>
            <b>Admin:</b> admin / admin123<br>
            <b>User:</b> user / user123
        </div>
        """, unsafe_allow_html=True)

    st.stop()  # Stop rendering rest of app


# ============================================================
# LOGGED IN — Show user in sidebar
# ============================================================


page = st.session_state.page

# ============================================================
# DASHBOARD PAGE
# ============================================================
if page == "Dashboard":
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=15000, key="dash_autorefresh")

    now = datetime.now().strftime("%d %b %Y, %H:%M:%S")
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(26, 31, 46, 0.5);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 16px;
    ">
        <div style="color:#8b9cb3; font-size:0.85rem;">
            🔄 <b style="color:#00d4ff;">Live Dashboard</b> — Auto-refresh every 15s
        </div>
        <div style="color:#64748b; font-size:0.8rem;">
            Last update: <b style="color:#00d4ff;">{now}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_accounts = len(accounts)
    total_transactions = len(transactions)
    fraud_count = len([t for t in transactions if t.is_fraud])
    blocked_accounts = len([a for a in accounts if a.is_blocked])
    total_balance = sum([a.balance for a in accounts])

    latest_fraud = [t for t in transactions if t.is_fraud][:1]
    if latest_fraud:
        t = latest_fraud[0]
        if t.created_at and (datetime.utcnow() - t.created_at).total_seconds() < 60:
            st.toast(f"🚨 New fraud: {t.transaction_id} — Rs {t.amount:,.0f}", icon="🚨")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("💳 Total Accounts", total_accounts)
    with col2:
        st.metric("📊 Transactions", total_transactions)
    with col3:
        st.metric("🚨 Fraud Detected", fraud_count,
                  delta=f"{fraud_count} alerts", delta_color="inverse")
    with col4:
        st.metric("🔒 Blocked", blocked_accounts)
    with col5:
        st.metric("💰 Total Balance", f"Rs {total_balance:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### 🚨 Recent High-Risk Transactions")
        high_risk_txns = [t for t in transactions if t.fraud_score >= 0.5][:6]

        if high_risk_txns:
            for t in high_risk_txns:
                is_critical = t.is_fraud or t.fraud_score >= 0.7
                card_class = "txn-card" if is_critical else "txn-card medium"
                icon_class = "txn-icon" if is_critical else "txn-icon medium"
                score_class = "txn-score" if is_critical else "txn-score medium"
                icon_emoji = "🚨" if is_critical else "⚠️"

                # Determine transaction icon based on type
                txn_type = (t.transaction_type or "").lower()
                type_icon = "💸"
                if "transfer" in txn_type:
                    type_icon = "🔄"
                elif "withdraw" in txn_type:
                    type_icon = "🏧"
                elif "payment" in txn_type:
                    type_icon = "💳"
                elif "deposit" in txn_type:
                    type_icon = "💰"

                date_str = t.created_at.strftime('%d %b • %H:%M') if t.created_at else '—'

                st.markdown(f"""
                <div class="{card_class}">
                    <div class="{icon_class}">{icon_emoji}</div>
                    <div class="txn-body">
                        <div class="txn-title">{t.transaction_id}</div>
                        <div class="txn-meta">
                            <span class="txn-meta-item">{type_icon} {t.transaction_type or 'N/A'}</span>
                            <span class="txn-meta-item">📅 {date_str}</span>
                        </div>
                    </div>
                    <div class="txn-right">
                        <div class="txn-amount">Rs {t.amount:,.0f}</div>
                        <span class="{score_class}">SCORE {t.fraud_score:.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ No high-risk transactions detected. All systems operating normally.")

    with right:
        st.markdown("### 📊 Fraud Distribution")

        fraud_df = pd.DataFrame({
            "Status": ["Safe", "Fraud"],
            "Count": [total_transactions - fraud_count, fraud_count]
        })
        fig = px.pie(
            fraud_df, values="Count", names="Status",
            color="Status",
            color_discrete_map={"Fraud": "#ff4b4b", "Safe": "#00c853"},
            hole=0.65
        )
        fig.update_traces(
            textposition='outside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#0e1117', width=2))
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e6edf3",
            font_family="Inter",
            showlegend=False,
            height=320,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ACCOUNTS PAGE
# ============================================================
elif page == "Accounts":
    st.markdown("## 💳 All Accounts")
    st.caption(f"Total {len(accounts)} accounts registered in the system")

    if not accounts:
        st.warning("No accounts found in the system.")
    else:
        total_acc = len(accounts)
        active_acc = len([a for a in accounts if not a.is_blocked])
        blocked_acc = len([a for a in accounts if a.is_blocked])

        c1, c2, c3 = st.columns(3)
        c1.metric("💳 Total", total_acc)
        c2.metric("🟢 Active", active_acc)
        c3.metric("🔴 Blocked", blocked_acc)

        st.markdown("---")

        data = []
        for a in accounts:
            data.append({
                "ID": a.id,
                "Account No.": a.account_number,
                "Type": a.account_type.title(),
                "Balance (Rs)": f"{a.balance:,.2f}",
                "Risk Score": a.risk_score,
                "Status": "🔴 Blocked" if a.is_blocked else "🟢 Active",
                "Block Reason": a.block_reason or "—"
            })
        df = pd.DataFrame(data)

        st.markdown("### 📥 Export Accounts")
        from app.utils.export_utils import to_excel, to_csv
        ts_acc = datetime.now().strftime("%Y%m%d_%H%M")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.download_button(
                label="📊 Download Excel",
                data=to_excel(df, "Accounts"),
                file_name=f"intellibank_accounts_{ts_acc}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with col_e2:
            st.download_button(
                label="📃 Download CSV",
                data=to_csv(df),
                file_name=f"intellibank_accounts_{ts_acc}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("---")
        st.dataframe(df, use_container_width=True, hide_index=True, height=400)

        st.markdown("---")
        st.markdown("### 🔧 Account Actions")
        st.caption("Select an account to block or unblock it")

        acc_options = {f"{a.account_number} — Rs {a.balance:,.0f}": a for a in accounts}
        selected_label = st.selectbox("Select Account", list(acc_options.keys()))
        selected_acc = acc_options[selected_label]

        col1, col2 = st.columns(2)

        with col1:
            if selected_acc.is_blocked:
                if st.button("🔓 Unblock Account", use_container_width=True):
                    db = SessionLocal()
                    try:
                        acc = db.query(Account).filter(Account.id == selected_acc.id).first()
                        acc.is_blocked = False
                        acc.block_reason = None
                        db.commit()

                        from app.utils.audit import log_action
                        log_action(
                            action="unblock_account",
                            target=f"Account {acc.account_number}",
                            details="Manually unblocked by admin",
                        )

                        st.success(f"✅ Unblocked {acc.account_number}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
                    finally:
                        db.close()
            else:
                st.info("🟢 This account is currently active")

        with col2:
            if not selected_acc.is_blocked:
                if st.button("🔒 Block Account", use_container_width=True):
                    db = SessionLocal()
                    try:
                        acc = db.query(Account).filter(Account.id == selected_acc.id).first()
                        acc.is_blocked = True
                        acc.block_reason = "Manually blocked by admin"
                        db.commit()

                        from app.utils.audit import log_action
                        log_action(
                            action="block_account",
                            target=f"Account {acc.account_number}",
                            details="Manually blocked by admin",
                        )

                        st.success(f"🔒 Blocked {acc.account_number}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
                    finally:
                        db.close()
            else:
                st.info("🔴 This account is currently blocked")

        if selected_acc.is_blocked:
            st.markdown(f"""
            <div style="
                background: rgba(61, 26, 26, 0.5);
                backdrop-filter: blur(15px);
                border-left: 4px solid #ff4b4b;
                border-radius: 10px;
                padding: 14px 18px;
                margin-top: 14px;
            ">
                <div style="font-size:1rem; font-weight:700; color:#ff4b4b;">
                    🔴 Account Blocked
                </div>
                <div style="color:#8b9cb3; font-size:0.85rem; margin-top:6px;">
                    <b>Account:</b> {selected_acc.account_number}<br>
                    <b>Reason:</b> {selected_acc.block_reason or 'N/A'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                background: rgba(26, 61, 42, 0.5);
                backdrop-filter: blur(15px);
                border-left: 4px solid #00c853;
                border-radius: 10px;
                padding: 14px 18px;
                margin-top: 14px;
            ">
                <div style="font-size:1rem; font-weight:700; color:#00c853;">
                    🟢 Account Active
                </div>
                <div style="color:#8b9cb3; font-size:0.85rem; margin-top:6px;">
                    <b>Account:</b> {selected_acc.account_number}<br>
                    <b>Balance:</b> Rs {selected_acc.balance:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# TRANSACTIONS PAGE
# ============================================================
elif page == "Transactions":
    st.markdown("## 📜 All Transactions")
    st.caption(f"Total {len(transactions)} transactions on record")

    if not transactions:
        st.warning("No transactions found in the system.")
    else:
        data = []
        for t in transactions:
            data.append({
                "ID": t.id,
                "Txn ID": t.transaction_id,
                "Type": t.transaction_type.title() if t.transaction_type else "—",
                "Amount (Rs)": f"{t.amount:,.2f}",
                "Fraud Score": t.fraud_score,
                "Is Fraud": "Yes" if t.is_fraud else "No",
                "Status": t.status,
                "Description": t.description or "—",
                "Date": t.created_at.strftime("%d %b %Y %H:%M") if t.created_at else "—"
            })
        df = pd.DataFrame(data)

        st.markdown("### 📥 Export Reports")
        from app.utils.export_utils import to_excel, to_csv, to_pdf

        col1, col2, col3 = st.columns(3)
        ts = datetime.now().strftime("%Y%m%d_%H%M")

        with col1:
            st.download_button(
                label="📊 Download Excel",
                data=to_excel(df, "Transactions"),
                file_name=f"intellibank_transactions_{ts}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                label="📄 Download PDF",
                data=to_pdf(df, "Transactions Report"),
                file_name=f"intellibank_transactions_{ts}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with col3:
            st.download_button(
                label="📃 Download CSV",
                data=to_csv(df),
                file_name=f"intellibank_transactions_{ts}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("---")
        st.dataframe(df, use_container_width=True, hide_index=True, height=550)


# ============================================================
# FRAUD ALERTS PAGE
# ============================================================
elif page == "Fraud Alerts":
    st.markdown("## 🚨 Fraud Detection Center")
    st.caption("Real-time monitoring of suspicious and confirmed fraudulent transactions")

    fraud_txns = [t for t in transactions if t.is_fraud]
    high_risk = [t for t in transactions if t.fraud_score >= 0.5]

    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Confirmed Fraud", len(fraud_txns))
    c2.metric("⚠️ High Risk (≥0.5)", len(high_risk))
    c3.metric("📊 Total Analyzed", len(transactions))

    st.markdown("---")

    # ===== Export Section =====
    if fraud_txns:
        st.markdown("### 📥 Export Fraud Report")

        fraud_data = []
        for t in fraud_txns:
            fraud_data.append({
                "Txn ID": t.transaction_id,
                "Type": t.transaction_type.title() if t.transaction_type else "—",
                "Amount (Rs)": t.amount,
                "Fraud Score": t.fraud_score,
                "Description": t.description or "—",
                "Date": t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else "—",
            })
        fraud_df = pd.DataFrame(fraud_data)

        from app.utils.export_utils import to_excel, to_csv, to_pdf
        ts_fraud = datetime.now().strftime("%Y%m%d_%H%M")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.download_button(
                label="📊 Download Excel",
                data=to_excel(fraud_df, "Fraud Alerts"),
                file_name=f"intellibank_fraud_{ts_fraud}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with col_f2:
            st.download_button(
                label="📄 Download PDF",
                data=to_pdf(fraud_df, "Fraud Alerts Report"),
                file_name=f"intellibank_fraud_{ts_fraud}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with col_f3:
            st.download_button(
                label="📃 Download CSV",
                data=to_csv(fraud_df),
                file_name=f"intellibank_fraud_{ts_fraud}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("---")

    # ===== Flagged Transactions List =====
    st.markdown("### 🚩 Flagged Transactions")

    if fraud_txns:
        for t in fraud_txns:
            # Determine type icon
            txn_type = (t.transaction_type or "").lower()
            type_icon = "💸"
            if "transfer" in txn_type:
                type_icon = "🔄"
            elif "withdraw" in txn_type:
                type_icon = "🏧"
            elif "payment" in txn_type:
                type_icon = "💳"
            elif "deposit" in txn_type:
                type_icon = "💰"

            date_str = t.created_at.strftime('%d %b %Y • %H:%M') if t.created_at else '—'
            score_pct = min((t.fraud_score or 0) * 100, 100)

            st.markdown(f"""
            <div class="flagged-card">
                <div class="flagged-header">
                    <div class="flagged-id">
                        🚨 {t.transaction_id}
                    </div>
                    <div class="flagged-status">
                        ⚠️ FRAUD CONFIRMED
                    </div>
                </div>
                <div class="flagged-body">
                    <div class="flagged-item">
                        <div class="flagged-label">💰 Amount</div>
                        <div class="flagged-value amount">Rs {t.amount:,.0f}</div>
                    </div>
                    <div class="flagged-item">
                        <div class="flagged-label">{type_icon} Type</div>
                        <div class="flagged-value">{t.transaction_type or 'N/A'}</div>
                    </div>
                    <div class="flagged-item">
                        <div class="flagged-label">🎯 Fraud Score</div>
                        <div class="flagged-value score">{t.fraud_score:.2f}</div>
                    </div>
                    <div class="flagged-item">
                        <div class="flagged-label">📅 Date</div>
                        <div class="flagged-value" style="font-size:0.8rem;">{date_str}</div>
                    </div>
                </div>
                <div class="risk-bar">
                    <div class="risk-bar-fill" style="width: {score_pct}%;"></div>
                </div>
                <div style="color:#8b9cb3; font-size:0.78rem; margin-top:10px; font-style:italic;">
                    📝 {t.description or 'No description provided'}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No confirmed fraud transactions at this time.")

        # ============================================================
# ANALYTICS PAGE
# ============================================================
elif page == "Analytics":
    st.markdown("## 📈 Analytics & Insights")

    if not transactions:
        st.info("📭 Insufficient data for analytics. Please add transactions first.")
    else:
        type_counts = {}
        type_amounts = {}
        scores = []

        for t in transactions:
            t_type = t.transaction_type or "unknown"
            type_counts[t_type] = type_counts.get(t_type, 0) + 1
            type_amounts[t_type] = type_amounts.get(t_type, 0) + (t.amount or 0)
            scores.append(t.fraud_score if t.fraud_score is not None else 0)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Transaction Count by Type")
            if type_counts:
                df_count = pd.DataFrame({
                    "Type": list(type_counts.keys()),
                    "Count": list(type_counts.values())
                })
                fig1 = px.bar(
                    df_count, x="Type", y="Count", color="Type",
                    color_discrete_sequence=["#00d4ff", "#7b61ff", "#00c853", "#ffaa00"]
                )
                fig1.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e6edf3", font_family="Inter",
                    height=380, showlegend=False,
                    margin=dict(t=30, b=30),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
                )
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("#### 💰 Total Amount by Type")
            if type_amounts:
                df_amount = pd.DataFrame({
                    "Type": list(type_amounts.keys()),
                    "Amount": list(type_amounts.values())
                })
                fig2 = px.bar(
                    df_amount, x="Type", y="Amount", color="Type",
                    color_discrete_sequence=["#00d4ff", "#7b61ff", "#00c853", "#ffaa00"]
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e6edf3", font_family="Inter",
                    height=380, showlegend=False,
                    margin=dict(t=30, b=30),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
                )
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🎯 Fraud Score Distribution")

        if scores:
            df_scores = pd.DataFrame({"Fraud Score": scores})
            fig3 = px.histogram(
                df_scores, x="Fraud Score", nbins=10,
                color_discrete_sequence=["#ff4b4b"]
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e6edf3", font_family="Inter",
                height=380, showlegend=False,
                margin=dict(t=30, b=30),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
            )
            st.plotly_chart(fig3, use_container_width=True)


# ============================================================
# SIMULATOR PAGE
# ============================================================
elif page == "Simulator":
    st.markdown("## 🎮 Real-Time Fraud Simulator")
    st.caption("Test the AI fraud detection engine with custom transactions")

    from app.ml.fraud_detector import FraudDetector

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### 📝 Transaction Details")

        if accounts:
            acc_options = {f"Account {a.id} — {a.account_number} (Rs {a.balance:,.0f})": a for a in accounts}
            selected = st.selectbox("Select Account", list(acc_options.keys()))
            selected_acc = acc_options[selected]
        else:
            st.warning("No accounts available")
            selected_acc = None

        amount = st.number_input("Amount (Rs)", min_value=1.0, value=80000.0, step=1000.0)
        txn_type = st.selectbox("Transaction Type", ["transfer", "withdrawal", "payment", "deposit"])
        description = st.text_input("Description", "Test transaction")
        hour = st.slider("Hour of Day", 0, 23, 3)

    with col2:
        st.markdown("### 🤖 Prediction Result")

        if st.button("🚀 Run Fraud Detection", use_container_width=True):
            if not selected_acc:
                st.error("Please add accounts first")
            else:
                try:
                    detector = FraudDetector()
                    score = detector.calculate_fraud_score(
                        amount=amount,
                        transaction_type=txn_type,
                        account_balance=selected_acc.balance,
                        hour=hour,
                    )
                    is_fraud = detector.is_fraud(score)

                    st.markdown("---")

                    if is_fraud:
                        st.markdown(f"""
                        <div class="fraud-alert">
                            <b style="color:#ff4b4b; font-size:1.1rem;">🚨 FRAUD DETECTED!</b><br>
                            <small>Score: {score:.3f} (threshold: 0.5)</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="safe-alert">
                            <b style="color:#00c853; font-size:1.1rem;">✅ TRANSACTION SAFE</b><br>
                            <small>Score: {score:.3f} (threshold: 0.5)</small>
                        </div>
                        """, unsafe_allow_html=True)

                    from app.utils.audit import log_action
                    log_action(
                        action="simulate",
                        target=f"Account {selected_acc.account_number}",
                        details=f"Amount Rs {amount:,.0f} | Type {txn_type} | Score {score:.3f} | {'FRAUD' if is_fraud else 'SAFE'}",
                    )

                    st.metric("Fraud Score", f"{score:.3f}")
                    st.progress(min(score, 1.0))

                    if score >= 0.7:
                        st.error("🔴 Critical risk")
                    elif score >= 0.5:
                        st.warning("🟠 High risk")
                    elif score >= 0.3:
                        st.info("🟡 Medium risk")
                    else:
                        st.success("🟢 Low risk")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

        st.markdown("---")
        st.caption("💡 Tip: Try Rs 100,000+ at 3 AM for higher fraud scores")

    st.markdown("---")
    st.markdown("### 🔍 AI Explanation (SHAP)")
    st.caption("Understand which features contributed most to the fraud prediction")

    if st.button("📊 Explain Prediction with SHAP", use_container_width=True):
        if not selected_acc:
            st.warning("Select an account first")
        else:
            try:
                from app.ml.explain import explain_transaction

                contributions = explain_transaction(
                    amount=amount,
                    transaction_type=txn_type,
                    account_balance=selected_acc.balance,
                    hour=hour,
                )

                st.markdown("#### Feature Contributions")

                for c in contributions:
                    impact = c["impact"]
                    if abs(impact) < 0.001:
                        continue

                    if impact > 0:
                        color = "#ff4b4b"
                        icon = "🔴"
                        label = "increases risk"
                    else:
                        color = "#00c853"
                        icon = "🟢"
                        label = "decreases risk"

                    st.markdown(f"""
                    <div style="
                        background: rgba(26, 31, 46, 0.5);
                        backdrop-filter: blur(15px);
                        border-left: 4px solid {color};
                        border-radius: 10px;
                        padding: 12px 16px;
                        margin-bottom: 8px;
                    ">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <b style="color:{color};">{icon} {c['feature']}</b>
                                <span style="color:#8b9cb3;"> = {c['value']:.2f}</span>
                            </div>
                            <div style="text-align:right;">
                                <span style="color:{color}; font-weight:700; font-size:1.05rem;">
                                    {impact:+.4f}
                                </span>
                                <div style="color:#64748b; font-size:0.75rem;">{label}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.caption("💡 Positive values push toward fraud, negative values push toward safe")

            except Exception as e:
                st.error(f"❌ Explanation failed: {e}")
                st.caption("Make sure the model file exists at `app/ml/models/fraud_xgb_model.joblib`")


# ============================================================
# PDF ANALYSIS PAGE
# ============================================================
elif page == "PDF Analysis":
    st.markdown("## 📄 PDF Document Analysis")
    st.caption("Upload a bank statement or financial report — the system will extract and analyze the data")

    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"],
        help="Bank statement, transaction report, or any financial PDF document"
    )

    if uploaded_file is not None:
        import os
        import uuid
        from app.services.pdf_service import analyze_pdf

        os.makedirs("uploads", exist_ok=True)
        file_id = str(uuid.uuid4())[:8]
        save_path = os.path.join("uploads", f"{file_id}_{uploaded_file.name}")

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("🔍 Analyzing PDF document..."):
            try:
                result = analyze_pdf(save_path)
                st.session_state["pdf_analysis"] = result
                st.session_state["pdf_text"] = result.get("full_text", "")

                from app.utils.audit import log_action
                log_action(
                    action="pdf_upload",
                    target=uploaded_file.name,
                    details=f"Extracted {result.get('amounts_found', 0)} amounts, {result.get('tables_found', 0)} tables",
                )

                st.success("✅ PDF analyzed successfully!")
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                result = None

        if result:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💵 Amounts Found", result.get("amounts_found", 0))
            c2.metric("📈 Max Amount", f"Rs {result.get('max_amount', 0):,.0f}")
            c3.metric("📊 Tables Found", result.get("tables_found", 0))
            c4.metric("🚨 Alerts", len(result.get("suspicious_alerts", [])))

            st.markdown("---")
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("### 👤 Possible Names")
                names = result.get("possible_names", [])
                if names:
                    for n in names:
                        st.write(f"• {n}")
                else:
                    st.info("No clear names detected in the document")

                st.markdown("### 🏦 Account Numbers")
                accounts_found = result.get("accounts_found", [])
                if accounts_found:
                    for a in accounts_found:
                        st.code(a, language=None)
                else:
                    st.info("No account numbers detected in the document")

            with col_right:
                st.markdown("### 📅 Dates Found")
                dates = result.get("dates_found", [])
                if dates:
                    for d in dates[:10]:
                        st.write(f"• {d}")
                else:
                    st.info("No dates detected in the document")

                st.markdown("### 🚨 Suspicious Alerts")
                alerts = result.get("suspicious_alerts", [])
                if alerts:
                    for alert in alerts:
                        st.warning(alert)
                else:
                    st.success("No suspicious patterns detected in the document")

            st.markdown("---")
            st.markdown("### 📝 Document Preview")
            st.text_area("Extracted Text (preview)", result.get("preview_text", ""), height=200)

            with st.expander("📜 Full Extracted Text"):
                st.text(result.get("full_text", "")[:8000])

            # ===== Aesthetic PDF Ready Card (Glassmorphism + Logo) =====
            st.markdown("""
            <div class="pdf-ready-card">
                <div class="pdf-ready-badge">● READY</div>
                <div class="pdf-ready-logo">
                    <img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" alt="AI">
                </div>
                <div class="pdf-ready-content">
                    <div class="pdf-ready-title">✨ Document Ready for AI Analysis</div>
                    <div class="pdf-ready-desc">
                        Your PDF has been successfully processed and indexed.
                        Head over to the <b>🤖 Jarvis Chat</b> section to ask questions,
                        extract insights, and get instant AI-powered answers about this document.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# JARVIS CHAT PAGE
# ============================================================
elif page == "Jarvis Chat":
    st.markdown("""
        <div style="text-align:center; padding: 10px 0 5px 0;">
            <h2 style="color:#00d4ff; margin-bottom:4px;">🤖 Jarvis</h2>
            <p style="color:#8b9cb3; font-size:0.95rem; margin:0;">
                IntelliBank AI Assistant • Voice & Text Interaction
            </p>
        </div>
    """, unsafe_allow_html=True)

    pdf_loaded = bool(st.session_state.get("pdf_text"))

    if pdf_loaded:
        st.markdown("""
        <div style="text-align:center; margin: 10px 0 20px 0;">
            <span style="
                background: rgba(0, 200, 83, 0.15);
                color: #00c853;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                border: 1px solid rgba(0, 200, 83, 0.4);
            ">📄 PDF LOADED • Ready for questions</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; margin: 10px 0 20px 0;">
            <span style="
                background: rgba(139, 156, 179, 0.15);
                color: #8b9cb3;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                border: 1px solid rgba(139, 156, 179, 0.3);
            ">📄 No PDF loaded</span>
        </div>
        """, unsafe_allow_html=True)

    if pdf_loaded:
        if st.button("📄 Summarize PDF with AI", use_container_width=True):
            try:
                from app.jarvis.llm import summarize_pdf
                with st.spinner("🤖 AI is analyzing your document..."):
                    summary = summarize_pdf(st.session_state["pdf_text"])
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": "📄 Summarize the PDF"})
                st.session_state.messages.append({"role": "assistant", "content": summary})

                from app.utils.audit import log_action
                log_action(
                    action="pdf_summarize",
                    target="Jarvis Chat",
                    details="User requested PDF summary",
                )

                st.rerun()
            except Exception as e:
                st.error(f"❌ Summarization failed: {e}")

    speak_reply = st.toggle("🔊 Enable voice responses", value=True)

    if "messages" not in st.session_state:
        greeting = "Hello! I am **Jarvis**, your IntelliBank AI assistant.\n\n"
        if pdf_loaded:
            greeting += "I can see you've uploaded a PDF document. Ask me anything about it!\n\n"
        greeting += (
            "You can ask me about:\n"
            "- Transaction records\n"
            "- Fraud alerts\n"
            "- Account balances\n"
            "- PDF document queries\n\n"
            "**Examples:**\n"
            "- *How many transactions have been processed?*\n"
            "- *Show me all fraud transactions*\n"
            "- *What is the balance of account 1?*\n"
            "- *Summarize the PDF*\n"
            "- *What is the highest amount in the PDF?*"
        )
        st.session_state.messages = [{"role": "assistant", "content": greeting}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown("---")
    st.markdown("#### 🎤 Voice Command")
    st.caption("Click the microphone icon, speak your command, then stop recording")

    audio_data = st.audio_input("Record your command", key="jarvis_voice_mic")

    if audio_data is not None:
        try:
            from app.jarvis.voice import speech_to_text, speak
            from app.jarvis.brain import process_query

            with st.spinner("Processing your voice input..."):
                transcript = speech_to_text(audio_data.read(), "input.wav")

            if transcript and not transcript.lower().startswith(("error", "speech")):
                st.session_state.messages.append({"role": "user", "content": f"🎤 {transcript}"})
                response = process_query(transcript)
                st.session_state.messages.append({"role": "assistant", "content": response})

                from app.utils.audit import log_action
                log_action(
                    action="jarvis_query",
                    target="Voice Input",
                    details=f"Q: {transcript[:80]}",
                )

                if speak_reply:
                    try:
                        speak(response)
                    except Exception:
                        pass
                st.rerun()
            else:
                st.warning(f"Unable to process audio input: {transcript}")
        except Exception as e:
            st.error(f"❌ Voice processing error: {e}")

    st.markdown("")
    st.markdown("#### 💬 Type a Message")
    prompt = st.chat_input("Message Jarvis...")

    if prompt:
        try:
            from app.jarvis.brain import process_query
            from app.jarvis.voice import speak

            st.session_state.messages.append({"role": "user", "content": prompt})
            response = process_query(prompt)

            from app.utils.audit import log_action
            log_action(
                action="jarvis_query",
                target="Jarvis Chat",
                details=f"Q: {prompt[:80]}",
            )

            st.session_state.messages.append({"role": "assistant", "content": response})

            if speak_reply:
                try:
                    speak(response)
                except Exception:
                    pass
            st.rerun()
        except Exception as e:
            st.error(f"❌ Chat error: {e}")


# ============================================================
# AUDIT LOG PAGE
# ============================================================
elif page == "Audit Log":
    st.markdown("## 📋 System Audit Log")
    st.caption("Complete activity history of IntelliBank operations")

    from app.models.audit_log import AuditLog

    db = SessionLocal()
    try:
        logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(200).all()
    finally:
        db.close()

    if not logs:
        st.info("📭 No audit entries yet. Perform some actions to see logs here.")
    else:
        total_logs = len(logs)
        unique_actions = len(set(l.action for l in logs))
        today = datetime.utcnow().date()
        today_logs = len([l for l in logs if l.created_at and l.created_at.date() == today])

        c1, c2, c3 = st.columns(3)
        c1.metric("📋 Total Events", total_logs)
        c2.metric("🎯 Unique Actions", unique_actions)
        c3.metric("📅 Today", today_logs)

        st.markdown("---")

        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            action_filter = st.multiselect(
                "Filter by Action",
                sorted(set(l.action for l in logs)),
                default=[],
            )
        with col_f2:
            limit = st.selectbox("Show last", [25, 50, 100, 200], index=1)

        filtered = logs
        if action_filter:
            filtered = [l for l in logs if l.action in action_filter]
        filtered = filtered[:limit]

        st.markdown(f"### Recent Activity ({len(filtered)} entries)")

        icon_map = {
            "block_account": "🔒",
            "unblock_account": "🔓",
            "simulate": "🎮",
            "pdf_upload": "📄",
            "pdf_summarize": "🤖",
            "jarvis_query": "💬",
            "export": "📥",
        }

        for l in filtered:
            icon = icon_map.get(l.action, "📌")
            ts = l.created_at.strftime("%d %b %Y, %H:%M:%S") if l.created_at else "—"

            st.markdown(f"""
            <div style="
                background: rgba(26, 31, 46, 0.5);
                backdrop-filter: blur(15px);
                border-left: 4px solid #00d4ff;
                border-radius: 10px;
                padding: 12px 16px;
                margin-bottom: 8px;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b style="color:#00d4ff; font-size:1rem;">
                            {icon} {l.action.replace('_', ' ').title()}
                        </b>
                        {f'<span style="color:#8b9cb3;"> — {l.target}</span>' if l.target else ''}
                        <div style="color:#8b9cb3; font-size:0.85rem; margin-top:4px;">
                            {l.details or 'No additional details'}
                        </div>
                    </div>
                    <div style="text-align:right; color:#64748b; font-size:0.8rem;">
                        {ts}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#64748b; font-size:0.8rem; padding: 10px 0 20px 0;">
        IntelliBank © 2026 &nbsp;|&nbsp; AI & Data Science Final Year Project &nbsp;|&nbsp;
        FastAPI • Streamlit • XGBoost • LangChain
    </div>
""", unsafe_allow_html=True)