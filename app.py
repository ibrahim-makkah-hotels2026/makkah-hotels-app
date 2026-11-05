import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
import time

# 🕋 إعداد واجهة الصفحة والأيقونة العلوية للكعبة المشرفة
st.set_page_config(page_title="نظام إدارة ونقل الفنادق المتكامل", page_icon="🕋", layout="wide")

# 🔒 جدار الأمان الذكي لإخفاء شريط جيت هاب وعلامة القط نهائياً عن الزوار وحظر الفضول
st.markdown("<style>#MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} header {visibility: hidden !important;} .viewerBadge_container__16S6S {display: none !important;} stDeployButton {display: none !important;} button[title='View source code'] {display: none !important;} a[href*='github.com'] {display: none !important;}</style>", unsafe_allow_html=True)
st.title("🕋 النظام الشامل لإدارة وسائل نقل وفنادق مكة المكرمة بالكامل")

excel_filename = "makkah_hotels_database_v3.xlsx"
comments_filename = "visitor_comments_database_v3.xlsx"
messages_filename = "visitor_messages_database_v3.xlsx"

# 📊 قاعدة البيانات الكبرى المدمجة لجميع فنادق مكة المكرمة بالكامل بإحداثياتها الدقيقة لمطابقة خرائط جوجل
def get_all_makkah_hotels():
    return [
        {"اسم الفندق": "فندق أسطورة أعمار", "المنطقة / الحي": "العزيزية (محبس الجن)", "المسافة إلى الحرم (كم)": 2.0, "الوقت مشياً (دقيقة)": 25, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "محبس الجن", "latitude": 21.4165, "longitude": 39.8450},
        {"اسم الفندق": "فندق برايد جوي", "المنطقة / الحي": "العزيزية (محبس الجن)", "المسافة إلى الحرم (كم)": 1.8, "الوقت مشياً (دقيقة)": 22, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "أمام الفندق", "latitude": 21.4172, "longitude": 39.8435},
        {"اسم الفندق": "فندق ميدان", "المنطقة / الحي": "العزيزية الجنوبية", "المسافة إلى الحرم (كم)": 3.0, "الوقت مشياً (دقيقة)": 40, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "باص الفندق", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "بوابة الفندق", "latitude": 21.4050, "longitude": 39.8520},
        {"اسم الفندق": "فندق ذرة طيبة", "المنطقة / الحي": "العزيزية (شارع الإحسان)", "المسافة إلى الحرم (كم)": 3.5, "الوقت مشياً (دقيقة)": 45, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "شتل ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "أوقات الصلوات", "موقع محطة الحافلة": "شارع الإحسان", "latitude": 21.4085, "longitude": 39.8590},
        {"اسم الفندق": "فندق ضيافة الرجاء", "المنطقة / الحي": "الهجلة (شارع إبراهيم الخليل)", "المسافة إلى الحرم (كم)": 0.8, "الوقت مشياً (دقيقة)": 10, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "لا يتطلب باص", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4150, "longitude": 39.8240},
        {"اسم الفندق": "فندق اعمار جراند", "المنطقة / الحي": "الهجلة (شارع إبراهيم الخليل)", "المسافة إلى الحرم (كم)": 0.75, "الوقت مشياً (دقيقة)": 9, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "لا يتطلب باص", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4155, "longitude": 39.8245},
        {"اسم الفندق": "فندق الاباء", "المنطقة / الحي": "جرول (طريق أم القرى)", "المسافة إلى الحرم (كم)": 1.2, "الوقت مشياً (دقيقة)": 15, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات النقل الترددي", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "موقف جرول", "latitude": 21.4320, "longitude": 39.8180},
        {"اسم الفندق": "فندق إعمار النور", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 3.0, "الوقت مشياً (دقيقة)": 30, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات شتل", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "الشارع الرئيسي", "latitude": 21.4120, "longitude": 39.8490},
        {"اسم الفندق": "فندق فوكو مكة", "المنطقة / الحي": "المسفلة (شارع إبراهيم الخليل)", "المسافة إلى الحرم (كم)": 1.3, "الوقت مشياً (دقيقة)": 18, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "باصات شتل الفندق", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "ساحة الفندق", "latitude": 21.4082, "longitude": 39.8239},
        {"اسم الفندق": "فندق هيلتون جبل عمر", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.3, "الوقت مشياً (دقيقة)": 4, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر لساحة الحرم", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "قريب جداً", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4205, "longitude": 39.8230},
        {"اسم الفندق": "فندق سويس مقام مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "داخل الساحة مباشرة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "مشي فوري", "موقع محطة الحافلة": "مشي عبر الأبراج", "latitude": 21.4190, "longitude": 39.8260},
        {"اسم الفندق": "فندق أسطورة أجياد", "المنطقة / الحي": "أجياد السد", "المسافة إلى الحرم (كم)": 0.6, "الوقت مشياً (دقيقة)": 8, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "لا يتطلب باص", "موقع محطة الحافلة": "مشي عبر شارع أجياد", "latitude": 21.4170, "longitude": 39.8290},
        {"اسم الفندق": "فندق قصر مكة رافلز", "المنطقة / الحي": "أبراج البيت (وقف الملك عبدالعزيز)", "المسافة إلى الحرم (كم)": 0.05, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مباشرة على الساحة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "اتصال فوري بالساحة", "موقع محطة الحافلة": "مشي فوري", "latitude": 21.4192, "longitude": 39.8258},
        {"اسم الفندق": "فندق فيرمونت مكة (برج الساعة)", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.05, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مباشرة على الساحة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "اتصال فوري بالساحة", "موقع محطة الحافلة": "مشي فوري", "latitude": 21.4188, "longitude": 39.8262},
        {"اسم الفندق": "فندق بولمان زمزم مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 2, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "اتصال فوري", "موقع محطة الحافلة": "مشي فوري", "latitude": 21.4182, "longitude": 39.8255},
        {"اسم الفندق": "فندق كونراد مكة", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.25, "الوقت مشياً (دقيقة)": 3, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "قريب جداً", "موقع محطة الحافلة": "ساحة جبل عمر", "latitude": 21.4212, "longitude": 39.8235},
        {"اسم الفندق": "فندق جبل عمر أراكل", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.4, "الوقت مشياً (دقيقة)": 5, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "قريب جداً", "موقع محطة الحافلة": "ساحة جبل عمر", "latitude": 21.4218, "longitude": 39.8225},
        {"اسم الفندق": "فندق أنجم مكة", "المنطقة / الحي": "الشبيكة / جبل الكعبة", "المسافة إلى الحرم (كم)": 0.4, "الوقت مشياً (دقيقة)": 5, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي عبر الأنفاق الشمالية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "لا يتطلب باص", "موقع محطة الحافلة": "نفق الشبيكة المباشر", "latitude": 21.4245, "longitude": 39.8215},
        {"اسم الفندق": "فندق حياك مكة", "المنطقة / الحي": "جرول", "المسافة إلى الحرم (كم)": 1.5, "الوقت مشياً (دقيقة)": 18, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات مكة الترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "محطة جرول", "latitude": 21.4335, "longitude": 39.8160},
        {"اسم الفندق": "فندق مواسم الرائد", "المنطقة / الحي": "الروضة", "المسافة إلى الحرم (كم)": 2.8, "الوقت مشياً (دقيقة)": 35, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "شارع الروضة", "latitude": 21.4380, "longitude": 39.8410},
        {"اسم الفندق": "فندق مكارم أم القرى", "المنطقة / الحي": "أجياد المصافي", "المسافة إلى الحرم (كم)": 1.5, "الوقت مشياً (دقيقة)": 20, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات الفندق الخاصة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "بوابة الفندق", "latitude": 21.4115, "longitude": 39.8320},
        {"اسم الفندق": "فندق كودي مكة", "المنطقة / الحي": "كدي", "المسافة إلى الحرم (كم)": 3.2, "الوقت مشياً (دقيقة)": 42, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "موقف كدي الترددي", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "محطة باصات كدي", "latitude": 21.3980, "longitude": 39.8295},
        {"اسم الفندق": "فندق ميركيور مكة", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 3.8, "الوقت مشياً (دقيقة)": 48, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات مكة العامة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "طريق مسجد الشيخ ابن باز", "latitude": 21.4110, "longitude": 39.8620},
        {"اسم الفندق": "فندق درة الأصيل", "المنطقة / الحي": "المحبس", "المسافة إلى الحرم (كم)": 2.2, "الوقت مشياً (دقيقة)": 28, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "محبس الجن", "latitude": 21.4178, "longitude": 39.8475},
        {"اسم الفندق": "فندق نوازي دثر", "المنطقة / الحي": "التنعيم", "المسافة إلى الحرم (كم)": 6.5, "الوقت مشياً (دقيقة)": 80, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية / باصات مكة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "شارع المدينة المنورة", "latitude": 21.4650, "longitude": 39.7990},
        {"اسم الفندق": "فندق شذا مكة", "المنطقة / الحي": "جبل الكعبة", "المسافة إلى الحرم (كم)": 0.7, "الوقت مشياً (دقيقة)": 9, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "قريب جداً", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4270, "longitude": 39.8205},
        {"اسم الفندق": "فندق روتانا جبل عمر", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.35, "الوقت مشياً (دقيقة)": 4, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "قريب جداً", "موقع محطة الحافلة": "ساحة جبل عمر", "latitude": 21.4208, "longitude": 39.8228},
        {"اسم الفندق": "فندق بارك إن باي راديسون العزيزية", "المنطقة / الحي": "العزيزية الشمالية", "المسافة إلى الحرم (كم)": 4.2, "الوقت مشياً (دقيقة)": 55, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات الفندق الترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "أمام البوابة الرئيسية", "latitude": 21.4135, "longitude": 39.8685},
        {"اسم الفندق": "فندق ريحانة روتانا مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.08, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي فوري لساحة الحرم", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "اتصال مباشر", "موقع محطة الحافلة": "مشي فوري", "latitude": 21.4187, "longitude": 39.8259},
        {"اسم الفندق": "فندق ثروة التيسير", "المنطقة / الحي": "التيسير", "المسافة إلى الحرم (كم)": 1.4, "الوقت مشياً (دقيقة)": 17, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات مكة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "شارع التيسير", "latitude": 21.4310, "longitude": 39.8130}
    ]

# 🔄 تحميل البيانات مع الضمان التلقائي لملء الجدول
def load_current_data():
    if os.path.exists(excel_filename):
        try:
            df_read = pd.read_excel(excel_filename)
            if not df_read.empty:
                return df_read
        except Exception:
            pass
    # إذا كان الملف غير موجود أو فارغاً يتم إنشاؤه ممتلئاً بالبيانات
    df_init = pd.DataFrame(get_all_makkah_hotels())
    df_init.to_excel(excel_filename, index=False)
    return df_init

def load_comments():
    return pd.read_excel(comments_filename) if os.path.exists(comments_filename) else pd.DataFrame(columns=["الوقت", "الفندق المستهدف", "التقييم", "التعليق"])

def load_messages():
    return pd.read_excel(messages_filename) if os.path.exists(messages_filename) else pd.DataFrame(columns=["الوقت", "الاسم", "نص الرسالة"])

# تحميل البيانات الفعلية
df = load_current_data()

# --- 🔐 جدار حماية الأدمن في أعلى الشاشة ---
st.header("🔐 صلاحيات النظام ودخول الإدارة")
if "logged_in" not in st.session_state: 
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    st.success("✓ وضع المدير نشط حالياً (صلاحيات كاملة بالتعديل والحذف وقراءة الرسائل والتعليقات)")
    if st.button("🔒 تسجيل الخروج والعودة الفورية لوضع الزائر", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
else:
    admin_password = st.text_input("✍️ أدخل كلمة مرور المدير لتعديل البيانات والحذف:", type="password")
    if admin_password == "1234": 
        st.session_state["logged_in"] = True
        st.rerun()

st.info("ℹ️ وضع التصفح الحالي: صلاحية زائر لشركة طريق الميقات (تصفح وفلترة كاملة)")
st.markdown("---")

# --- 🔍 شريط التصفية الجانبي (يسار الشاشة) ---
st.sidebar.header("🔍 خيارات البحث والفرز الشامل")
search_query = st.sidebar.text_input("🔍 ابحث باسم أي فندق بمكة المكرمة:")
selected_district = st.sidebar.multiselect("📍 فرز وتصفية حسب الحي/المنطقة بمكة:", options=df["المنطقة / الحي"].unique() if "المنطقة / الحي" in df.columns else [])
max_distance = st.sidebar.slider("📏 أقصى مسافة عن الحرم (كم):", 0.0, 10.0, 10.0, 0.1)
shuttle_only = st.sidebar.checkbox("🚌 عرض الفنادق التي توفر حافلات نقل فقط")

filtered_df = df.copy()
if max_distance and 'المسافة إلى الحرم (كم)' in filtered_df.columns: 
    filtered_df = filtered_df[filtered_df['المسافة إلى الحرم (كم)'] <= max_distance]
if search_query and 'اسم الفندق' in filtered_df.columns: 
    filtered_df = filtered_df[filtered_df['اسم الفندق'].str.contains(search_query, case=False, na=False)]
if selected_district and 'المنطقة / الحي' in filtered_df.columns: 
    filtered_df = filtered_df[filtered_df['المنطقة / الحي'].isin(selected_district)]
if shuttle_only and 'توفر حافلة نقل (Shuttle)' in filtered_df.columns: 
    filtered_df = filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']

col1, col2, col3 = st.columns(3)
col1.metric("📊 إجمالي فنادق مكة المعروضة", len(filtered_df))
if not filtered_df.empty and 'المسافة إلى الحرم (كم)' in filtered_df.columns: 
    col2.metric("📍 أقرب فندق متوفر حالياً", f"{filtered_df['المسافة إلى الحرم (كم)'].min()} كم")
if not filtered_df.empty and 'توفر حافلة نقل (Shuttle)' in filtered_df.columns: 
    col3.metric("🚌 فنادق توفر حافلات ترددية", len(filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']))

col_table, col_map = st.columns(2)
with col_table:
    st.subheader("📋 جدول الفنادق المتاحة وتفاصيل النقل")
    st.dataframe(filtered_df, use_container_width=True, height=400)

with col_map:
    st.subheader("🗺️ الخريطة الجغرافية لمدينة مكة المكرمة (مطابقة لخرائط جوجل)")
    haram_lat, haram_lon = 21.4225, 39.8262
    m = folium.Map(location=[haram_lat, haram_lon], zoom_start=14, tiles="OpenStreetMap")
    folium.Marker([haram_lat, haram_lon], popup="🕌 المسجد الحرام", tooltip="المسجد الحرام", icon=folium.Icon(color="darkpurple", icon="home", prefix="fa")).add_to(m)
    folium.Circle(radius=3000, location=[haram_lat, haram_lon], color="blue", fill=True, fill_color="cyan", fill_opacity=0.08).add_to(m)
    for idx, row in filtered_df.iterrows():
        if pd.notna(row.get('latitude')) and pd.notna(row.get('longitude')):
            color = "green" if "نعم" in str(row.get('توفر حافلة نقل (Shuttle)', 'لا')) else "orange"
            folium.Marker([row['latitude'], row['longitude']], popup=f"{row.get('اسم الفندق')}<br>المسافة: {row.get('المسافة إلى الحرم (كم)')} كم", icon=folium.Icon(color=color, icon="info-sign")).add_to(m)
    map_data = st_folium(m, width=600, height=400, returned_objects=["last_clicked"])

clicked_lat = map_data["last_clicked"]["lat"] if map_data and map_data.get("last_clicked") else 21.4082
clicked_lon = map_data["last_clicked"]["lng"] if map_data and map_data.get("last_clicked") else 39.8239

st.markdown("---")

if st.session_state["logged_in"]:
    st.subheader("🛠️ لوحة تحكم المدير وتعديل الإحداثيات اليدوية وقراءة الرسائل والتعليقات الواردة")
    c_edit, c_del = st.columns(2)
    with c_edit:
        st.subheader("🎯 تعديل ونقل موقع فندق يدوياً بالضغط على الخريطة")
        hotel_to_update = st.selectbox("🎯 اختر الفندق لتعديل مكانه:", options=df["اسم الفندق"].unique() if "اسم الفندق" in df.columns else None)
        if st.button("🎯 تحديث موقع الفندق إلى النقطة المحددة وتصحيحه", use_container_width=True):
            cdf = load_current_data()
            cdf.loc[cdf['اسم الفندق'] == hotel_to_update, ['latitude', 'longitude']] = [clicked_lat, clicked_lon]
            cdf.to_excel(excel_filename, index=False)
            st.success("🎯 تم بنجاح نقل وتعديل الموقع الجغرافي الفعلي لفندقك!")
            time.sleep(0.5)
            st.rerun()
    with c_del:
        st.subheader("🗑️ حذف وتطهير فندق من القائمة")
        hotel_to_delete = st.selectbox("❌ اختر الفندق لحذفه نهائياً من قاعدة البيانات:", options=df["اسم الفندق"].unique() if "اسم الفندق" in df.columns else None)
        if st.button("🗑️ تأكيد الحذف ومسحه فوراً من الإكسيل", use_container_width=True):
            cdf = load_current_data()
            cdf[cdf["اسم الفندق"] != hotel_to_delete].to_excel(excel_filename, index=False)
            st.error("❌ تم حذف الفندق وتصفية البيانات نهائياً!")
            time.sleep(0.5)
            st.rerun()
    
    st.markdown("---")
    adm_col1, adm_col2 = st.columns(2)
    with adm_col1: 
        st.subheader("💬 تعليقات وتقييمات الفنادق الواردة")
        st.dataframe(load_comments(), use_container_width=True)
    with adm_col2: 
        st.subheader("📩 رسائل واستفسارات الزوار المباشرة")
        st.dataframe(load_messages(), use_container_width=True)
else:
    # 🟢 لوحة تواصل الزوار (تم إخفاء الجملة المحددة باللون الأزرق بناءً على طلبك)
    st.subheader("🤝 لوحة تواصل الزوار")
    fb_link = "https://www.facebook.com/share/1DveNwUUvR/"
    tiktok_link = "https://www.tiktok.com/@miqat_11june_branch?is_from_webapp=1&sender_device=pc"
    maps_link = "https://maps.app.goo.gl/6VL4dgZ3EuWsj46XA?g_st=ac"
    
    link_c1, link_c2, link_c3, link_c4 = st.columns(4)
    with link_c1: st.link_button("🌐 تابعنا على صفحة فيسبوك", fb_link, use_container_width=True)
    with link_c2: st.link_button("🎵 تابعنا على حساب تيك توك", tiktok_link, use_container_width=True)
    with link_c3: st.link_button("📍 زيارة موقعنا بجوجل ماب", maps_link, use_container_width=True)
    with link_c4: 
        if st.button("👍 الإعجاب السريع للمعتمرين", use_container_width=True): 
            st.toast("❤️ شكرًا لك على إعجابك وتثمينك لخدماتنا!")
            st.balloons()
            
    st.markdown("---")
    visitor_col1, visitor_col2 = st.columns(2)
    with visitor_col1:
        st.subheader("💬 إضافة تعليق ومراجعة مخصصة لفندق")
        v_hotel = st.selectbox("🎯 اختر الفندق المراد تقييمه:", options=df["اسم الفندق"].unique() if "اسم الفندق" in df.columns else None)
        v_rating = st.select_slider("⭐ اختر تقييمك للفندق:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
        v_comment = st.text_area("✍️ اكتب مراجعتك أو تعليقك هنا حول الفندق والباص:", key="visitor_comment_box")
        if st.button("💬 نشر وإرسال التعليق فوراً", use_container_width=True):
            if v_comment.strip():
                df_c = load_comments()
                new_c = {"الوقت": time.strftime("%Y-%m-%d %H:%M:%S"), "الفندق المستهدف": v_hotel, "التقييم": v_rating, "التعليق": v_comment}
                pd.concat([df_c, pd.DataFrame([new_c])], ignore_index=True).to_excel(comments_filename, index=False)
                st.success("🎉 تم تسجيل مراجعتك وتعليقك بنجاح للشركة!")
                st.balloons()
                time.sleep(0.5)
                st.rerun()
            else: 
                st.error("⚠️ اكتب تعليقك أولاً.")
    with visitor_col2:
        st.subheader("📩 إرسال رسالة مباشرة واقتراح إلى الإدارة")
        v_name = st.text_input("✍️ اسمك الموقر (اختياري):", placeholder="مثال: معتمر من ليبيا")
        v_msg = st.text_area("✉️ اكتب نص رسالتك أو استفسارك هنا بالتفصيل:", key="visitor_message_box")
        if st.button("🚀 إرسال الرسالة إلى المدير فوراً", use_container_width=True):
            if v_msg.strip():
                df_m = load_messages()
                sender = v_name.strip() if v_name.strip() else "زائر مجهول"
                new_m = {"الوقت": time.strftime("%Y-%m-%d %H:%M:%S"), "الاسم": sender, "نص الرسالة": v_msg}
                pd.concat([df_m, pd.DataFrame([new_m])], ignore_index=True).to_excel(messages_filename, index=False)
                st.success("📥 تم إرسال رسالتك بنجاح وسيتطلع عليها المدير.")
                st.balloons()
                time.sleep(0.5)
                st.rerun()
            else: 
                st.error("⚠️ اكتب نص الرسالة أولاً.")

st.sidebar.markdown("---")
if os.path.exists(excel_filename):
    with open(excel_filename, "rb") as file:
        st.sidebar.download_button(label="📥 تنزيل جدول الفنادق الحالي كملف Excel", data=file, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
