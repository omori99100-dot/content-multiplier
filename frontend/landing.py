import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8501")

st.set_page_config(
    page_title="ContentMultiplier AI - ضاعف محتواك",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap');
    * { font-family: 'Tajawal', sans-serif !important; }
    .hero { text-align: center; padding: 5rem 1rem 3rem; background: linear-gradient(135deg, #0a1628, #1a3a6a); color: white; border-radius: 0 0 40px 40px; margin: -5rem -1rem 2rem; }
    .hero h1 { font-size: 3rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.3; }
    .hero p { font-size: 1.2rem; opacity: 0.85; max-width: 600px; margin: 0 auto 2rem; }
    .hero .btn-primary { display: inline-block; padding: 1rem 3rem; background: #00d4aa; color: #0a1628; font-size: 1.2rem; font-weight: 700; border-radius: 50px; text-decoration: none; transition: 0.3s; }
    .hero .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,212,170,0.4); }
    .section-title { text-align: center; font-size: 2rem; font-weight: 700; margin: 4rem 0 2rem; }
    .feature-card { background: white; border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06); height: 100%; }
    .feature-card .icon { font-size: 3rem; margin-bottom: 1rem; }
    .feature-card h3 { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; }
    .feature-card p { color: #666; font-size: 0.95rem; line-height: 1.6; }
    .pricing-card { background: white; border-radius: 20px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06); height: 100%; border: 2px solid transparent; position: relative; }
    .pricing-card.featured { border-color: #00d4aa; }
    .pricing-card .price { font-size: 2.5rem; font-weight: 800; color: #1a3a6a; margin: 1rem 0; }
    .pricing-card .price span { font-size: 1rem; color: #666; }
    .pricing-card ul { list-style: none; padding: 0; margin: 1rem 0 2rem; text-align: right; }
    .pricing-card ul li { padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; }
    .pricing-card .btn-plan { display: inline-block; padding: 0.8rem 2rem; background: #1a3a6a; color: white; border-radius: 50px; text-decoration: none; font-weight: 700; width: 100%; }
    .pricing-card .btn-plan:hover { background: #0a1628; }
    .testimonial-card { background: #f8f9fa; border-radius: 16px; padding: 2rem; text-align: center; height: 100%; }
    .testimonial-card .avatar { font-size: 3rem; margin-bottom: 0.5rem; }
    .testimonial-card .text { font-style: italic; color: #555; line-height: 1.6; margin-bottom: 1rem; }
    .testimonial-card .name { font-weight: 700; color: #1a3a6a; }
    .footer { text-align: center; padding: 3rem 1rem; margin-top: 4rem; border-top: 1px solid #eee; color: #888; }
    .footer a { color: #1a3a6a; text-decoration: none; margin: 0 1rem; }
    .badge { display: inline-block; background: #00d4aa; color: #0a1628; padding: 0.25rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; margin-bottom: 0.5rem; }
    .rtl { direction: rtl; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🚀 ضاعف محتواك لمنصات التواصل<br>في دقائق بالذكاء الاصطناعي</h1>
    <p>حوّل مقالاً واحداً إلى منشورات مخصصة وجاهزة للنشر على تويتر، لينكدإن، فيسبوك، انستغرام، وتيك توك<br>بدون عناء إعادة الصياغة اليدوية</p>
    <a href="/" class="btn-primary">✨ ابدأ الآن مجاناً</a>
    <br><br>
    <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; margin-top:2rem;">
        <div>📝 <strong>50+</strong> قالب منشور</div>
        <div>🌍 <strong>5</strong> منصات تواصل</div>
        <div>🆓 <strong>7</strong> أيام تجربة مجانية</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">✨ لماذا ContentMultiplier؟</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">⏱️</div>
        <h3>وفر 5 ساعات أسبوعياً</h3>
        <p>بدلاً من إعادة صياغة كل مقال يدوياً لكل منصة، دع الذكاء الاصطناعي يقوم بالمهمة في ثوانٍ.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🎯</div>
        <h3>منشورات محسّنة لكل منصة</h3>
        <p>كل منصة لها طابعها: تويتر للتغريدات القصيرة، لينكدإن للمحتوى المهني، تيك توك للفيديوهات الجذابة.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🌐</div>
        <h3>دعم عربي كامل + لهجات</h3>
        <p>أول أداة تدعم اللهجات السعودية والمصرية بجانب الفصحى، مع هاشتاغات ومحتوى عربي أصيل.</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">📧</div>
        <h3>توصيل لبريدك تلقائياً</h3>
        <p>ضع الرابط وامشِ. النتائج تصلك على إيميلك جاهزة مع صور مقترحة.</p>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🖼️</div>
        <h3>صور مقترحة لكل منشور</h3>
        <p>نقترح صورة مناسبة لكل منشور باستخدام Unsplash، لتجعل محتواك بصرياً وجذاباً.</p>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">💾</div>
        <h3>تصدير PDF بنقرة</h3>
        <p>حمّل كل المنشورات كملف PDF جاهز للنشر أو العرض على عميلك.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">💰 خطط الأسعار</div>', unsafe_allow_html=True)
pcol1, pcol2, pcol3 = st.columns(3)

with pcol1:
    st.markdown("""
    <div class="pricing-card">
        <div class="badge">🆓 مجاني</div>
        <h3>تجريبي</h3>
        <div class="price">$0<span>/شهر</span></div>
        <ul>
            <li>✅ 5 توليدات/يوم</li>
            <li>✅ منصات أساسية</li>
            <li>✅ نبرة قياسية</li>
            <li>❌ تصدير PDF</li>
            <li>❌ صور مقترحة</li>
        </ul>
        <a href="/" class="btn-plan">ابدأ مجاناً</a>
    </div>
    """, unsafe_allow_html=True)

with pcol2:
    st.markdown("""
    <div class="pricing-card featured">
        <div class="badge">⭐ الأكثر طلباً</div>
        <h3>أساسي</h3>
        <div class="price">$9<span>/شهر</span></div>
        <ul>
            <li>✅ 30 توليدة/يوم</li>
            <li>✅ جميع المنصات</li>
            <li>✅ جميع النبرات</li>
            <li>✅ تصدير PDF</li>
            <li>✅ صور مقترحة</li>
        </ul>
        <a href="/?checkout=basic" class="btn-plan" style="background:#00d4aa;color:#0a1628;">اشترك $9/شهر</a>
    </div>
    """, unsafe_allow_html=True)

with pcol3:
    st.markdown("""
    <div class="pricing-card">
        <div class="badge">🚀 احترافي</div>
        <h3>احترافي</h3>
        <div class="price">$29<span>/شهر</span></div>
        <ul>
            <li>✅ 100 توليدة/يوم</li>
            <li>✅ جميع المنصات</li>
            <li>✅ جميع النبرات + لهجات</li>
            <li>✅ تصدير PDF</li>
            <li>✅ صور مقترحة</li>
            <li>✅ دعم أولوية</li>
        </ul>
        <a href="/?checkout=pro" class="btn-plan">اشترك $29/شهر</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div style="margin-bottom:1rem;">
        <strong>🚀 ContentMultiplier AI</strong> — ضاعف محتواك لمنصات التواصل
    </div>
    <div>
        <a href="/privacy" target="_self">سياسة الخصوصية</a>
        <a href="/privacy" target="_self">الشروط والأحكام</a>
        <a href="mailto:hello@contentmultiplier.app">تواصل معنا</a>
    </div>
    <div style="margin-top:0.5rem;">
        <a href="https://github.com/yourusername/content-multiplier" target="_blank">GitHub</a>
        <a href="https://twitter.com/contentmultiplier" target="_blank">تويتر</a>
    </div>
    <div style="margin-top:1rem;font-size:0.85rem;">
        © 2026 ContentMultiplier AI. جميع الحقوق محفوظة.
    </div>
</div>
""", unsafe_allow_html=True)
