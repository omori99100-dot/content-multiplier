import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

    :root {
        --primary-start: #3b82f6;
        --primary-end: #8b5cf6;
        --primary-gradient: linear-gradient(90deg, var(--primary-start), var(--primary-end));
        --primary: var(--primary-start);
        --primary-dark: #2563eb;
        --accent-light: #7aa2f8;
        --bg-dark-1: #0F172A;
        --bg-dark-2: #1a2a4a;
        --bg-dark: linear-gradient(135deg, var(--bg-dark-1) 0%, var(--bg-dark-2) 100%);
        --bg-light-1: #EEF2FF;
        --bg-light-2: #C7D2FE;
        --bg-light: linear-gradient(135deg, var(--bg-light-1) 0%, var(--bg-light-2) 100%);
        --text-light: #F8FAFC;
        --text-dark: #1E293B;
        --text-muted: rgba(255, 255, 255, 0.6);
        --text-secondary: rgba(255, 255, 255, 0.82);
        --text-muted-light: rgba(0, 0, 0, 0.5);
        --text-secondary-light: #334155;
        --label-color: rgba(255, 255, 255, 0.75);
        --label-color-light: #475569;
        --link-hover: #93C5FD;
        --link-hover-light: #1D4ED8;
        --input-bg: rgba(255, 255, 255, 0.06);
        --input-border: rgba(255, 255, 255, 0.15);
        --input-bg-light: #FFFFFF;
        --input-border-light: #CBD5E1;
        --bg-glass: rgba(255, 255, 255, 0.05);
        --glass-bg: var(--bg-glass);
        --glass-border: rgba(255, 255, 255, 0.1);
        --glass-bg-light: rgba(255, 255, 255, 0.85);
        --glass-border-light: rgba(255, 255, 255, 0.9);
        --card-radius: 16px;
        --card-padding: 1.5rem;
        --btn-padding: 0.75rem 2rem;
        --btn-radius: 10px;
        --input-padding: 0.75rem 1rem;
        --input-radius: 12px;
        --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.3);
        --shadow-card-hover: 0 12px 40px rgba(0, 0, 0, 0.4);
        --shadow-card-light: 0 8px 32px rgba(0, 0, 0, 0.06);
        --gold: #F59E0B;
        --gold-light: #FCD34D;
        --scrollbar-track: rgba(255, 255, 255, 0.05);
        --scrollbar-thumb: rgba(255, 255, 255, 0.15);
        --scrollbar-thumb-hover: rgba(255, 255, 255, 0.25);
        --scrollbar-track-light: rgba(0, 0, 0, 0.05);
        --scrollbar-thumb-light: rgba(0, 0, 0, 0.15);
        --scrollbar-thumb-hover-light: rgba(0, 0, 0, 0.25);
        --alert-bg-light: rgba(255, 255, 255, 0.9);
        --border-light: #CBD5E1;
        --metric-bg-light: rgba(255, 255, 255, 0.8);
        --metric-border-light: rgba(0, 0, 0, 0.06);
        --metric-label-light: #64748B;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
    }

    .stApp {
        background: var(--bg-dark);
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(16px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(59, 130, 246, 0.6); }
    }

    .glass-card {
        animation: fadeIn 0.6s ease-out both;
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: var(--card-radius);
        padding: var(--card-padding);
        box-shadow: var(--shadow-card);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .glass-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: var(--shadow-card-hover);
    }

    .glass-card h1, .glass-card h2, .glass-card h3,
    .glass-card h4, .glass-card p, .glass-card label,
    .glass-card span, .glass-card div:not(.glass-card) {
        color: var(--text-light);
    }

    .stButton > button {
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: var(--btn-padding) !important;
        border: none !important;
        border-radius: var(--btn-radius) !important;
        background: var(--primary-gradient) !important;
        color: var(--text-light) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        transition: all 0.3s !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important;
        filter: brightness(1.1) !important;
    }

    .stButton > button:active {
        transform: scale(1) !important;
    }

    .stButton > button[kind="primary"] {
        animation: pulse 2s infinite;
    }

    .stButton > button[kind="secondary"] {
        background: transparent !important;
        box-shadow: none !important;
        border: 1.5px solid var(--input-border) !important;
        color: var(--text-secondary) !important;
        animation: none !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: none !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        color: var(--text-light) !important;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stSelectbox > div > div {
        background: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: var(--input-radius) !important;
        padding: var(--input-padding) !important;
        color: var(--text-light) !important;
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(79, 126, 248, 0.2) !important;
    }

    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: var(--label-color) !important;
        font-weight: 500 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
        color: var(--text-light) !important;
    }

    p, li, span, div {
        color: var(--text-secondary);
    }

    a {
        color: var(--primary) !important;
        text-decoration: none;
        transition: color 0.2s;
    }

    a:hover {
        color: var(--link-hover) !important;
        text-decoration: underline;
    }

    .stAlert {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--input-radius) !important;
    }

    .stAlert > div {
        color: var(--text-light) !important;
    }

    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--scrollbar-track); }
    ::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-thumb-hover); }

    .main-header {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent-light) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.1rem; color: var(--text-muted); margin-bottom: 2rem;
    }

    .popular-badge {
        background: #8b5cf6;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        text-align: center;
        margin-bottom: 10px;
        font-weight: bold;
    }

    .glass-card.popular {
        border: 2px solid #8b5cf6;
        transform: scale(1.05);
    }

    @media (prefers-color-scheme: light) {
        .stApp { background: var(--bg-light); }
        h1, h2, h3, h4, h5, h6 { color: var(--text-dark) !important; }
        p, li, span, div { color: var(--text-secondary-light); }
        .glass-card {
            background: var(--glass-bg-light);
            border: 1px solid var(--glass-border-light);
            box-shadow: var(--shadow-card-light);
        }
        .glass-card h1, .glass-card h2, .glass-card h3,
        .glass-card h4, .glass-card p, .glass-card label,
        .glass-card span, .glass-card div:not(.glass-card) { color: var(--text-dark); }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stSelectbox > div > div {
            background: var(--input-bg-light) !important; border: 1px solid var(--input-border-light) !important;
            color: var(--text-dark) !important;
        }
        .stTextInput label, .stTextArea label, .stSelectbox label { color: var(--label-color-light) !important; }
        a { color: var(--primary) !important; }
        a:hover { color: var(--link-hover-light) !important; }
        .stAlert { background: var(--alert-bg-light) !important; border: 1px solid var(--border-light) !important; }
        .stAlert > div { color: var(--text-dark) !important; }
        ::-webkit-scrollbar-track { background: var(--scrollbar-track-light); }
        ::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb-light); }
        ::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-thumb-hover-light); }
        .main-header {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sub-header { color: var(--text-muted-light); }
        .hero-ring { opacity: 0.05 !important; }
        .stMetric { background: var(--metric-bg-light); border: 1px solid var(--metric-border-light); }
        .stMetric label { color: var(--metric-label-light) !important; }
        .stMetric [data-testid='stMetricValue'] { color: var(--text-dark) !important; }
    }

    @media (max-width: 768px) {
        .glass-card { padding: 1.25rem; border-radius: var(--card-radius); }
        .main-header { font-size: 1.8rem !important; }
        .sub-header { font-size: 0.95rem !important; }
        .stButton > button { padding: 0.85rem 1.5rem !important; font-size: 1.05rem !important; width: 100% !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea { font-size: 16px !important; }
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        .topbar { padding: 0.75rem 1rem !important; gap: 0.5rem !important; }
        .topbar > div:first-child { gap: 0.5rem !important; }
        .topbar .avatar-circle-sm { width: 32px; height: 32px; font-size: 0.9rem; }
        .platform-pill { padding: 0.5rem 1rem; font-size: 0.85rem; }
        .stMetric { padding: 0.75rem; }
        .stTabs [data-baseweb="tab"] { padding: 0.4rem 1rem !important; font-size: 0.85rem !important; }
        .result-card { padding: 1rem; }
        .section-spacer { height: 2.5rem; }
    }
</style>
""", unsafe_allow_html=True)
