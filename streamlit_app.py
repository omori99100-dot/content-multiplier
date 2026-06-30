import streamlit as st
from frontend.fonts import FONT_CSS
from frontend.style import inject_custom_css

# Page configuration — must be first Streamlit command
st.set_page_config(
    page_title="ContentMultiplier AI - ضاعف محتواك",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LANG = st.session_state.get("lang", "ar")

page_param = st.query_params.get("page")
if page_param == "app":
    st.switch_page("pages/01_📱_App.py")
elif page_param == "privacy":
    st.switch_page("pages/02_🔒_Privacy_Policy.py")

# ── SEO meta tags (injected via JS to reach <head>) ─────────────────────────
OG_SCRIPT = """<script>
(function() {
    var d=document;
    function m(a){var e=d.createElement("meta");for(var k in a)e.setAttribute(k,a[k]);d.head.appendChild(e);}
    m({"property":"og:title","content":"\u0636\u0627\u0639\u0641 \u0645\u062d\u062a\u0648\u0627\u0643 \u0628\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a | ContentMultiplier AI"});
    m({"property":"og:description","content":"\u0623\u062f\u0627\u0629 \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631 \u062a\u062d\u0648\u0644 \u0623\u064a \u0645\u0642\u0627\u0644 \u0625\u0644\u0649 \u0645\u0646\u0634\u0648\u0631\u0627\u062a \u0627\u062d\u062a\u0631\u0627\u0641\u064a\u0629 \u0644\u062c\u0645\u064a\u0639 \u0645\u0646\u0635\u0627\u062a \u0627\u0644\u062a\u0648\u0627\u0635\u0644."});
    m({"property":"og:image","content":"https://opencode.ai/favicon.ico"});
    m({"property":"og:type","content":"website"});
    m({"name":"twitter:card","content":"summary_large_image"});
    m({"name":"twitter:title","content":"\u0636\u0627\u0639\u0641 \u0645\u062d\u062a\u0648\u0627\u0643 \u0628\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a | ContentMultiplier AI"});
    m({"name":"twitter:description","content":"\u0623\u062f\u0627\u0629 \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631 \u062a\u062d\u0648\u0644 \u0623\u064a \u0645\u0642\u0627\u0644 \u0625\u0644\u0649 \u0645\u0646\u0634\u0648\u0631\u0627\u062a \u0627\u062d\u062a\u0631\u0627\u0641\u064a\u0629 \u0644\u062c\u0645\u064a\u0639 \u0645\u0646\u0635\u0627\u062a \u0627\u0644\u062a\u0648\u0627\u0635\u0644."});
})();
</script>"""
st.markdown(OG_SCRIPT, unsafe_allow_html=True)

st.markdown(FONT_CSS, unsafe_allow_html=True)
inject_custom_css()

# ── Language switcher ──────────────────────────────────────────────────────
def switch_lang():
    st.session_state["lang"] = "en" if LANG == "ar" else "ar"
    st.rerun()

hero_anim = """
<style>
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .hero-section { text-align: center; padding: 6rem 1rem 4rem; animation: fadeSlideUp 0.8s ease-out; }
    .hero-section h1 { animation: fadeSlideUp 0.8s ease-out 0.1s both; }
    .hero-section p { animation: fadeSlideUp 0.8s ease-out 0.2s both; }
    .hero-section .hero-actions { animation: fadeSlideUp 0.8s ease-out 0.3s both; }
    .hero-section .hero-stats { animation: fadeSlideUp 0.8s ease-out 0.4s both; }
    .btn-pulse {
        display: inline-block; padding: 1.2rem 3.5rem;
        background: var(--primary);
        color: var(--text-light) !important; font-size: 1.3rem; font-weight: 800;
        border-radius: 60px; text-decoration: none !important;
        animation: pulse 2s infinite;
        transition: transform 0.2s;
    }
    .btn-pulse:hover { transform: translateY(-3px); }
    .hero-decoration {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 500px; height: 500px; pointer-events: none; z-index: 0;
    }
    .hero-ring {
        position: absolute; inset: 0; border-radius: 50%;
        background: conic-gradient(from 0deg, var(--primary), var(--accent-light), var(--primary-dark), var(--primary));
        opacity: 0.08; animation: spin 20s linear infinite;
        mask: radial-gradient(circle, transparent 45%, #000 46%, #000 54%, transparent 55%);
        -webkit-mask: radial-gradient(circle, transparent 45%, #000 46%, #000 54%, transparent 55%);
    }
    .hero-dots {
        position: absolute; inset: 0;
        background-image: radial-gradient(circle, rgba(96,165,250,0.25) 1.5px, transparent 1.5px);
        background-size: 30px 30px;
        animation: drift 30s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes drift {
        0% { transform: translate(0, 0); }
        50% { transform: translate(10px, -10px); }
        100% { transform: translate(0, 0); }
    }
    .feature-enter { animation: fadeSlideUp 0.6s ease-out both; }
    .feature-enter:nth-child(1) { animation-delay: 0.1s; }
    .feature-enter:nth-child(2) { animation-delay: 0.2s; }
    .feature-enter:nth-child(3) { animation-delay: 0.3s; }
    .section-spacer { height: 5rem; }
    .gold-border { border: 2px solid #4f46e5 !important; }
    .gold-badge { background: #4f46e5; color: #ffffff !important; }
    .avatar-circle {
        width: 64px; height: 64px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem; margin: 0 auto 1rem;
        background: var(--primary-gradient);
    }
</style>
"""
st.markdown(hero_anim, unsafe_allow_html=True)

# ── Hero section ───────────────────────────────────────────────────────────
col1, _, col2 = st.columns([1, 8, 1])
with col2:
    st.button("🌐 " + ("English" if LANG == "ar" else "العربية"), on_click=switch_lang, use_container_width=True)

st.markdown('<div class="hero-section" style="position:relative;overflow:hidden;">'
    '<div class="hero-decoration"><div class="hero-ring"></div><div class="hero-dots"></div></div>'
    '<div style="position:relative;z-index:1;">', unsafe_allow_html=True)

hero_title = ("🚀 ضاعف محتواك لمنصات التواصل<br>في دقائق بالذكاء الاصطناعي" if LANG == "ar"
              else "🚀 Multiply Your Content Across<br>Social Platforms in Minutes")
hero_desc = ("حوّل مقالاً واحداً إلى منشورات مخصصة وجاهزة للنشر على تويتر، لينكدإن، فيسبوك، انستغرام، وتيك توك" if LANG == "ar"
             else "Convert one article into platform-optimized posts for Twitter, LinkedIn, Facebook, Instagram & TikTok")

st.markdown(f'<h1 class="main-header">{hero_title}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header" style="max-width:650px;margin:0 auto 2rem;">{hero_desc}</p>', unsafe_allow_html=True)

cta_main = "ابدأ الآن مجاناً" if LANG == "ar" else "Start Free"
cta_login = "تسجيل الدخول" if LANG == "ar" else "Login"
st.markdown(f'<div class="hero-actions">'
    f'<a href="?page=app" class="btn-pulse">{cta_main} ✨</a>&nbsp;&nbsp;'
    f'<a href="?page=app" class="glass-card" style="display:inline-block;padding:1rem 2.5rem;border-radius:var(--btn-radius);text-decoration:none!important;color:var(--text-light)!important;font-weight:700;">{cta_login} 🔐</a>'
    f'</div>', unsafe_allow_html=True)

stats_ar = [("📝", "٥٠+", "قالب"), ("🌍", "5", "منصات"), ("🆓", "7", "أيام تجربة")]
stats_en = [("📝", "50+", "Templates"), ("🌍", "5", "Platforms"), ("🆓", "7", "Days Free Trial")]
stats = stats_ar if LANG == "ar" else stats_en
stats_html = '<div class="hero-stats" style="display:flex;justify-content:center;gap:3rem;flex-wrap:wrap;margin-top:2.5rem;">'
for icon, num, label in stats:
    stats_html += f'<div style="text-align:center;"><div style="font-size:2rem;">{icon}</div><div style="font-size:1.5rem;font-weight:800;">{num}</div><div style="opacity:0.7;">{label}</div></div>'
stats_html += '</div>'
st.markdown(stats_html, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# ── Features section ───────────────────────────────────────────────────────
features_title = "✨ لماذا مضاعف المحتوى؟" if LANG == "ar" else "✨ Why ContentMultiplier?"
st.markdown(f'<h2 style="text-align:center;font-size:2rem;font-weight:800;margin-bottom:3rem;">{features_title}</h2>', unsafe_allow_html=True)

features = [
    ("⏱️", "وفر 5 ساعات أسبوعياً" if LANG == "ar" else "Save 5 Hours/Week",
     "دع الذكاء الاصطناعي يعيد صياغة محتواك لكل منصة في ثوانٍ بدلاً من ساعات العمل اليدوي." if LANG == "ar"
     else "Let AI rewrite your content for each platform in seconds instead of hours of manual work."),
    ("🎯", "منشورات محسّنة لكل منصة" if LANG == "ar" else "Platform-Optimized Posts",
     "كل منصة لها طابعها الخاص: تويتر للتغريدات القصيرة، لينكدإن للمحتوى المهني، تيك توك للفيديوهات الجذابة." if LANG == "ar"
     else "Each platform gets its own style: short tweets, professional LinkedIn, engaging TikTok videos."),
    ("🌐", "دعم عربي كامل + لهجات" if LANG == "ar" else "Full Arabic + Dialects",
     "أول أداة تدعم اللهجات السعودية والمصرية بجانب الفصحى، مع هاشتاغات ومحتوى عربي أصيل." if LANG == "ar"
     else "First tool supporting Saudi & Egyptian dialects alongside formal Arabic with authentic hashtags."),
]

cols = st.columns(3)
for i, (col, (icon, title, desc)) in enumerate(zip(cols, features)):
    with col:
        st.markdown(f'<div class="feature-enter">'
            f'<div class="glass-card" style="text-align:center;">'
            f'<div style="font-size:4rem;margin-bottom:1rem;">{icon}</div>'
            f'<h3 style="font-size:1.3rem;font-weight:700;margin-bottom:0.75rem;">{title}</h3>'
            f'<p style="opacity:0.75;line-height:1.7;">{desc}</p>'
            f'</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# ── SVG pricing icons ────────────────────────────────────────────────────
pricing_title = "💰 خطط الأسعار" if LANG == "ar" else "💰 Pricing Plans"
st.markdown(f'<h2 style="text-align:center;font-size:2rem;font-weight:800;margin-bottom:3rem;">{pricing_title}</h2>', unsafe_allow_html=True)

_PRICING_ICONS = {
    "free": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "basic": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "pro": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15l-3-3m0 0l3-3m-3 3H3m12 0h6M4.5 9.5L3 12l1.5 2.5M19.5 9.5L21 12l-1.5 2.5M9 19.5L12 21l3-1.5M9 4.5L12 3l3 1.5"/></svg>',
}

# ── Pricing section ────────────────────────────────────────────────────────
_PRICING_PLANS = [
    ("free", "مجاني" if LANG == "ar" else "Free", "$0",
     ["5 توليدات/يوم" if LANG == "ar" else "5 generations/day",
      "منصات أساسية" if LANG == "ar" else "Basic platforms",
      "نبرة قياسية" if LANG == "ar" else "Standard tone"], False),
    ("basic", "أساسي" if LANG == "ar" else "Basic", "$9",
     ["30 توليدة/يوم" if LANG == "ar" else "30 generations/day",
      "جميع المنصات" if LANG == "ar" else "All platforms",
      "جميع النبرات" if LANG == "ar" else "All tones",
      "تصدير PDF" if LANG == "ar" else "PDF export"], True),
    ("pro", "احترافي" if LANG == "ar" else "Pro", "$29",
     ["100 توليدة/يوم" if LANG == "ar" else "100 generations/day",
      "جميع المنصات" if LANG == "ar" else "All platforms",
      "جميع النبرات + لهجات" if LANG == "ar" else "All tones + dialects",
      "تصدير PDF" if LANG == "ar" else "PDF export",
      "دعم أولوية" if LANG == "ar" else "Priority support"], False),
]

pcols = st.columns(3)
for i, (col, (key, name, price, feats, featured)) in enumerate(zip(pcols, _PRICING_PLANS)):
    with col:
        margin = "margin-top:-1rem;" if featured else ""
        border = 'class="glass-card gold-border"' if featured else 'class="glass-card"'
        st.markdown(f'<div {border} style="text-align:center;{margin}position:relative;">', unsafe_allow_html=True)
        if featured:
            st.markdown(f'<div class="gold-badge" style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);padding:0.3rem 1.5rem;border-radius:20px;font-size:0.85rem;font-weight:700;white-space:nowrap;">{"الأكثر طلباً" if LANG == "ar" else "Most Popular"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom:0.5rem;color:var(--text-light);">{_PRICING_ICONS[key]}</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="font-size:1.4rem;font-weight:700;margin-bottom:0.5rem;">{name}</h3>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:2.5rem;font-weight:800;margin:1rem 0;">{price}<span style="font-size:0.9rem;opacity:0.6;">/{"شهر" if LANG == "ar" else "mo"}</span></div>', unsafe_allow_html=True)
        for f in feats:
            st.markdown(f'<p style="margin:0.5rem 0;display:flex;align-items:center;justify-content:center;gap:0.5rem;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="20 6 9 17 4 12"/></svg> {f}</p>', unsafe_allow_html=True)
        btn = "ابدأ مجاناً" if LANG == "ar" else "Start Free"
        if name not in ("مجاني" if LANG == "ar" else "Free",):
            btn = f"اشترك {price}/شهر" if LANG == "ar" else f"Subscribe {price}/mo"
        st.markdown(f'<a href="?page=app" style="display:block;text-align:center;padding:var(--btn-padding);margin-top:1.5rem;border-radius:var(--btn-radius);background:var(--primary);color:#ffffff!important;font-weight:600;text-decoration:none!important;">{btn}</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# ── Testimonials section ──────────────────────────────────────────────────────
testimonials_title = "💬 ماذا يقول المستخدمون؟" if LANG == "ar" else "💬 What Our Users Say"
st.markdown(f'<h2 style="text-align:center;font-size:2rem;font-weight:800;margin-bottom:3rem;">{testimonials_title}</h2>', unsafe_allow_html=True)

tcols = st.columns(3)
testimonials = [
    ("🧑‍💻", "أحمد السالم", "مطور برمجيات" if LANG == "ar" else "Software Developer",
     "أداة رائعة! وفرت علي ساعات طويلة من إعادة صياغة المحتوى. أدعمها بشدة." if LANG == "ar"
     else "Amazing tool! Saved me hours of content reformatting. Highly recommend."),
    ("👩‍💼", "سارة العتيبي", "مسوقة رقمية" if LANG == "ar" else "Digital Marketer",
     "أسعار مناسبة جداً وجودة ممتازة. أحببت دعم اللهجات العربية المختلفة." if LANG == "ar"
     else "Very affordable pricing with excellent quality. Love the Arabic dialect support."),
    ("👨‍🏫", "خالد الحربي", "صانع محتوى" if LANG == "ar" else "Content Creator",
     "أنتج محتوى لخمس منصات في دقائق. صار عندي وقت إضافي للتركيز على الإبداع." if LANG == "ar"
     else "Content for 5 platforms in minutes. I now have extra time to focus on creativity."),
]
for col, (icon, name, role, quote) in zip(tcols, testimonials):
    with col:
        st.markdown(f'<div class="glass-card" style="text-align:center;">'
            f'<div class="avatar-circle">{icon}</div>'
            f'<h4 style="font-weight:700;margin-bottom:0.25rem;">{name}</h4>'
            f'<p style="opacity:0.5;font-size:0.85rem;margin-bottom:1rem;">{role}</p>'
            f'<p style="opacity:0.8;line-height:1.7;font-style:italic;">"{quote}"</p>'
            f'</div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown(f'''
<div style="text-align:center;padding:3rem 1rem;border-top:1px solid rgba(255,255,255,0.1);">
    <div style="margin-bottom:1rem;font-weight:700;font-size:1.2rem;">🚀 ContentMultiplier AI</div>
    <div style="margin-bottom:1rem;opacity:0.7;">{"ضاعف محتواك لمنصات التواصل" if LANG == "ar" else "Multiply your content across social platforms"}</div>
    <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:1rem;">
        <a href="?page=privacy" target="_self">{"سياسة الخصوصية" if LANG == "ar" else "Privacy Policy"}</a>
        <a href="?page=privacy" target="_self">{"الشروط والأحكام" if LANG == "ar" else "Terms & Conditions"}</a>
        <a href="mailto:hello@contentmultiplier.app">{"تواصل معنا" if LANG == "ar" else "Contact Us"}</a>
    </div>
    <div style="opacity:0.4;font-size:0.8rem;margin-top:0.5rem;">
        © 2026 ContentMultiplier AI. {"جميع الحقوق محفوظة." if LANG == "ar" else "All rights reserved."}
    </div>
</div>
''', unsafe_allow_html=True)
