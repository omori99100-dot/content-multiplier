import os
import streamlit as st
from frontend.fonts import FONT_CSS
from frontend.style import inject_custom_css

from backend.database import (
    init_db, get_daily_usage, get_usage_limit, increment_daily_usage,
    save_generation, get_generation_history, get_referral_stats,
)
from backend.auth import authenticate_user, register_user as backend_register_user
from utils.generator import generate_platform_posts
from utils.article_fetcher import fetch_article
from frontend import translations as t

init_db()

st.set_page_config(page_title="ContentMultiplier AI", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

for k in ("user", "results", "ref_code"):
    if k not in st.session_state:
        st.session_state[k] = None
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "lang" not in st.session_state:
    st.session_state["lang"] = "ar"

LANG = st.session_state["lang"]

def _(key):
    return t._(key, LANG)

# ── SVG outline icons ───────────────────────────────────────────────────────
_SVG = {
    "lock": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "mail": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "image": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
    "rocket": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15l-3-3m0 0l3-3m-3 3H3m12 0h6M4.5 9.5L3 12l1.5 2.5M19.5 9.5L21 12l-1.5 2.5M9 19.5L12 21l3-1.5M9 4.5L12 3l3 1.5"/></svg>',
    "edit": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
    "home": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "key": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>',
    "bulb": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
    "globe": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "zap": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "star": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "heart": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
}

DIR = "rtl" if LANG == "ar" else "ltr"

st.markdown(FONT_CSS, unsafe_allow_html=True)
inject_custom_css()

st.markdown("""
<style>
    div[data-testid="stSidebarNav"] { display: none; }
    .stApp { direction: ltr; }
    .platform-pill {
        display: inline-flex; align-items: center; gap: 0.5rem;
        padding: 0.6rem 1.2rem; border-radius: 50px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: rgba(255,255,255,0.7); cursor: pointer;
        transition: all 0.2s; font-weight: 500; user-select: none;
    }
    .platform-pill:hover { background: rgba(255,255,255,0.12); transform: translateY(-2px); }
    .platform-pill.active { background: var(--primary-gradient); color: var(--text-light); border-color: transparent; }
    .result-card {
        animation: fadeSlideUp 0.5s ease-out both;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    }
    .result-card:nth-child(1) { animation-delay: 0.05s; }
    .result-card:nth-child(2) { animation-delay: 0.1s; }
    .result-card:nth-child(3) { animation-delay: 0.15s; }
    .result-card:nth-child(4) { animation-delay: 0.2s; }
    .result-card:nth-child(5) { animation-delay: 0.25s; }
    .topbar {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 2rem; margin: -5rem -5rem 2rem -5rem;
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .avatar-circle-sm {
        width: 40px; height: 40px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; font-weight: 700;
        background: var(--primary-gradient);
        flex-shrink: 0;
    }
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 50px !important; padding: 0.5rem 1.5rem !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        border-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }
    .stMetric { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.06); }
    .stMetric label { color: rgba(255,255,255,0.6) !important; }
    .stMetric [data-testid="stMetricValue"] { color: var(--text-light) !important; font-weight: 800; }
    .rtl { direction: rtl; text-align: right; }
    .rtl .icon-right { margin-left: 0.5rem; }
    .ltr .icon-left { margin-right: 0.5rem; }
    .auth-feature { display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem; }
    .auth-feature svg { flex-shrink: 0; margin-top: 2px; color: var(--primary); }
</style>
""", unsafe_allow_html=True)

def check_api_key() -> bool:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        try:
            key = st.secrets.get("OPENAI_API_KEY")
        except (AttributeError, KeyError, TypeError):
            try:
                key = st.secrets["OPENAI_API_KEY"]
            except (KeyError, TypeError):
                pass
    if key:
        return True
    st.markdown(f'<div style="max-width:600px;margin:4rem auto;">'
        f'<div class="glass-card" style="text-align:center;padding:3rem 2rem;">'
        f'<div style="font-size:3rem;margin-bottom:1rem;color:var(--primary);">{_SVG["key"]}</div>'
        f'<h2 style="margin-bottom:1rem;display:flex;align-items:center;justify-content:center;gap:0.5rem;">{_SVG["bulb"]} {"Welcome!" if LANG == "en" else "مرحباً بك!"}</h2>'
        f'<p style="opacity:0.8;line-height:1.7;margin-bottom:2rem;">'
        f'{"To start using the tool, please add your OpenAI API key in the app settings." if LANG == "en" else "لبدء استخدام الأداة، يرجى إضافة مفتاح OpenAI API في إعدادات التطبيق."}'
        f'</p>'
        f'<a href="https://platform.openai.com/api-keys" target="_blank" style="display:inline-block;padding:0.9rem 2rem;border-radius:var(--btn-radius);background:var(--primary);color:var(--text-light)!important;font-weight:700;text-decoration:none!important;">'
        f'{_SVG["key"]} {"Get API Key" if LANG == "en" else "الحصول على مفتاح API"}</a>'
        f'<p style="margin-top:1.5rem;font-size:0.85rem;opacity:0.5;display:flex;align-items:center;justify-content:center;gap:0.4rem;">'
        f'{_SVG["bulb"]} {"Add it in Streamlit Cloud → Settings → Secrets, or a .env file for local dev." if LANG == "en" else "أضف المفتاح في Streamlit Cloud → Settings → Secrets، أو في ملف .env للتشغيل المحلي."}'
        f'</p>'
        f'</div></div>', unsafe_allow_html=True)
    return False

def switch_lang():
    st.session_state["lang"] = "en" if LANG == "ar" else "ar"
    st.rerun()

def show_login():
    ref = st.query_params.get("ref") or st.session_state.get("ref_code")
    st.markdown(f'<h2 style="text-align:center;display:flex;align-items:center;justify-content:center;gap:0.5rem;">{_SVG["lock"]} {_("login_title")}</h2>', unsafe_allow_html=True)
    with st.form("login_form"):
        st.text_input(_("username"), key="login_user")
        st.text_input(_("password"), type="password", key="login_pass")
        st.markdown(f'<div style="text-align:{("left" if LANG == "en" else "right")};margin-top:-0.5rem;margin-bottom:0.75rem;">'
            f'<a href="#" style="font-size:0.85rem;opacity:0.7;">{_("forgot_password")}</a></div>', unsafe_allow_html=True)
        if st.form_submit_button(_("login_btn"), type="primary", use_container_width=True):
            user = authenticate_user(st.session_state.login_user, st.session_state.login_pass)
            if user:
                st.session_state["user"] = user
                st.session_state["page"] = "generate"
                st.rerun()
            else:
                st.error("Invalid username or password")
    st.markdown("---")
    st.markdown(f'<p style="text-align:center;opacity:0.7;">{_("no_account")}</p>', unsafe_allow_html=True)
    if st.button(_("create_account_btn"), use_container_width=True, type="secondary"):
        st.session_state["page"] = "register"
        if ref:
            st.session_state["ref_code"] = ref
        st.rerun()

def show_register():
    ref = st.session_state.get("ref_code")
    st.markdown(f'<h2 style="text-align:center;display:flex;align-items:center;justify-content:center;gap:0.5rem;">{_SVG["edit"]} {_("register_title")}</h2>', unsafe_allow_html=True)
    if ref:
        st.info(_SVG["star"] + " " + ("You were invited by a friend! Get a free month when you subscribe." if LANG == "en" else "تمت دعوتك من صديق! احصل على شهر مجاني عند الاشتراك."))
    with st.form("register_form"):
        st.text_input(_("full_name"), key="reg_name")
        st.text_input(_("username"), key="reg_user")
        st.text_input(_("email"), key="reg_email")
        st.text_input(_("password"), type="password", key="reg_pass")
        if st.form_submit_button(_("register_btn"), type="primary", use_container_width=True):
            result = backend_register_user(
                st.session_state.reg_user, st.session_state.reg_email,
                st.session_state.reg_name, st.session_state.reg_pass, ref,
            )
            if result.get("success"):
                st.success("Account created! Please log in.")
                st.session_state["page"] = "login"
                st.session_state["ref_code"] = None
                st.rerun()
            else:
                st.error(result.get("error", "Registration failed"))
    if st.button(_("back_to_login"), use_container_width=True, type="secondary"):
        st.session_state["page"] = "login"; st.rerun()

def show_topbar(user):
    initial = user["name"][0].upper() if user["name"] else "?"
    plan_badge = f'<span style="background:rgba(245,158,11,0.2);color:#FCD34D;padding:0.2rem 0.8rem;border-radius:50px;font-size:0.8rem;font-weight:700;">{user["subscription"].upper()}</span>'
    st.markdown(f'''
    <div class="topbar">
        <div style="display:flex;align-items:center;gap:0.75rem;">
            <div class="avatar-circle-sm">{initial}</div>
            <div>
                <div style="font-weight:600;">{user["name"]}</div>
                <div style="font-size:0.8rem;opacity:0.5;">@{user["username"]}</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:1rem;">
            {plan_badge}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button(_SVG["globe"], key="lang_topbar", help="English" if LANG == "ar" else "العربية"):
        st.session_state["lang"] = "en" if LANG == "ar" else "ar"
        st.rerun()

def show_nav():
    pages = [
        ("🚀", _("generate_tab"), "generate"),
        ("📊", _("dashboard_tab"), "dashboard"),
        ("💎", _("upgrade_tab"), "pricing"),
        ("🔗", "Referrals" if LANG == "en" else "الإحالات", "referral"),
    ]
    navcols = st.columns(len(pages))
    for i, (col, (icon, label, key)) in enumerate(zip(navcols, pages)):
        with col:
            if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True,
                         type="primary" if st.session_state["page"] == key else "secondary"):
                st.session_state["page"] = key
                st.rerun()

def show_generate():
    user = st.session_state["user"]
    show_topbar(user)
    show_nav()
    st.markdown(f'<div style="text-align:center;margin-bottom:2rem;"><h1 class="main-header">🚀 {_("app_title")}</h1><p class="sub-header">{_("app_subtitle")}</p></div>', unsafe_allow_html=True)

    used = get_daily_usage(user["id"])
    limit = get_usage_limit(user["id"])
    remaining = limit - used
    pct = min(used / limit * 100, 100) if limit else 0
    st.markdown(f'<div style="margin-bottom:1.5rem;"><div style="display:flex;justify-content:space-between;font-size:0.9rem;opacity:0.7;">'
        f'<span>{_("usage_title")}: {used}/{limit}</span><span>{_("remaining")}: {remaining}</span></div>'
        f'<div style="height:6px;border-radius:3px;background:rgba(255,255,255,0.08);overflow:hidden;">'
        f'<div style="width:{pct}%;height:100%;border-radius:3px;background:var(--primary-gradient);transition:width 0.3s;"></div></div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="glass-card" style="padding:2rem;">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs([_("generate_from_url"), _("generate_from_text")])

    with tab1:
        url = st.text_input("URL", placeholder=_("url_placeholder"), label_visibility="collapsed")
        tone_options = ["professional", "casual", "marketing", "humorous"]
        if LANG == "ar": tone_options += ["saudi", "egyptian"]
        tone = st.selectbox(_("tone_label"), tone_options, format_func=lambda x: {"professional": _("tone_professional"), "casual": _("tone_casual"), "marketing": _("tone_marketing"), "humorous": _("tone_humorous"), "saudi": _("tone_saudi"), "egyptian": _("tone_egyptian")}.get(x, x))

        st.markdown(f'<div style="margin:1rem 0 0.5rem;font-weight:600;">{_("platforms_label")}</div>', unsafe_allow_html=True)
        platform_icons = {"twitter": "🐦", "linkedin": "💼", "facebook": "📘", "instagram": "📸", "tiktok": "🎵"}
        platform_names = {"twitter": "Twitter/X", "linkedin": "LinkedIn", "facebook": "Facebook", "instagram": "Instagram", "tiktok": "TikTok"}
        selected = st.multiselect("", list(platform_icons.keys()), default=["twitter", "linkedin", "facebook"], label_visibility="collapsed",
            format_func=lambda x: f"{platform_icons[x]} {platform_names[x]}")

        if st.button(f"🚀 {_('generate_btn')}", type="primary", use_container_width=True):
            if url:
                if used >= limit:
                    st.error(f"Daily limit reached ({limit}). Upgrade your plan for more.")
                else:
                    with st.spinner(_("generating")):
                        article = fetch_article(url)
                        if not article:
                            st.error("Could not fetch article content")
                        else:
                            posts = generate_platform_posts(article["text"], selected, tone, LANG)
                            increment_daily_usage(user["id"])
                            for platform, data in posts.items():
                                save_generation(user["id"], url, article["text"][:500], article["title"], platform, data["text"], tone, data.get("image_url"))
                            st.session_state["results"] = posts
                            st.session_state["source_title"] = article["title"]
                            st.success(_("success")); st.rerun()
            else:
                st.warning(_("enter_url"))

    with tab2:
        input_text = st.text_area("", placeholder=_("text_placeholder"), height=200, label_visibility="collapsed")
        tone2 = st.selectbox(_("tone_label"), tone_options, key="tone2", format_func=lambda x: {"professional": _("tone_professional"), "casual": _("tone_casual"), "marketing": _("tone_marketing"), "humorous": _("tone_humorous"), "saudi": _("tone_saudi"), "egyptian": _("tone_egyptian")}.get(x, x))
        selected2 = st.multiselect("", list(platform_icons.keys()), default=["twitter", "linkedin", "facebook"], label_visibility="collapsed", key="plat2",
            format_func=lambda x: f"{platform_icons[x]} {platform_names[x]}")
        if st.button(f"🚀 {_('generate_btn')}", type="primary", use_container_width=True, key="btn2"):
            if input_text and len(input_text.strip()) > 20:
                if used >= limit:
                    st.error(f"Daily limit reached ({limit}). Upgrade your plan for more.")
                else:
                    with st.spinner(_("generating")):
                        posts = generate_platform_posts(input_text, selected2, tone2, LANG)
                        increment_daily_usage(user["id"])
                        for platform, data in posts.items():
                            save_generation(user["id"], "", input_text[:500], "Custom Text", platform, data["text"], tone2, data.get("image_url"))
                        st.session_state["results"] = posts
                        st.session_state["source_title"] = "Custom Text"
                        st.success(_("success")); st.rerun()
            else:
                st.warning(_("enter_text"))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("results"):
        st.markdown(f'<h2 style="margin:2rem 0 1rem;">📊 {_("results_title")}{" — " + st.session_state["source_title"] if st.session_state.get("source_title") else ""}</h2>', unsafe_allow_html=True)
        platform_icons = {"twitter": "🐦", "linkedin": "💼", "facebook": "📘", "instagram": "📸", "tiktok": "🎵"}
        for platform, data in st.session_state["results"].items():
            text = data if isinstance(data, str) else data.get("text", "")
            image_url = None if isinstance(data, str) else data.get("image_url")
            st.markdown(f'<div class="result-card">'
                f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.75rem;">'
                f'<span style="font-size:1.5rem;">{platform_icons.get(platform, "🌐")}</span>'
                f'<strong>{platform_names.get(platform, platform)}</strong></div>', unsafe_allow_html=True)
            if image_url:
                st.image(image_url, width=400)
            st.markdown(text)
            if st.button(f"📋 {_('copy_btn')}", key=f"copy_{platform}"):
                st.code(text, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
        if st.button(f"🔄 {_('clear_results')}"):
            st.session_state["results"] = None; st.rerun()

def show_dashboard():
    user = st.session_state["user"]
    show_topbar(user)
    show_nav()
    st.markdown(f'<h1 class="main-header" style="margin-bottom:2rem;">📊 {_("your_dashboard")}</h1>', unsafe_allow_html=True)

    used = get_daily_usage(user["id"])
    limit = get_usage_limit(user["id"])
    remaining = limit - used

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("🚀 " + _("used_today"), used, delta=None)
    mcol2.metric("📊 " + _("daily_limit"), limit)
    mcol3.metric("✅ " + _("remaining"), max(remaining, 0))
    mcol4.metric("💪 " + ("Plan" if LANG == "en" else "الباقة"), user["subscription"].upper())

    ref = get_referral_stats(user["id"])
    st.markdown(f'<div style="height:2rem;"></div>', unsafe_allow_html=True)
    rcol1, rcol2 = st.columns(2)
    rcol1.metric("👥 " + ("Invited" if LANG == "en" else "المدعوون"), ref.get("count", 0))
    rcol2.metric("🎁 " + ("Bonuses" if LANG == "en" else "المكافآت"), ref.get("bonuses", 0))

    st.markdown(f'<div class="glass-card" style="margin-top:2rem;">', unsafe_allow_html=True)
    st.markdown(f'<h3>📜 {_("generation_history")}</h3>', unsafe_allow_html=True)
    history = get_generation_history(user["id"])
    if history:
        for gen in history[:10]:
            label = f"<strong>{gen['platform'].upper()}</strong> — {gen['created_at'][:16]}"
            if gen.get('source_title'): label += f" | {gen['source_title'][:60]}"
            st.markdown(f'<details style="margin:0.5rem 0;padding:0.75rem;background:rgba(255,255,255,0.03);border-radius:10px;border:1px solid rgba(255,255,255,0.05);">'
                f'<summary style="cursor:pointer;font-weight:500;">{label}</summary>'
                f'<div style="margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid rgba(255,255,255,0.05);">', unsafe_allow_html=True)
            st.markdown(gen['generated_content'])
            if gen.get('image_url'): st.image(gen['image_url'], width=400)
            st.markdown('</div></details>', unsafe_allow_html=True)
    else:
        st.info(_("no_history"))
    st.markdown('</div>', unsafe_allow_html=True)

def show_referral():
    user = st.session_state["user"]
    show_topbar(user)
    show_nav()
    st.markdown(f'<h1 class="main-header">🔗 {"Referral Program" if LANG == "en" else "برنامج الإحالات"}</h1>', unsafe_allow_html=True)

    ref = get_referral_stats(user["id"])
    code = ref.get("code", "")

    st.markdown(f'<div class="glass-card" style="text-align:center;padding:2rem;max-width:500px;margin:0 auto 2rem;">', unsafe_allow_html=True)
    st.markdown(f'<h3>{"Your Referral Link" if LANG == "en" else "رابط الإحالة الخاص بك"}</h3>', unsafe_allow_html=True)
    st.code(code, language="text")
    if st.button("📋 " + ("Copy Link" if LANG == "en" else "نسخ الرابط")):
        st.write("Copied!")
    st.markdown('</div>', unsafe_allow_html=True)

    mcol1, mcol2 = st.columns(2)
    mcol1.metric("👥 " + ("People Invited" if LANG == "en" else "عدد المدعوين"), ref.get("count", 0))
    mcol2.metric("🎁 " + ("Bonuses Earned" if LANG == "en" else "المكافآت"), ref.get("bonuses", 0))

    st.markdown(f'<div class="glass-card" style="margin-top:2rem;">', unsafe_allow_html=True)
    st.markdown(f'<h3>💡 {"How it works" if LANG == "en" else "كيف يعمل؟"}</h3>', unsafe_allow_html=True)
    steps = [
        ("1️⃣ " + ("Share your link" if LANG == "en" else "شارك رابطك"),
         "You invite a friend" if LANG == "en" else "ترسل الرابط لصديق"),
        ("2️⃣ " + ("They subscribe" if LANG == "en" else "يشترك صديقك"),
         "They sign up & subscribe to any plan" if LANG == "en" else "يسجل ويشترك بأي باقة"),
        ("3️⃣ " + ("You get a free month!" if LANG == "en" else "تحصل على شهر مجاني!"),
         "We extend your subscription by 30 days" if LANG == "en" else "نمدد اشتراكك 30 يوماً"),
    ]
    for title, desc in steps:
        st.markdown(f"**{title}**")
        st.markdown(f'<p style="opacity:0.6;margin:-0.5rem 0 1rem 1.5rem;">{desc}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_pricing():
    user = st.session_state["user"]
    show_topbar(user)
    show_nav()
    st.markdown(f'<h1 class="main-header" style="display:flex;align-items:center;justify-content:center;gap:0.5rem;">{_SVG["star"]} {_("choose_plan")}</h1>', unsafe_allow_html=True)
    plans = [
        ("free", _SVG["heart"], _("free_plan"), "$0", _("free_desc")),
        ("basic", _SVG["star"], _("basic_plan"), "$9", _("basic_desc")),
        ("pro", _SVG["rocket"], _("pro_plan"), "$29", _("pro_desc")),
    ]
    pcols = st.columns(3)
    for col, (key, icon, name, price, desc) in zip(pcols, plans):
        with col:
            featured = key == "basic"
            margin = "margin-top:-1rem;" if featured else ""
            border = 'class="glass-card gold-border"' if featured else 'class="glass-card"'
            st.markdown(f'<div {border} style="text-align:center;{margin}position:relative;">', unsafe_allow_html=True)
            if featured:
                st.markdown(f'<div class="gold-badge" style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);padding:0.3rem 1.5rem;border-radius:20px;font-size:0.85rem;font-weight:700;white-space:nowrap;">{"الأكثر طلباً" if LANG == "ar" else "Most Popular"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom:0.5rem;">{icon}</div>', unsafe_allow_html=True)
            st.markdown(f'<h3 style="font-weight:700;font-size:1.3rem;">{name}</h3>')
            st.markdown(f'<div style="font-size:2.5rem;font-weight:800;margin:0.5rem 0;">{price}<span style="font-size:0.9rem;opacity:0.6;">/{"شهر" if LANG == "ar" else "mo"}</span></div>')
            for line in desc.split("\n"):
                st.markdown(f'<p style="margin:0.3rem 0;display:flex;align-items:center;justify-content:center;gap:0.4rem;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="20 6 9 17 4 12"/></svg> {line}</p>', unsafe_allow_html=True)
            if user["subscription"] == key:
                st.markdown(f'<div style="text-align:center;padding:0.75rem;margin-top:1.5rem;border-radius:var(--btn-radius);background:rgba(79,126,248,0.15);color:var(--primary);font-weight:600;font-size:1rem;display:flex;align-items:center;justify-content:center;gap:0.4rem;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> {_("active")}</div>', unsafe_allow_html=True)
            elif key != "free":
                st.markdown(f'<a href="?page=dashboard" style="display:block;text-align:center;padding:0.9rem;margin-top:1.5rem;border-radius:14px;background:var(--primary);color:#ffffff!important;font-weight:600;text-decoration:none!important;">{"Contact us to upgrade" if LANG == "en" else "تواصل معنا للترقية"}</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    checkout = st.query_params.get("checkout")
    if checkout == "success": st.success(_("payment_success"))
    elif checkout == "cancel": st.info(_("payment_cancel"))

    ref = st.query_params.get("ref")
    if ref:
        st.session_state["ref_code"] = ref

    if st.session_state["user"] is None:
        st.markdown(f'<div style="text-align:center;padding:3rem 1rem 0;">'
            f'<h1 class="main-header" style="display:flex;align-items:center;justify-content:center;gap:0.5rem;">{_SVG["rocket"]} {_("app_title")}</h1>'
            f'<p class="sub-header">{_("app_subtitle")}</p>'
            f'</div>', unsafe_allow_html=True)
        if st.button("🏠 " + ("← Home" if LANG == "en" else "→ الصفحة الرئيسية"), type="secondary"):
            st.switch_page("streamlit_app.py")
        st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)
        authcol1, authcol2 = st.columns(2)
        with authcol1:
            st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
            if st.session_state.get("page", "login") == "register":
                show_register()
            else:
                show_login()
            st.markdown('</div>', unsafe_allow_html=True)
        with authcol2:
            st.markdown(f'<div class="glass-card" style="height:100%;">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="text-align:center;display:flex;align-items:center;justify-content:center;gap:0.5rem;margin-bottom:1.5rem;">{_SVG["zap"]} {"Why ContentMultiplier?" if LANG == "en" else "لماذا مضاعف المحتوى؟"}</h3>', unsafe_allow_html=True)
            features_col = [
                ("globe", "Support Arabic, English, and dialects" if LANG == "en" else "يدعم العربية والإنجليزية واللهجات"),
                ("zap", "One article → optimized posts for all platforms" if LANG == "en" else "مقال واحد → منشورات مخصصة لكل المنصات"),
                ("mail", "Auto-delivery to your email" if LANG == "en" else "توصيل تلقائي لبريدك"),
                ("image", "Suggested images for each post" if LANG == "en" else "صور مقترحة لكل منشور"),
                ("star", "Save 5+ hours every week" if LANG == "en" else "وفر 5+ ساعات كل أسبوع"),
            ]
            for icon_key, text in features_col:
                st.markdown(f'<div class="auth-feature" style="display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:1rem;">'
                    f'<span style="flex-shrink:0;color:var(--primary);margin-top:2px;">{_SVG[icon_key]}</span>'
                    f'<span style="opacity:0.85;line-height:1.5;">{text}</span></div>', unsafe_allow_html=True)
            st.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:1.5rem 0;">', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;padding:0.5rem;border-radius:12px;background:rgba(79,126,248,0.08);border:1px solid rgba(79,126,248,0.15);">'
                f'<p style="font-style:italic;opacity:0.8;line-height:1.6;margin:0;">'
                f'&ldquo;{"Amazing tool! Saved me hours of content reformatting." if LANG == "en" else "أداة رائعة! وفرت علي ساعات طويلة من إعادة الصياغة."}&rdquo;</p>'
                f'<p style="margin:0.5rem 0 0;font-size:0.85rem;opacity:0.5;">— {"Ahmed, Software Developer" if LANG == "en" else "أحمد، مطور برمجيات"}</p>'
                f'</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        return

    if st.session_state["page"] in ("generate", "home") and not check_api_key():
        return

    if st.session_state["page"] == "dashboard": show_dashboard()
    elif st.session_state["page"] == "pricing": show_pricing()
    elif st.session_state["page"] == "referral": show_referral()
    else: show_generate()

main()
