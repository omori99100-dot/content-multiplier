import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
    }


    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(16px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(37, 99, 235, 0.6); }
    }

    .glass-card {
        animation: fadeIn 0.6s ease-out both;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .glass-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }

    .glass-card h1, .glass-card h2, .glass-card h3,
    .glass-card h4, .glass-card p, .glass-card label,
    .glass-card span, .glass-card div:not(.glass-card) {
        color: #fff;
    }

    .stButton > button {
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stButton > button[kind="primary"] {
        animation: pulse 2s infinite;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }

    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 500 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', 'Tajawal', system-ui, sans-serif !important;
        color: #fff !important;
    }

    p, li, span, div {
        color: rgba(255, 255, 255, 0.85);
    }

    a {
        color: #60A5FA !important;
        text-decoration: none;
        transition: color 0.2s;
    }

    a:hover {
        color: #93C5FD !important;
        text-decoration: underline;
    }

    .stAlert {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
    }

    .stAlert > div {
        color: #fff !important;
    }

    .stSpinner > div {
        border-color: #60A5FA transparent transparent transparent !important;
    }

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.25);
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.65);
        margin-bottom: 2rem;
    }
    @media (prefers-color-scheme: light) {
        .stApp {
            background: linear-gradient(135deg, #EEF2FF 0%, #C7D2FE 100%);
        }
        h1, h2, h3, h4, h5, h6 { color: #1E293B !important; }
        p, li, span, div { color: #334155; }
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.9);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
        }
        .glass-card h1, .glass-card h2, .glass-card h3,
        .glass-card h4, .glass-card p, .glass-card label,
        .glass-card span, .glass-card div:not(.glass-card) {
            color: #1E293B;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stSelectbox > div > div {
            background: #fff !important;
            border: 1px solid #CBD5E1 !important;
            color: #1E293B !important;
        }
        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: #475569 !important;
        }
        a { color: #2563EB !important; }
        a:hover { color: #1D4ED8 !important; }
        .stAlert {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid #CBD5E1 !important;
        }
        .stAlert > div { color: #1E293B !important; }
        ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.05); }
        ::-webkit-scrollbar-thumb { background: rgba(0, 0, 0, 0.15); }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.25); }
        .main-header {
            background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sub-header { color: rgba(0, 0, 0, 0.5); }
        .stMetric { background: rgba(255,255,255,0.8); border: 1px solid rgba(0,0,0,0.06); }
        .stMetric label { color: #64748B !important; }
        .stMetric [data-testid='stMetricValue'] { color: #1E293B !important; }
    }

    @media (max-width: 768px) {
        .glass-card { padding: 1.25rem; border-radius: 16px; }
        .main-header { font-size: 1.8rem !important; }
        .sub-header { font-size: 0.95rem !important; }
        .stButton > button {
            padding: 0.85rem 1.5rem !important;
            font-size: 1.05rem !important;
            width: 100% !important;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-size: 16px !important;
        }
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
