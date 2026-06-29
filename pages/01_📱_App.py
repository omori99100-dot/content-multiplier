import streamlit as st
import os
from frontend.fonts import FONT_CSS

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

for k in ("user", "page", "results", "ref_code"):
    st.session_state.setdefault(k, None if k != "page" else "home")
st.session_state.setdefault("lang", "ar")

LANG = st.session_state["lang"]
DIR = "rtl" if LANG == "ar" else "ltr"

def _(key):
    return t._(key, LANG)

st.markdown(FONT_CSS, unsafe_allow_html=True)
st.markdown(f"""
<style>
    * {{ font-family: 'ShorooqN1', sans-serif !important; }}
    .main-header {{ text-align: center; padding: 1.5rem 0; direction: {DIR}; }}
    .post-card {{ background: #f8f9fa; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; border-{('right' if DIR == 'rtl' else 'left')}: 4px solid #0066cc; direction: {DIR}; text-align: {DIR}; }}
    .platform-badge {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold; margin-bottom: 0.5rem; }}
    .badge-twitter {{ background: #1DA1F2; color: white; }}
    .badge-linkedin {{ background: #0A66C2; color: white; }}
    .badge-facebook {{ background: #1877F2; color: white; }}
    .badge-instagram {{ background: #E4405F; color: white; }}
    .badge-tiktok {{ background: #000000; color: white; }}
    .usage-bar {{ height: 8px; border-radius: 4px; background: #e0e0e0; margin: 5px 0; }}
    .usage-fill {{ height: 8px; border-radius: 4px; background: #0066cc; }}
    div[data-testid="stSidebarNav"] {{ display: none; }}
    .stApp, .main > div, .element-container {{ direction: {DIR}; }}
</style>
""", unsafe_allow_html=True)

def switch_lang():
    st.session_state["lang"] = "en" if LANG == "ar" else "ar"
    st.rerun()

def show_login():
    ref = st.query_params.get("ref") or st.session_state.get("ref_code")
    st.markdown(f"## 🔐 {_('login_title')}")
    with st.form("login_form"):
        st.text_input(_("username"), key="login_user")
        st.text_input(_("password"), type="password", key="login_pass")
        if st.form_submit_button(_("login_btn"), type="primary", use_container_width=True):
            user = authenticate_user(st.session_state.login_user, st.session_state.login_pass)
            if user:
                st.session_state["user"] = user
                st.session_state["page"] = "generate"
                st.rerun()
            else:
                st.error("Invalid username or password")
    st.markdown("---")
    st.markdown(_("no_account"))
    if st.button(_("create_account_btn"), use_container_width=True):
        st.session_state["page"] = "register"
        if ref:
            st.session_state["ref_code"] = ref
        st.rerun()

def show_register():
    ref = st.session_state.get("ref_code")
    st.markdown(f"## 📝 {_('register_title')}")
    if ref:
        st.info("🎉 " + ("You were invited by a friend! Get a free month when you subscribe." if LANG == "en" else "تمت دعوتك من صديق! احصل على شهر مجاني عند الاشتراك."))
    with st.form("register_form"):
        st.text_input(_("full_name"), key="reg_name")
        st.text_input(_("username"), key="reg_user")
        st.text_input(_("email"), key="reg_email")
        st.text_input(_("password"), type="password", key="reg_pass")
        if st.form_submit_button(_("register_btn"), type="primary", use_container_width=True):
            result = backend_register_user(
                st.session_state.reg_user,
                st.session_state.reg_email,
                st.session_state.reg_name,
                st.session_state.reg_pass,
                ref,
            )
            if result.get("success"):
                st.success("Account created! Please log in.")
                st.session_state["page"] = "login"
                st.session_state["ref_code"] = None
                st.rerun()
            else:
                st.error(result.get("error", "Registration failed"))
    if st.button(_("back_to_login"), use_container_width=True):
        st.session_state["page"] = "login"; st.rerun()

