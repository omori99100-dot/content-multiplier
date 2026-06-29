import streamlit as st
import os

st.set_page_config(
    page_title="ContentMultiplier AI - ضاعف محتواك",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LANG = st.session_state.get("lang", "ar")
DIR = "rtl" if LANG == "ar" else "ltr"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap');
    * {{ font-family: 'Tajawal', sans-serif !important; }}
    .hero {{ text-align: center; padding: 5rem 1rem 3rem; background: linear-gradient(135deg, #0a1628, #1a3a6a); color: white; border-radius: 0 0 40px 40px; margin: -5rem -1rem 2rem; }}
    .hero h1 {{ font-size: 2.8rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.3; }}
    .hero p {{ font-size: 1.2rem; opacity: 0.85; max-width: 600px; margin: 0 auto 2rem; }}
    .btn-primary {{ display: inline-block; padding: 1rem 3rem; background: #00d4aa; color: #0a1628; font-size: 1.2rem; font-weight: 700; border-radius: 50px; text-decoration: none; transition: 0.3s; margin: 0.5rem; }}
    .btn-secondary {{ display: inline-block; padding: 1rem 3rem; background: rgba(255,255,255,0.15); color: white; font-size: 1.2rem; font-weight: 700; border-radius: 50px; text-decoration: none; transition: 0.3s; margin: 0.5rem; border: 2px solid rgba(255,255,255,0.3); }}
    .section-title {{ text-align: center; font-size: 2rem; font-weight: 700; margin: 4rem 0 2rem; direction: {DIR}; }}
    .feature-card {{ background: white; border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06); height: 100%; direction: {DIR}; }}
    .feature-card .icon {{ font-size: 3rem; margin-bottom: 1rem; }}
    .feature-card h3 {{ font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; }}
    .feature-card p {{ color: #666; font-size: 0.95rem; line-height: 1.6; }}
    .pricing-card {{ background: white; border-radius: 20px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06); height: 100%; border: 2px solid transparent; direction: {DIR}; }}
    .pricing-card.featured {{ border-color: #00d4aa; }}
    .pricing-card .price {{ font-size: 2.5rem; font-weight: 800; color: #1a3a6a; margin: 1rem 0; }}
    .pricing-card .price span {{ font-size: 1rem; color: #666; }}
    .pricing-card ul {{ list-style: none; padding: 0; margin: 1rem 0 2rem; }}
    .pricing-card ul li {{ padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; }}
    .testimonial-card {{ background: #f8f9fa; border-radius: 16px; padding: 2rem; text-align: center; height: 100%; direction: {DIR}; }}
    .testimonial-card .avatar {{ font-size: 3rem; margin-bottom: 0.5rem; }}
    .testimonial-card .text {{ font-style: italic; color: #555; line-height: 1.6; margin-bottom: 1rem; }}
    .testimonial-card .name {{ font-weight: 700; color: #1a3a6a; }}
    .footer {{ text-align: center; padding: 3rem 1rem; margin-top: 4rem; border-top: 1px solid #eee; color: #888; direction: {DIR}; }}
    .footer a {{ color: #1a3a6a; text-decoration: none; margin: 0 1rem; }}
    .badge {{ display: inline-block; background: #00d4aa; color: #0a1628; padding: 0.25rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; margin-bottom: 0.5rem; }}
    .lang-btn {{ position: fixed; top: 1rem; {('left' if DIR == 'rtl' else 'right')}: 1rem; z-index: 999; background: white; border: 1px solid #ddd; border-radius: 50px; padding: 0.5rem 1rem; cursor: pointer; font-size: 0.9rem; }}
</style>
""", unsafe_allow_html=True)

def switch_lang():
    st.session_state["lang"] = "en" if LANG == "ar" else "ar"
    st.rerun()

col1, _, col2 = st.columns([1, 8, 1])
with col2:
    st.button("🌐 " + ("English" if LANG == "ar" else "العربية"), on_click=switch_lang)

APP_URL = "http://localhost:8501"

hero_title_ar = "🚀 ضاعف محتواك لمنصات التواصل<br>في دقائق بالذكاء الاصطناعي"
hero_title_en = "🚀 Multiply Your Content Across<br>Social Platforms in Minutes"

hero_desc_ar = "حوّل مقالاً واحداً إلى منشورات مخصصة وجاهزة للنشر على تويتر، لينكدإن، فيسبوك، انستغرام، وتيك توك"
hero_desc_en = "Convert one article into platform-optimized posts for Twitter, LinkedIn, Facebook, Instagram & TikTok"

hero_title = hero_title_ar if LANG == "ar" else hero_title_en
hero_desc = hero_desc_ar if LANG == "ar" else hero_desc_en

cta_main = "ابدأ الآن مجاناً" if LANG == "ar" else "Start Free"
cta_login = "تسجيل الدخول" if LANG == "ar" else "Login"
cta_app = "لوحة التحكم" if LANG == "ar" else "Dashboard"

st.markdown(f"""
<div class="hero">
    <h1>{hero_title}</h1>
    <p>{hero_desc}</p>
    <div>
        <a href="{APP_URL}" class="btn-primary">{cta_main} ✨</a>
        <a href="{APP_URL}" class="btn-secondary">{cta_login} 🔐</a>
    </div>
    <br>
    <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; margin-top:2rem;">
        <div>📝 <strong>{'50+' if LANG == 'en' else '٥٠+'}</strong> {'Templates' if LANG == 'en' else 'قالب'}</div>
        <div>🌍 <strong>{'5'}</strong> {'Platforms' if LANG == 'en' else 'منصات'}</div>
        <div>🆓 <strong>{'7'}</strong> {'Days Free Trial' if LANG == 'en' else 'أيام تجربة'}</div>
    </div>
</div>
""", unsafe_allow_html=True)

features = [
    ("⏱️", ("Save 5 Hours/Week", "وفر 5 ساعات أسبوعياً"), ("Let AI rewrite your content for each platform in seconds.", "دع الذكاء الاصطناعي يعيد صياغة محتواك لكل منصة في ثوانٍ.")),
    ("🎯", ("Platform-Optimized Posts", "منشورات محسّنة لكل منصة"), ("Each platform gets its own style: short tweets, professional LinkedIn, engaging TikTok.", "كل منصة لها طابعها: تويتر للتغريدات، لينكدإن للمحتوى المهني.")),
    ("🌐", ("Full Arabic + Dialects", "دعم عربي كامل + لهجات"), ("First tool supporting Saudi & Egyptian dialects alongside formal Arabic.", "أول أداة تدعم اللهجات السعودية والمصرية بجانب الفصحى.")),
    ("📧", ("Auto Email Delivery", "توصيل لبريدك تلقائياً"), ("Enter a URL and walk away. Results arrive in your inbox with images.", "ضع الرابط وامشِ. النتائج تصلك على إيميلك مع صور.")),
    ("🖼️", ("Suggested Images", "صور مقترحة"), ("Auto-generated image suggestions from Unsplash for each post.", "نقترح صورة مناسبة لكل منشور تلقائياً.")),
    ("💾", ("PDF Export", "تصدير PDF"), ("Download all posts as a professional PDF ready to present.", "حمّل كل المنشورات كملف PDF جاهز.")),
]

st.markdown(f'<div class="section-title">✨ {"Why ContentMultiplier?" if LANG == "en" else "لماذا مضاعف المحتوى؟"}</div>', unsafe_allow_html=True)
for i in range(0, 6, 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(features):
            icon, (en_title, ar_title), (en_desc, ar_desc) = features[idx]
            title = ar_title if LANG == "ar" else en_title
            desc = ar_desc if LANG == "ar" else en_desc
            with col:
                st.markdown(f'<div class="feature-card"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

pricing_title = "💰 خطط الأسعار" if LANG == "ar" else "💰 Pricing Plans"
st.markdown(f'<div class="section-title">{pricing_title}</div>', unsafe_allow_html=True)

pcol1, pcol2, pcol3 = st.columns(3)
plans_data = [
    ("🆓", "مجاني" if LANG == "ar" else "Free", "FREE" if LANG == "en" else "مجاني", "$0", ["5 توليدات/يوم" if LANG == "ar" else "5 generations/day", "منصات أساسية" if LANG == "ar" else "Basic platforms", "نبرة قياسية" if LANG == "ar" else "Standard tone"]),
    ("⭐", "أساسي" if LANG == "ar" else "Basic", "POPULAR" if LANG == "en" else "الأكثر طلباً", "$9", ["30 توليدة/يوم" if LANG == "ar" else "30 generations/day", "جميع المنصات" if LANG == "ar" else "All platforms", "جميع النبرات" if LANG == "ar" else "All tones", "تصدير PDF" if LANG == "ar" else "PDF export"]),
    ("🚀", "احترافي" if LANG == "ar" else "Pro", "PRO" if LANG == "en" else "احترافي", "$29", ["100 توليدة/يوم" if LANG == "ar" else "100 generations/day", "جميع المنصات" if LANG == "ar" else "All platforms", "جميع النبرات + لهجات" if LANG == "ar" else "All tones + dialects", "تصدير PDF" if LANG == "ar" else "PDF export", "دعم أولوية" if LANG == "ar" else "Priority support"]),
]

for col, (icon, name, badge, price, features_list) in zip([pcol1, pcol2, pcol3], plans_data):
    with col:
        featured = badge in ("POPULAR", "الأكثر طلباً")
        featured_class = " featured" if featured else ""
        st.markdown(f'<div class="pricing-card{featured_class}">', unsafe_allow_html=True)
        if badge:
            st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
        st.markdown(f"<h3>{icon} {name}</h3>", unsafe_allow_html=True)
        st.markdown(f'<div class="price">{price}<span>/{"شهر" if LANG == "ar" else "mo"}</span></div>', unsafe_allow_html=True)
        st.markdown("<ul>" + "".join(f"<li>✅ {f}</li>" for f in features_list) + "</ul>", unsafe_allow_html=True)
        btn_text = "ابدأ مجاناً" if LANG == "ar" else "Start Free"
        if name not in ("مجاني" if LANG == "ar" else "Free",):
            btn_text = f"اشترك {price}/شهر" if LANG == "ar" else f"Subscribe {price}/mo"
        st.markdown(f'<a href="{APP_URL}" class="btn-primary" style="display:block;text-align:center;">{btn_text}</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

testimonials_title = "💬 ماذا يقول مستخدمونا" if LANG == "ar" else "💬 What Our Users Say"
st.markdown(f'<div class="section-title">{testimonials_title}</div>', unsafe_allow_html=True)

tcol1, tcol2, tcol3 = st.columns(3)
testimonials = [
    ("👩‍💼", "سارة أحمد" if LANG == "ar" else "Sara Ahmed", "مديرة تسويق رقمي" if LANG == "ar" else "Digital Marketing Manager",
     '"كانت إعادة صياغة المحتوى تأخذ مني 3 ساعات يومياً. الآن أصبحت دقيقة واحدة. أداة رائعة!"' if LANG == "ar" else '"Content repurposing used to take me 3 hours daily. Now it takes 1 minute. Amazing tool!"'),
    ("👨‍💻", "فيصل العتيبي" if LANG == "ar" else "Faisal Al-Otaibi", "صانع محتوى" if LANG == "ar" else "Content Creator",
     '"دعم اللهجة السعودية شيء خرافي! أخيراً أداة تفهم السوق العربي."' if LANG == "ar" else '"Saudi dialect support is incredible! Finally a tool that understands the Arab market."'),
    ("👨‍💼", "محمد الغامدي" if LANG == "ar" else "Mohammed Al-Ghamdi", "مستشار تسويق" if LANG == "ar" else "Marketing Consultant",
     '"أوفر 5 ساعات أسبوعياً وأنشر على 5 منصات في نفس الوقت. أفضل استثمار."' if LANG == "ar" else '"I save 5 hours weekly and post to 5 platforms simultaneously. Best investment."'),
]

for col, (avatar, name, role, text) in zip([tcol1, tcol2, tcol3], testimonials):
    with col:
        st.markdown(f'<div class="testimonial-card"><div class="avatar">{avatar}</div><div class="text">{text}</div><div class="name">{name}</div><div style="color:#888;font-size:0.85rem;">{role}</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <div style="margin-bottom:1rem;">
        <strong>🚀 ContentMultiplier AI</strong> — {"ضاعف محتواك لمنصات التواصل" if LANG == "ar" else "Multiply your content across social platforms"}
    </div>
    <div>
        <a href="/privacy" target="_self">{"سياسة الخصوصية" if LANG == "ar" else "Privacy Policy"}</a>
        <a href="/privacy" target="_self">{"الشروط والأحكام" if LANG == "ar" else "Terms"}</a>
        <a href="mailto:hello@contentmultiplier.app">{"تواصل معنا" if LANG == "ar" else "Contact"}</a>
    </div>
    <div style="margin-top:0.5rem;">
        <a href="https://github.com/yourusername/content-multiplier" target="_blank">GitHub</a>
        <a href="https://twitter.com/contentmultiplier" target="_blank">{"تويتر" if LANG == "ar" else "Twitter"}</a>
    </div>
    <div style="margin-top:1rem;font-size:0.85rem;">
        {"بُنِيَ باستخدام" if LANG == "ar" else "Built with"} ❤️ <a href="https://opencode.ai" target="_blank">OpenCode</a> + DeepSeek AI
    </div>
    <div style="margin-top:0.5rem;font-size:0.85rem;">
        © 2026 ContentMultiplier AI. {"جميع الحقوق محفوظة." if LANG == "ar" else "All rights reserved."}
    </div>
</div>
""", unsafe_allow_html=True)
