import streamlit as st
from frontend.fonts import FONT_CSS
from frontend.style import inject_custom_css

st.set_page_config(
    page_title="ContentMultiplier AI - ضاعف محتواك",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LANG = st.session_state.get("lang", "ar")
DIR = "rtl" if LANG == "ar" else "ltr"

page_param = st.query_params.get("page")
if page_param == "app":
    st.switch_page("pages/01_📱_App.py")
elif page_param == "privacy":
    st.switch_page("pages/02_🔒_Privacy_Policy.py")

st.markdown(FONT_CSS, unsafe_allow_html=True)
inject_custom_css()

def switch_lang():
    st.session_state["lang"] = "en" if LANG == "ar" else "ar"
    st.rerun()

hero_anim = """
<style>
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 4px 30px rgba(37, 99, 235, 0.3); }
        50% { box-shadow: 0 4px 50px rgba(37, 99, 235, 0.6); }
    }
    .hero-section { text-align: center; padding: 6rem 1rem 4rem; animation: fadeSlideUp 0.8s ease-out; }
    .hero-section h1 { animation: fadeSlideUp 0.8s ease-out 0.1s both; }
    .hero-section p { animation: fadeSlideUp 0.8s ease-out 0.2s both; }
    .hero-section .hero-actions { animation: fadeSlideUp 0.8s ease-out 0.3s both; }
    .hero-section .hero-stats { animation: fadeSlideUp 0.8s ease-out 0.4s both; }
    .btn-pulse {
        display: inline-block; padding: 1.2rem 3.5rem;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        color: #fff !important; font-size: 1.3rem; font-weight: 800;
        border-radius: 60px; text-decoration: none !important;
        animation: pulse 2s infinite;
        transition: transform 0.2s;
    }
    .btn-pulse:hover { transform: translateY(-3px); }
    .feature-enter { animation: fadeSlideUp 0.6s ease-out both; }
    .feature-enter:nth-child(1) { animation-delay: 0.1s; }
    .feature-enter:nth-child(2) { animation-delay: 0.2s; }
    .feature-enter:nth-child(3) { animation-delay: 0.3s; }
    .section-spacer { height: 5rem; }
    .gold-border { border: 2px solid #F59E0B !important; }
    .gold-badge { background: linear-gradient(135deg, #F59E0B, #FCD34D); color: #0F172A !important; }
    .avatar-circle {
        width: 64px; height: 64px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem; margin: 0 auto 1rem;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
    }
</style>
"""
st.markdown(hero_anim, unsafe_allow_html=True)

col1, _, col2 = st.columns([1, 8, 1])
with col2:
    st.button("🌐 " + ("English" if LANG == "ar" else "العربية"), on_click=switch_lang, use_container_width=True)

st.markdown('<div class="hero-section">', unsafe_allow_html=True)

hero_title = ("🚀 ضاعف محتواك لمنصات التواصل<br>في دقائق بالذكاء الاصطناعي" if LANG == "ar"
              else "🚀 Multiply Your Content Across<br>Social Platforms in Minutes")
hero_desc = ("حوّل مقالاً واحداً إلى منشورات مخصصة وجاهزة للنشر على تويتر، لينكدإن، فيسبوك، انستغرام، وتيك توك" if LANG == "ar"
             else "Convert one article into platform-optimized posts for Twitter, LinkedIn, Facebook, Instagram & TikTok")

st.markdown(f'<h1 class="main-header" style="font-size:3rem;">{hero_title}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header" style="font-size:1.2rem;max-width:650px;margin:0 auto 2rem;">{hero_desc}</p>', unsafe_allow_html=True)

cta_main = "ابدأ الآن مجاناً" if LANG == "ar" else "Start Free"
cta_login = "تسجيل الدخول" if LANG == "ar" else "Login"
st.markdown(f'<div class="hero-actions">'
    f'<a href="?page=app" class="btn-pulse">{cta_main} ✨</a>&nbsp;&nbsp;'
    f'<a href="?page=app" class="glass-card" style="display:inline-block;padding:1rem 2.5rem;border-radius:60px;text-decoration:none!important;color:#fff!important;font-weight:700;">{cta_login} 🔐</a>'
    f'</div>', unsafe_allow_html=True)

stats_ar = [("📝", "٥٠+", "قالب"), ("🌍", "5", "منصات"), ("🆓", "7", "أيام تجربة")]
stats_en = [("📝", "50+", "Templates"), ("🌍", "5", "Platforms"), ("🆓", "7", "Days Free Trial")]
stats = stats_ar if LANG == "ar" else stats_en
stats_html = '<div class="hero-stats" style="display:flex;justify-content:center;gap:3rem;flex-wrap:wrap;margin-top:2.5rem;">'
for icon, num, label in stats:
    stats_html += f'<div style="text-align:center;"><div style="font-size:2rem;">{icon}</div><div style="font-size:1.5rem;font-weight:800;">{num}</div><div style="opacity:0.7;">{label}</div></div>'
stats_html += '</div>'
st.markdown(stats_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

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

pricing_title = "💰 خطط الأسعار" if LANG == "ar" else "💰 Pricing Plans"
st.markdown(f'<h2 style="text-align:center;font-size:2rem;font-weight:800;margin-bottom:3rem;">{pricing_title}</h2>', unsafe_allow_html=True)

plans = [
    ("🆓", "مجاني" if LANG == "ar" else "Free", "$0",
     ["5 توليدات/يوم" if LANG == "ar" else "5 generations/day",
      "منصات أساسية" if LANG == "ar" else "Basic platforms",
      "نبرة قياسية" if LANG == "ar" else "Standard tone"], False),
    ("⭐", "أساسي" if LANG == "ar" else "Basic", "$9",
     ["30 توليدة/يوم" if LANG == "ar" else "30 generations/day",
      "جميع المنصات" if LANG == "ar" else "All platforms",
      "جميع النبرات" if LANG == "ar" else "All tones",
      "تصدير PDF" if LANG == "ar" else "PDF export"], True),
    ("🚀", "احترافي" if LANG == "ar" else "Pro", "$29",
     ["100 توليدة/يوم" if LANG == "ar" else "100 generations/day",
      "جميع المنصات" if LANG == "ar" else "All platforms",
      "جميع النبرات + لهجات" if LANG == "ar" else "All tones + dialects",
      "تصدير PDF" if LANG == "ar" else "PDF export",
      "دعم أولوية" if LANG == "ar" else "Priority support"], False),
]

pcols = st.columns(3)
for i, (col, (icon, name, price, feats, featured)) in enumerate(zip(pcols, plans)):
    with col:
        margin = "margin-top:-1rem;" if featured else ""
        border = 'class="glass-card gold-border"' if featured else 'class="glass-card"'
        st.markdown(f'<div {border} style="text-align:center;{margin}position:relative;">', unsafe_allow_html=True)
        if featured:
            st.markdown(f'<div class="gold-badge" style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);padding:0.3rem 1.5rem;border-radius:20px;font-size:0.85rem;font-weight:700;white-space:nowrap;">{"الأكثر طلباً" if LANG == "ar" else "Most Popular"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:2.5rem;margin-bottom:0.5rem;">{icon}</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="font-size:1.4rem;font-weight:700;margin-bottom:0.5rem;">{name}</h3>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:2.5rem;font-weight:800;margin:1rem 0;"><span style="font-size:0.9rem;opacity:0.6;">{"شهر/" if LANG == "ar" else "/mo"}</span></div>'.replace('<span style=','<span style="font-size:1rem;opacity:0.6;" >' if LANG == "ar" else '<span style="font-size:1rem;opacity:0.6;" >', 1), unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:2.5rem;font-weight:800;margin:1rem 0;">{price}<span style="font-size:0.9rem;opacity:0.6;">/{"شهر" if LANG == "ar" else "mo"}</span></div>', unsafe_allow_html=True)
        for f in feats:
            st.markdown(f'<p style="margin:0.5rem 0;">✅ {f}</p>', unsafe_allow_html=True)
        btn = "ابدأ مجاناً" if LANG == "ar" else "Start Free"
        if name not in ("مجاني" if LANG == "ar" else "Free",):
            btn = f"اشترك {price}/شهر" if LANG == "ar" else f"Subscribe {price}/mo"
        st.markdown(f'<a href="?page=app" style="display:block;text-align:center;padding:0.9rem;margin-top:1.5rem;border-radius:14px;background:linear-gradient(135deg,#2563EB,#7C3AED);color:#fff!important;font-weight:700;text-decoration:none!important;">{btn}</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

testi_title = "💬 ماذا يقول مستخدمونا" if LANG == "ar" else "💬 What Our Users Say"
st.markdown(f'<h2 style="text-align:center;font-size:2rem;font-weight:800;margin-bottom:3rem;">{testi_title}</h2>', unsafe_allow_html=True)

testimonials = [
    ("👩‍💼", "سارة أحمد" if LANG == "ar" else "Sara Ahmed", "مديرة تسويق رقمي" if LANG == "ar" else "Digital Marketing Manager",
     "كانت إعادة صياغة المحتوى تأخذ مني 3 ساعات يومياً. الآن أصبحت دقيقة واحدة. أداة رائعة!" if LANG == "ar"
     else "Content repurposing used to take me 3 hours daily. Now it takes 1 minute. Amazing tool!"),
    ("👨‍💻", "فيصل العتيبي" if LANG == "ar" else "Faisal Al-Otaibi", "صانع محتوى" if LANG == "ar" else "Content Creator",
     "دعم اللهجة السعودية شيء خرافي! أخيراً أداة تفهم السوق العربي وتعرف تكتب زي الناس." if LANG == "ar"
     else "Saudi dialect support is incredible! Finally a tool that understands the Arab market."),
    ("👨‍💼", "محمد الغامدي" if LANG == "ar" else "Mohammed Al-Ghamdi", "مستشار تسويق" if LANG == "ar" else "Marketing Consultant",
     "أوفر 5 ساعات أسبوعياً وأنشر على 5 منصات في نفس الوقت. أفضل استثمار لأداة تسويقية." if LANG == "ar"
     else "I save 5 hours weekly and post to 5 platforms simultaneously. Best marketing investment."),
]

tcols = st.columns(3)
for col, (avatar, name, role, text) in zip(tcols, testimonials):
    with col:
        st.markdown(f'<div class="glass-card" style="text-align:center;">'
            f'<div class="avatar-circle">{avatar}</div>'
            f'<p style="font-style:italic;opacity:0.85;line-height:1.7;margin-bottom:1.5rem;">"{text}"</p>'
            f'<div style="font-weight:700;font-size:1.1rem;">{name}</div>'
            f'<div style="opacity:0.6;font-size:0.9rem;">{role}</div>'
            f'</div>', unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

st.markdown(f'''
<div style="text-align:center;padding:3rem 1rem;border-top:1px solid rgba(255,255,255,0.1);">
    <div style="margin-bottom:1rem;font-weight:700;font-size:1.2rem;">🚀 ContentMultiplier AI</div>
    <div style="margin-bottom:1rem;opacity:0.7;">{"ضاعف محتواك لمنصات التواصل" if LANG == "ar" else "Multiply your content across social platforms"}</div>
    <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:1rem;">
        <a href="?page=privacy" target="_self">{"سياسة الخصوصية" if LANG == "ar" else "Privacy Policy"}</a>
        <a href="?page=privacy" target="_self">{"الشروط والأحكام" if LANG == "ar" else "Terms & Conditions"}</a>
        <a href="mailto:hello@contentmultiplier.app">{"تواصل معنا" if LANG == "ar" else "Contact Us"}</a>
    </div>
    <div style="opacity:0.5;font-size:0.85rem;">
        {"بُنِيَ باستخدام" if LANG == "ar" else "Built with"} ❤️
        <a href="https://opencode.ai" target="_blank" style="opacity:0.8!important;">OpenCode</a> + DeepSeek AI
    </div>
    <div style="opacity:0.4;font-size:0.8rem;margin-top:0.5rem;">
        © 2026 ContentMultiplier AI. {"جميع الحقوق محفوظة." if LANG == "ar" else "All rights reserved."}
    </div>
</div>
''', unsafe_allow_html=True)
