import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

# 🕋 إعداد واجهة الصفحة والأيقونة العلوية للكعبة المشرفة
st.set_page_config(page_title="نظام إدارة ونقل الفنادق المتكامل", page_icon="🕋", layout="wide")

# 🔒 جدار الأمان الذكي لإخفاء شريط جيت هاب وعلامة القط نهائياً عن الزوار لحظر فضولهم
st.markdown("<style>#MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} header {visibility: hidden !important;} .viewerBadge_container__16S6S {display: none !important;} stDeployButton {display: none !important;} button[title='View source code'] {display: none !important;} a[href*='github.com'] {display: none !important;}</style>", unsafe_allow_html=True)
st.title("🕋 النظام المتكامل لإدارة وسائل نقل وفنادق الحرم المكي الشريف")

excel_filename = "hotel_transport_data_v2.xlsx"
comments_filename = "hotel_visitor_comments.xlsx"
messages_filename = "hotel_visitor_messages.xlsx"
haram_lat, haram_lon = 21.4225, 39.8262 # إحداثيات الكعبة المشرفة الرسمية بخرائط جوجل

def load_current_data():
    if os.path.exists(excel_filename): return pd.read_excel(excel_filename)
    df_init = pd.DataFrame([{"اسم الفندق": "فندق أسطورة أعمار", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 2.0, "الوقت مشياً (دقيقة)": 25, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات مكة العامة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "محبس الجن", "latitude": 21.4165, "longitude": 39.8450}])
    df_init.to_excel(excel_filename, index=False); return df_init

def load_comments(): return pd.read_excel(comments_filename) if os.path.exists(comments_filename) else pd.DataFrame(columns=["الوقت", "الفندق المستهدف", "التقييم", "التعليق"])
def load_messages(): return pd.read_excel(messages_filename) if os.path.exists(messages_filename) else pd.DataFrame(columns=["الوقت", "الاسم", "نص الرسالة"])

df = load_current_data()

# --- 🔐 جدار حماية الصلاحيات المطور في أعلى الصفحة لخانات المدير ---
st.header("🔐 صلاحيات النظام ودخول الإدارة")
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    st.success("✓ وضع المدير نشط حالياً (صلاحيات كاملة بالتعديل والحذف وقراءة الرسائل)")
    if st.sidebar.button("🔒 تسجيل الخروج والعودة الفورية لوضع الزائر", use_container_width=True):
        st.session_state["logged_in"] = False; st.rerun()
else:
    admin_password = st.text_input("✍️ أدخل كلمة مرور المدير لتعديل البيانات والحذف:", type="password")
    if admin_password == "1234": st.session_state["logged_in"] = True; st.rerun()
    st.info("ℹ️ وضع التصفح الحالي: صلاحية زائر (عرض وبحث عام فقط بدون تعديل أو حذف)")

st.markdown("---")

# --- 🔍 محرك البحث الجغرافي الخارق لكافة فنادق مكة المكرمة بالكامل بناءً على خرائط جوجل الدقيقة ---
st.subheader("🔍 مستكشف وباحث الفنادق الشامل بمكة المكرمة (عبر الأقمار الصناعية)")
st.info("💡 اكتب اسم أي فندق موجود في مكة بالكامل وعنوانه، وسيتتبع النظام بوابته الرسمية ويحسب مسافته ووقت المشي للحرم تلقائياً!")

search_hotel_input = st.text
