import streamlit as st
from frontend.fonts import FONT_CSS

st.set_page_config(page_title="Privacy Policy | سياسة الخصوصية", page_icon="🔒", layout="centered", initial_sidebar_state="collapsed")

LANG = st.session_state.get("lang", "ar")
DIR = "rtl" if LANG == "ar" else "ltr"

st.markdown(FONT_CSS, unsafe_allow_html=True)
st.markdown(f"""
<style>
    * {{ font-family: 'ShorooqN1', sans-serif !important; }}
    .content {{ direction: {DIR}; text-align: {DIR}; max-width: 800px; margin: auto; padding: 2rem 1rem; line-height: 1.8; }}
    h1 {{ color: #1a3a6a; }}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🇸🇦 العربية"):
        st.session_state["lang"] = "ar"; st.rerun()
with col2:
    if st.button("🇬🇧 English"):
        st.session_state["lang"] = "en"; st.rerun()

if LANG == "ar":
    st.markdown(f"""
<div class="content">
    <h1>🔒 سياسة الخصوصية</h1>
    <p><em>آخر تحديث: 29 يونيو 2026</em></p>

    <h2>1. المقدمة</h2>
    <p>نحن في ContentMultiplier AI (يُشار إليها بـ "نحن" أو "الخدمة") نلتزم بحماية خصوصية مستخدمينا. توضح هذه السياسة كيفية جمع واستخدام وحماية معلوماتك.</p>

    <h2>2. المعلومات التي نجمعها</h2>
    <ul>
        <li><strong>معلومات الحساب:</strong> الاسم، البريد الإلكتروني، اسم المستخدم عند التسجيل.</li>
        <li><strong>محتوى المستخدم:</strong> روابط المقالات والنصوص التي ترسلها للتوليد.</li>
        <li><strong>معلومات الاستخدام:</strong> عدد التوليدات، المنصات المختارة، النبرات المستخدمة.</li>
        <li><strong>معلومات الدفع:</strong> تتم معالجة المدفوعات عبر Stripe ولا نخزن معلومات بطاقتك الائتمانية.</li>
    </ul>

    <h2>3. كيفية استخدام معلوماتك</h2>
    <ul>
        <li>لتقديم خدمة توليد المحتوى المطلوبة.</li>
        <li>لإرسال الإيميلات التي طلبتها (النتائج والإشعارات).</li>
        <li>لتحسين جودة التوليد بناءً على أنماط الاستخدام.</li>
        <li>لإرسال اتصالات دورية متعلقة بالخدمة (بموافقتك).</li>
    </ul>

    <h2>4. الذكاء الاصطناعي والمحتوى</h2>
    <p>يتم إرسال النصوص التي تقدمها إلى OpenAI API لتوليد المحتوى. لا نستخدم محتواك لتدريب نماذجنا الخاصة. راجع سياسة خصوصية OpenAI للمزيد.</p>

    <h2>5. تخزين البيانات وأمانها</h2>
    <p>نستخدم تشفير SSL/TLS لجميع الاتصالات. كلمات المرور مشفرة باستخدام bcrypt. نوصي باستخدام كلمة مرور قوية وفريدة.</p>

    <h2>6. الاحتفاظ بالبيانات</h2>
    <p>نحتفظ ببيانات حسابك طالما أن حسابك نشط. عند حذف حسابك، نحذف معلوماتك الشخصية خلال 30 يوماً.</p>

    <h2>7. حقوقك</h2>
    <ul>
        <li>حق الوصول إلى بياناتك الشخصية.</li>
        <li>حق تصحيح أو تحديث بياناتك.</li>
        <li>حق حذف حسابك وبياناتك.</li>
        <li>حق الاعتراض على معالجة بياناتك.</li>
    </ul>

    <h2>8. ملفات تعريف الارتباط (Cookies)</h2>
    <p>نستخدم ملفات تعريف ارتباط ضرورية للحفاظ على جلستك (تسجيل الدخول). لا نستخدم ملفات تتبع لأطراف ثالثة.</p>

    <h2>9. خدمات الطرف الثالث</h2>
    <ul>
        <li><strong>OpenAI:</strong> لتوليد المحتوى بالذكاء الاصطناعي.</li>
        <li><strong>Stripe:</strong> لمعالجة المدفوعات والاشتراكات.</li>
        <li><strong>SendGrid:</strong> لإرسال الإيميلات.</li>
        <li><strong>Unsplash:</strong> لجلب الصور المقترحة.</li>
    </ul>
    <p>هذه الخدمات لها سياسات خصوصية خاصة بها.</p>

    <h2>10. التغييرات على هذه السياسة</h2>
    <p>قد نقوم بتحديث هذه السياسة من وقت لآخر. سنخطرك بالتغييرات الجوهرية عبر البريد الإلكتروني.</p>

    <h2>11. اتصل بنا</h2>
    <p>للاستفسارات المتعلقة بالخصوصية: <a href="mailto:privacy@contentmultiplier.app">privacy@contentmultiplier.app</a></p>

    <hr>
    <p><a href="/" target="_self">← العودة للصفحة الرئيسية</a></p>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown(f"""
<div class="content">
    <h1>🔒 Privacy Policy</h1>
    <p><em>Last updated: June 29, 2026</em></p>

    <h2>1. Introduction</h2>
    <p>ContentMultiplier AI ("we", "our", "the Service") is committed to protecting your privacy. This policy explains how we collect, use, and protect your information.</p>

    <h2>2. Information We Collect</h2>
    <ul>
        <li><strong>Account information:</strong> Name, email, username upon registration.</li>
        <li><strong>User content:</strong> Article URLs and text you submit for generation.</li>
        <li><strong>Usage data:</strong> Generation count, selected platforms, tones used.</li>
        <li><strong>Payment data:</strong> Processed via Stripe; we never store credit card details.</li>
    </ul>

    <h2>3. How We Use Your Information</h2>
    <ul>
        <li>To provide the content generation service.</li>
        <li>To send requested emails (results and notifications).</li>
        <li>To improve generation quality based on usage patterns.</li>
        <li>To send service-related communications (with your consent).</li>
    </ul>

    <h2>4. AI and Content</h2>
    <p>Text you submit is sent to OpenAI API for content generation. We do not use your content to train our own models. See OpenAI's privacy policy for details.</p>

    <h2>5. Data Security</h2>
    <p>All communications use SSL/TLS encryption. Passwords are hashed using bcrypt. We recommend using a strong, unique password.</p>

    <h2>6. Data Retention</h2>
    <p>We retain your data while your account is active. Upon account deletion, personal data is removed within 30 days.</p>

    <h2>7. Your Rights</h2>
    <ul>
        <li>Right to access your personal data.</li>
        <li>Right to correct or update your data.</li>
        <li>Right to delete your account and data.</li>
        <li>Right to object to data processing.</li>
    </ul>

    <h2>8. Cookies</h2>
    <p>We use essential cookies for session management (login). We do not use third-party tracking cookies.</p>

    <h2>9. Third-Party Services</h2>
    <ul>
        <li><strong>OpenAI:</strong> AI content generation.</li>
        <li><strong>Stripe:</strong> Payment processing.</li>
        <li><strong>SendGrid:</strong> Email delivery.</li>
        <li><strong>Unsplash:</strong> Image suggestions.</li>
    </ul>
    <p>These services have their own privacy policies.</p>

    <h2>10. Policy Changes</h2>
    <p>We may update this policy periodically. Material changes will be notified via email.</p>

    <h2>11. Contact</h2>
    <p>Privacy inquiries: <a href="mailto:privacy@contentmultiplier.app">privacy@contentmultiplier.app</a></p>

    <hr>
    <p><a href="/" target="_self">← Back to Home</a></p>
</div>
""", unsafe_allow_html=True)
