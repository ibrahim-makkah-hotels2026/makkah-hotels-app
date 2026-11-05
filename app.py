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
st.title("🕋 النظام الشامل لإدارة وسائل نقل وفنادق مكة المكرمة والمدينة المنورة")

excel_filename = "makkah_hotels_database_v3.xlsx"
comments_filename = "visitor_comments_database_v3.xlsx"
messages_filename = "visitor_messages_database_v3.xlsx"

# 📊 قاعدة البيانات الكبرى المدمجة لجميع فنادق مكة المكرمة والمدينة المنورة بإحداثياتها الدقيقة
def get_all_makkah_hotels():
    return [
        # فنادق مكة المكرمة المضافة بالكامل
        {"اسم الفندق": "أبراج مكة", "المنطقة / الحي": "سحة الحرم", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي فوري", "latitude": 21.4190, "longitude": 39.8260},
        {"اسم الفندق": "فندق الشهداء", "المنطقة / الحي": "أجياد", "المسافة إلى الحرم (كم)": 0.5, "الوقت مشياً (دقيقة)": 6, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4180, "longitude": 39.8270},
        {"اسم الفندق": "فندق هبة الله مكة المكرمة", "المنطقة / الحي": "شارع إبراهيم الخليل", "المسافة إلى الحرم (كم)": 0.9, "الوقت مشياً (دقيقة)": 11, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4140, "longitude": 39.8235},
        {"اسم الفندق": "أبراج الميريديان مكة المكرمة", "المنطقة / الحي": "أجياد كدي", "المسافة إلى الحرم (كم)": 1.5, "الوقت مشياً (دقيقة)": 20, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "نفق كدي", "latitude": 21.4100, "longitude": 39.8290},
        {"اسم الفندق": "فندق منازل أجياد من إيلاف", "المنطقة / الحي": "أجياد", "المسافة إلى الحرم (كم)": 0.6, "الوقت مشياً (دقيقة)": 7, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4175, "longitude": 39.8275},
        {"اسم الفندق": "فندق مكارم أجياد مكة", "المنطقة / الحي": "أجياد", "المسافة إلى الحرم (كم)": 0.5, "الوقت مشياً (دقيقة)": 6, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4178, "longitude": 39.8280},
        {"اسم الفندق": "برستيج هوتيل (إكس إيلاف المشاعر)", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 3.0, "الوقت مشياً (دقيقة)": 35, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "أمام الفندق", "latitude": 21.4120, "longitude": 39.8490},
        {"اسم الفندق": "فندق الصفوة أوركيد", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4185, "longitude": 39.8275},
        {"اسم الفندق": "بولمان زمزم مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4182, "longitude": 39.8255},
        {"اسم الفندق": "قصر رافلز مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.05, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4192, "longitude": 39.8258},
        {"اسم الفندق": "فندق دار التوحيد إنتركونتيننتال", "المنطقة / الحي": "ساحة الحرم", "المسافة إلى الحرم (كم)": 0.05, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4200, "longitude": 39.8260},
        {"اسم الفندق": "فندق صفوة الغفران مكة", "المنطقة / الحي": "أجياد", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4185, "longitude": 39.8275},
        {"اسم الفندق": "فندق مكارم البيت", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 3.2, "الوقت مشياً (دقيقة)": 40, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات ترددية", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "أمام الفندق", "latitude": 21.4110, "longitude": 39.8520},
        {"اسم الفندق": "برج ساعة مكة الملكي، فندق فيرمونت", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.05, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4188, "longitude": 39.8262},
        {"اسم الفندق": "المروة ريحان من روتانا", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4190, "longitude": 39.8250},
        {"اسم الفندق": "فندق أنجم - مكة المكرمة", "المنطقة / الحي": "جبل الكعبة", "المسافة إلى الحرم (كم)": 0.4, "الوقت مشياً (دقيقة)": 5, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4245, "longitude": 39.8215},
        {"اسم الفندق": "فندق شيراتون مكة جبل الكعبة", "المنطقة / الحي": "جبل الكعبة", "المسافة إلى الحرم (كم)": 1.0, "الوقت مشياً (دقيقة)": 12, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات شتل", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "بوابة الفندق", "latitude": 21.4280, "longitude": 39.8190},
        {"اسم الفندق": "فندق جبل عمر ماريوت، مكة المكرمة", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.5, "الوقت مشياً (دقيقة)": 7, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "ساحة جبل عمر", "latitude": 21.4210, "longitude": 39.8210},
        {"اسم الفندق": "حياة ريجنسي جبل عمر مكة", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.4, "الوقت مشياً (دقيقة)": 5, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "ساحة جبل عمر", "latitude": 21.4212, "longitude": 39.8225},
        {"اسم الفندق": "كونراد جبل عمر، مكة المكرمة", "المنطقة / الحي": "جبل عمر", "المسافة إلى الحرم (كم)": 0.25, "الوقت مشياً (دقيقة)": 3, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "ساحة جبل عمر", "latitude": 21.4212, "longitude": 39.8235},
        {"اسم الفندق": "سويس أوتيل مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4190, "longitude": 39.8260},
        {"اسم الفندق": "سويس أوتل المقام مكة", "المنطقة / الحي": "أبراج البيت", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 21.4188, "longitude": 39.8260},
        
        # فنادق المدينة المنورة المضافة بالكامل
        {"اسم الفندق": "فندق دار الهجرة انتركونتيننتال", "المنطقة / الحي": "المركز المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.2, "الوقت مشياً (دقيقة)": 3, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4680, "longitude": 39.6110},
        {"اسم الفندق": "فندق المدينة هيلتون", "المنطقة / الحي": "المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.3, "الوقت مشياً (دقيقة)": 4, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4700, "longitude": 39.6100},
        {"اسم الفندق": "فندق ميلينيوم طيبة", "المنطقة / الحي": "المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4690, "longitude": 39.6120},
        {"اسم الفندق": "فندق دار التقوى", "المنطقة / الحي": "المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.15, "الوقت مشياً (دقيقة)": 2, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4710, "longitude": 39.6115},
        {"اسم الفندق": "فندق أنوار المدينة موفنبيك", "المنطقة / الحي": "المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.2, "الوقت مشياً (دقيقة)": 3, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4685, "longitude": 39.6130},
        {"اسم الفندق": "فندق أوبروى", "المنطقة / الحي": "المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.1, "الوقت مشياً (دقيقة)": 1, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4695, "longitude": 39.6105},
        {"اسم الفندق": "شذا المدينة", "المنطقة / الحي": "المركزية - المدينة", "المسافة إلى الحرم (كم)": 0.25, "الوقت مشياً (دقيقة)": 3, "توفر حافلة نقل (Shuttle)": "لا", "نوع وسيلة النقل": "مشي مباشر", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "مشي مباشر", "latitude": 24.4715, "longitude": 39.6095}
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
search_query = st.sidebar.text_input("🔍 ابحث باسم أي فندق:")
selected_district = st.sidebar.multiselect("📍 فرز وتصفية حسب الحي/المنطقة:", options=df["المنطقة / الحي"].unique() if "المنطقة / الحي" in df.columns else [])
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
col1.metric("📊 إجمالي الفنادق المعروضة", len(filtered_df))
if not filtered_df.empty and 'المسافة إلى الحرم (كم)' in filtered_df.columns: 
    col2.metric("📍 أقرب فندق متوفر حالياً", f"{filtered_df['المسافة إلى الحرم (كم)'].min()} كم")
if not filtered_df.empty and 'توفر حافلة نقل (Shuttle)' in filtered_df.columns: 
    col3.metric("🚌 فنادق توفر حافلات ترددية", len(filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']))

col_table, col_map = st.columns(2)
with col_table:
    st.subheader("📋 جدول الفنادق المتاحة وتفاصيل النقل")
    st.dataframe(filtered_df, use_container_width=True, height=400)

with col_map:
    st.subheader("🗺️ الخريطة الجغرافية التفاعلية")
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
    # 🟢 لوحة تواصل الزوار (بدون الجملة الزائدة)
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