def show_sidebar():
    user = st.session_state["user"]
    with st.sidebar:
        st.markdown(f"### 👋 {_('welcome')}, {user['name']}")
        st.markdown(f"**{_('plan_label')}:** {user['subscription'].upper()}")
        used = get_daily_usage(user["id"])
        limit = get_usage_limit(user["id"])
        remaining = limit - used
        pct = min(used / limit * 100, 100) if limit else 0
        st.markdown(f"**{_('usage_title')}:** {used}/{limit}")
        st.markdown(f'<div class="usage-bar"><div class="usage-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)
        st.caption(f"{_('remaining')}: {remaining}")
        st.markdown("---")
        if st.button(f"🚀 {_('generate_tab')}", use_container_width=True):
            st.session_state["page"] = "generate"; st.rerun()
        if st.button(f"📊 {_('dashboard_tab')}", use_container_width=True):
            st.session_state["page"] = "dashboard"; st.rerun()
        if st.button(f"💎 {_('upgrade_tab')}", use_container_width=True):
            st.session_state["page"] = "pricing"; st.rerun()
        if st.button(f"🔗 {'Referrals' if LANG == 'en' else 'الإحالات'}", use_container_width=True):
            st.session_state["page"] = "referral"; st.rerun()
        st.markdown("---")
        st.button("🌐 " + ("English" if LANG == "ar" else "العربية"), on_click=switch_lang, use_container_width=True)
        if st.button(f"🚪 {_('logout')}", use_container_width=True):
            st.session_state["user"] = None; st.session_state["results"] = None; st.session_state["page"] = "landing"; st.rerun()

def show_generate():
    show_sidebar()
    st.markdown(f'<div class="main-header"><h1>🚀 {_("app_title")}</h1><p>{_("app_subtitle")}</p></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs([_("generate_from_url"), _("generate_from_text")])

    with tab1:
        url = st.text_input("URL", placeholder=_("url_placeholder"), label_visibility="collapsed")
        tone_options = ["professional", "casual", "marketing", "humorous"]
        if LANG == "ar":
            tone_options += ["saudi", "egyptian"]
        tone = st.selectbox(_("tone_label"), tone_options, format_func=lambda x: {"professional": _("tone_professional"), "casual": _("tone_casual"), "marketing": _("tone_marketing"), "humorous": _("tone_humorous"), "saudi": _("tone_saudi"), "egyptian": _("tone_egyptian")}.get(x, x))
        platforms = st.multiselect(_("platforms_label"), ["twitter", "linkedin", "facebook", "instagram", "tiktok"], default=["twitter", "linkedin", "facebook"])
        if st.button(f"🚀 {_('generate_btn')}", type="primary", use_container_width=True):
            if url:
                user = st.session_state["user"]
                used = get_daily_usage(user["id"])
                limit = get_usage_limit(user["id"])
                if used >= limit:
                    st.error(f"Daily limit reached ({limit}). Upgrade your plan for more.")
                else:
                    with st.spinner(_("generating")):
                        article = fetch_article(url)
                        if not article:
                            st.error("Could not fetch article content")
                        else:
                            source_text = article["text"]
                            source_title = article["title"]
                            posts = generate_platform_posts(source_text, platforms, tone, LANG)
                            increment_daily_usage(user["id"])
                            for platform, data in posts.items():
                                save_generation(user["id"], url, source_text[:500], source_title, platform, data["text"], tone, data.get("image_url"))
                            st.session_state["results"] = posts
                            st.session_state["source_title"] = source_title
                            st.success(_("success")); st.rerun()
            else: st.warning(_("enter_url"))

    with tab2:
        input_text = st.text_area("", placeholder=_("text_placeholder"), height=200, label_visibility="collapsed")
        tone2_options = ["professional", "casual", "marketing", "humorous"]
        if LANG == "ar": tone2_options += ["saudi", "egyptian"]
        tone2 = st.selectbox(_("tone_label"), tone2_options, key="tone2", format_func=lambda x: {"professional": _("tone_professional"), "casual": _("tone_casual"), "marketing": _("tone_marketing"), "humorous": _("tone_humorous"), "saudi": _("tone_saudi"), "egyptian": _("tone_egyptian")}.get(x, x))
        platforms2 = st.multiselect(_("platforms_label"), ["twitter", "linkedin", "facebook", "instagram", "tiktok"], default=["twitter", "linkedin", "facebook"], key="platforms2")
        if st.button(f"🚀 {_('generate_btn')}", type="primary", use_container_width=True, key="btn2"):
            if input_text and len(input_text.strip()) > 20:
                user = st.session_state["user"]
                used = get_daily_usage(user["id"])
                limit = get_usage_limit(user["id"])
                if used >= limit:
                    st.error(f"Daily limit reached ({limit}). Upgrade your plan for more.")
                else:
                    with st.spinner(_("generating")):
                        posts = generate_platform_posts(input_text, platforms2, tone2, LANG)
                        increment_daily_usage(user["id"])
                        for platform, data in posts.items():
                            save_generation(user["id"], "", input_text[:500], "Custom Text", platform, data["text"], tone2, data.get("image_url"))
                        st.session_state["results"] = posts
                        st.session_state["source_title"] = "Custom Text"
                        st.success(_("success")); st.rerun()
            else: st.warning(_("enter_text"))

    if "results" in st.session_state and st.session_state["results"]:
        st.markdown("---")
        src = st.session_state.get("source_title", "")
        st.markdown(f"## 📊 {_('results_title')}" + (f" - {src}" if src else ""))
        badge_map = {"twitter": ("badge-twitter", "🐦 Twitter / X"), "linkedin": ("badge-linkedin", "💼 LinkedIn"), "facebook": ("badge-facebook", "📘 Facebook"), "instagram": ("badge-instagram", "📸 Instagram"), "tiktok": ("badge-tiktok", "🎵 TikTok")}
        for platform, data in st.session_state["results"].items():
            text = data if isinstance(data, str) else data.get("text", "")
            image_url = None if isinstance(data, str) else data.get("image_url")
            badge_class, badge_label = badge_map.get(platform, ("", platform))
            st.markdown(f'<div class="post-card">', unsafe_allow_html=True)
            st.markdown(f'<span class="platform-badge {badge_class}">{badge_label}</span>', unsafe_allow_html=True)
            if image_url: st.image(image_url, width=400)
            st.markdown(text)
            if st.button(f"📋 {_('copy_btn')}", key=f"copy_{platform}"): st.code(text, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
        if st.button(f"🔄 {_('clear_results')}"): st.session_state["results"] = None; st.rerun()

def show_dashboard():
    show_sidebar()
    st.markdown(f"## 📊 {_('your_dashboard')}")
    user = st.session_state["user"]
    used = get_daily_usage(user["id"])
    limit = get_usage_limit(user["id"])
    remaining = limit - used
    col1, col2, col3 = st.columns(3)
    col1.metric(_("used_today"), used)
    col2.metric(_("daily_limit"), limit)
    col3.metric(_("remaining"), remaining)
    st.markdown(f"### 📜 {_('generation_history')}")
    history = get_generation_history(user["id"])
    if history:
        for gen in history:
            label = f"{gen['created_at'][:16]} - {gen['platform'].upper()}"
            if gen.get('source_title'): label += f" - {gen['source_title'][:50]}"
            with st.expander(label):
                st.markdown(f"**Platform:** {gen['platform']}  **Tone:** {gen.get('tone', 'professional')}")
                if gen.get('image_url'): st.image(gen['image_url'], width=400)
                st.markdown(gen['generated_content'])
                if gen.get('source_url'): st.markdown(f"**Source:** {gen['source_url']}")
    else: st.info(_("no_history"))

def show_referral():
    show_sidebar()
    st.markdown("## 🔗 " + ("Referral Program" if LANG == "en" else "برنامج الإحالات"))
    user = st.session_state["user"]
    ref = get_referral_stats(user["id"])
    code = ref.get("code", "")
    st.markdown(f"### {'Your Referral Link' if LANG == 'en' else 'رابط الإحالة الخاص بك'}")
    st.code(code, language="text")
    if st.button("📋 " + ("Copy Link" if LANG == "en" else "نسخ الرابط")):
        st.write("Copied!")
    col1, col2 = st.columns(2)
    col1.metric("👥 " + ("People Invited" if LANG == "en" else "عدد المدعوين"), ref.get("count", 0))
    col2.metric("🎁 " + ("Bonuses Earned" if LANG == "en" else "المكافآت"), ref.get("bonuses", 0))
    st.markdown("---")
    st.markdown("### 💡 " + ("How it works" if LANG == "en" else "كيف يعمل؟"))
    steps = [
        ("1️⃣ " + ("Share your link" if LANG == "en" else "شارك رابطك"), "You invite a friend" if LANG == "en" else "ترسل الرابط لصديق"),
        ("2️⃣ " + ("They subscribe" if LANG == "en" else "يشترك صديقك"), "They sign up & subscribe to any plan" if LANG == "en" else "يسجل ويشترك بأي باقة"),
        ("3️⃣ " + ("You get a free month!" if LANG == "en" else "تحصل على شهر مجاني!"), "We extend your subscription by 30 days" if LANG == "en" else "نمدد اشتراكك 30 يوماً"),
    ]
    for title, desc in steps:
        st.markdown(f"**{title}**")
        st.markdown(f"<p style='color:#666;margin:-0.5rem 0 1rem 1.5rem;'>{desc}</p>", unsafe_allow_html=True)

def show_pricing():
    show_sidebar()
    st.markdown(f"## 💎 {_('choose_plan')}")
    user = st.session_state["user"]
    col1, col2, col3 = st.columns(3)
    plans = [("free", "🆓", _("free_plan"), "$0", _("free_desc")), ("basic", "⭐", _("basic_plan"), "$9", _("basic_desc")), ("pro", "🚀", _("pro_plan"), "$29", _("pro_desc"))]
    for col, (key, icon, name, price, desc) in zip([col1, col2, col3], plans):
        with col:
            st.markdown(f"### {icon} {name}"); st.markdown(f"**{price}/" + ("شهر" if LANG == "ar" else "mo") + "**")
            for line in desc.split("\n"): st.markdown(f"- {line}")
            if user["subscription"] == key: st.button(f"✅ {_('active')}", disabled=True, use_container_width=True)
            elif key != "free":
                stripe_key = os.getenv("STRIPE_SECRET_KEY")
                if stripe_key:
                    st.button(_("subscribe_basic") if key == "basic" else _("subscribe_pro"), type="primary", use_container_width=True)
                else:
                    st.info("💬 " + ("Contact us to upgrade" if LANG == "en" else "تواصل معنا للترقية"))

def main():
    checkout = st.query_params.get("checkout")
    if checkout == "success": st.success(_("payment_success"))
    elif checkout == "cancel": st.info(_("payment_cancel"))

    ref = st.query_params.get("ref")
    if ref:
        st.session_state["ref_code"] = ref

    if st.session_state["user"] is None:
        st.markdown(f'<div style="text-align:center;padding:3rem;"><h1>🚀 {_("app_title")}</h1><p>{_("app_subtitle")}</p><a href="?page=landing" target="_self" style="display:inline-block;padding:1rem 3rem;background:#0066cc;color:white;border-radius:50px;text-decoration:none;font-size:1.2rem;font-weight:bold;">{"Home" if LANG == "en" else "الصفحة الرئيسية"}</a></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: show_login()
        with col2:
            st.markdown("### " + ("New here?" if LANG == "en" else "جديد هنا؟"))
            st.markdown("🚀 " + ("ContentMultiplier AI converts one article into optimized posts for all platforms." if LANG == "en" else "مضاعف المحتوى يحوّل مقالاً واحداً إلى منشورات مخصصة لكل المنصات."))
            st.markdown("✅ " + ("Support Arabic, English, and dialects" if LANG == "en" else "يدعم العربية والإنجليزية واللهجات"))
            st.markdown("📧 " + ("Auto-delivery to your email" if LANG == "en" else "توصيل تلقائي لبريدك"))
            st.markdown("🖼️ " + ("Suggested images for each post" if LANG == "en" else "صور مقترحة لكل منشور"))
    elif st.session_state["page"] == "dashboard": show_dashboard()
    elif st.session_state["page"] == "pricing": show_pricing()
    elif st.session_state["page"] == "referral": show_referral()
    else: show_generate()

main()
