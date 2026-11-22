import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="درع الحماية الذكي", page_icon="🛡️")
st.title("🛡️ درع الحماية الذكي (Antihacker AI)")

# --- 1. تدريب نموذج الذكاء الاصطناعي ---
@st.cache_resource
def train_model():
    def extract_url_features(url):
        url = str(url)
        return [len(url), url.count('.'), url.count('-'), 1 if '@' in url else 0, 1 if url.startswith('https') else 0]

    sample_urls = [
        "https://google.com", "https://youtube.com",
        "https://github.com", "https://amazon.ae",
        "https://apple.com", "https://microsoft.com",
        "http://update-bank-account-security-login.com@evil.com",
        "http://free-iphone-winner-claim-now-2026.xyz",
        "http://192.168.1",
        "http://secure-login-apple-id-verification-alert.com",
        "http://whatsapp-gold-download-free-apk@virus.net",
        "http://bit.ly"
    ]
    labels = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    X_train = np.array([extract_url_features(u) for u in sample_urls])
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, labels)
    return model, extract_url_features

ai_model, extract_url_features = train_model()

# --- 2. تقسيم الواجهة إلى 3 تبويبات ---
tab1, tab2, tab3 = st.tabs(["🧠 فحص الروابط (AI)", "🖼️ الصور والفيديو", "📄 فحص ملفات PDF"])

with tab1:
    link = st.text_input("ضع الرابط المشبوه هنا:", placeholder="https://example.com")
    if st.button("فحص الرابط"):
        if not link:
            st.warning("⚠️ الرجاء إدخال رابط أولاً.")
        else:
            features = np.array([extract_url_features(link)])
            prediction = ai_model.predict(features)[0]
            probability = ai_model.predict_proba(features)[0][1] * 100
            if prediction == 1:
                st.error(f"🚨 تحذير من الذكاء الاصطناعي! الرابط خبيث بنسبة خطورة: {probability:.1f}%")
            else:
                st.success(f"✅ الذكاء الاصطناعي يصنف الرابط كآمن (نسبة الشك: {probability:.1f}%)")

with tab2:
    media_file = st.file_uploader("ارفع صورة أو مقطع فيديو لفحص بصمته الرقمية")
    if media_file is not None:
        header = media_file.read(16).hex()
        if header.startswith("ffd8ff") or header.startswith("89504e47") or header.startswith("47494638") or (header.startswith("52494646") and "57454250" in header):
            st.success(f"✅ النتيجة: ملف صورة سليم من حيث البنية الداخلية.\n(البصمة: {header[:12]})")
        elif "66747970" in header or (header.startswith("52494646") and "41564920" in header):
            st.success(f"✅ النتيجة: مقطع فيديو سليم من حيث البنية الداخلية.\n(البصمة: {header[:12]})")
        elif header.startswith("4d5a") or header.startswith("504b0304"):
            st.error("🚨 خطر شديد! هذا الملف عبارة عن برنامج تنفيذي أو تطبيق متنكر وليس صورة أو فيديو!")
        else:
            st.warning(f"⚠️ تحذير! صيغة هذا الملف غير معروفة أو مشبوهة.\n(البصمة: {header[:12]})")

with tab3:
    pdf_file = st.file_uploader("ارفع مستند PDF لفحصه من الداخل", type=["pdf"])
    if pdf_file is not None:
        raw_data = pdf_file.read()
        if not raw_data.startswith(b"%PDF"):
            st.error("🚨 خطر شديد! هذا الملف متنكر بصيغة PDF ولكنه ليس مستند PDF حقيقي.")
        else:
            dangerous_tags = {b"/JavaScript": "كود جافاسكريبت مخفي", b"/JS": "كود برمجي مختصر", b"/OpenAction": "تنفيذ تلقائي عند فتح الملف", b"/Launch": "محاولة تشغيل برنامج خارجي", b"/EmbeddedFile": "ملف مرفق مخبأ بالداخل"}
            found_threats = [desc for tag, desc in dangerous_tags.items() if tag in raw_data]
            if found_threats:
                st.error("🚨 خطر! تم اكتشاف عناصر برمجية خطيرة داخل ملف الـ PDF:\n- " + "\n- ".join(found_threats))
            else:
                st.success("✅ ملف PDF سليم ولا يحتوي على أكواد تنفيذية أو مرفقات مخفية.")
