import streamlit as st
import pandas as pd
import os
import time
import urllib.parse

# 🕋 إعداد واجهة الصفحة والأيقونة العلوية للكعبة المشرفة
st.set_page_config(page_title="نظام إدارة ونقل الفنادق المتكامل", page_icon="🕋", layout="wide")

# 🔒 جدار الأمان الذكي لإخفاء شريط جيت هاب وعلامة القط نهائياً عن الزوار
st.markdown("<style>#MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} header {visibility: hidden !important;} .viewerBadge_container__16S6S {display: none !important;} stDeployButton {display: none !important;} button[title='View source code'] {display: none !important;} a[href*='github.com'] {display: none !important;}</style>", unsafe_allow_html=True)

# 📢 1. شريط إعلانات متحرك ومميز بالإدارة (حسب الطلب)
st.markdown("""
<div style="background-color: #1e3d59; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 15px;">
    🌙 عروض و رحلات العمرة متوفرة بأفضل الأسعار - طريق الميقات (فرع 11 يونيو)
</div>
""", unsafe_allow_html=True)

# 🖼️ 2. إضافة 4 مربعات تفاعلية لعروض الصور تحت شريط الإعلان
st.write("### 🏷️ أبرز العروض والرحلات الحالية:")
c_img1, c_img2, c_img3, c_img4 = st.columns(4)

with c_img1:
    st.image("https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=400", caption="عرض فنادق الساحة (VIP)", use_container_width=True)
    if st.button("👁️ عرض تفاصيل 1", use_container_width=True):
        st.info("📌 تفاصيل عرض فنادق الساحة: تشمل الإقامة القريبة من الحرم مع نقل خاص.")

with c_img2:
    st.image("https://images.unsplash.com/photo-1565552437193-470e9ea296ef?w=400", caption="رحلات العمرة الاقتصادية", use_container_width=True)
    if st.button("👁️ عرض تفاصيل 2", use_container_width=True):
        st.info("📌 تفاصيل العرض الاقتصادي: تشمل الإقامة في فنادق العزيزية مع باصات ترددية على مدار الساعة.")

with c_img3:
    st.image("https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400", caption="باقة العائلات المميزة", use_container_width=True)
    if st.button("👁️ عرض تفاصيل 3", use_container_width=True):
        st.info("📌 تفاصيل باقة العائلات: غرف متسعة وأسعار تنافسية مع خدمات متكاملة.")

with c_img4:
    st.image("https://images.unsplash.com/photo-1541971875076-8f970d573be6?w=400", caption="رحلات المدينة المنورة", use_container_width=True)
    if st.button("👁️ عرض تفاصيل 4", use_container_width=True):
        st.info("📌 تفاصيل رحلات المدينة: زيارة المسجد النبوي الشريف مع الإقامة بالقرب من باب السلام.")

st.markdown("---")
st.title("🕋 النظام الشامل لإدارة وسائل نقل وفنادق مكة المكرمة والمدينة المنورة")

excel_filename = "makkah_madinah_full_hotels_v8.xlsx"
comments_filename = "visitor_comments_database_v8.xlsx"
messages_filename = "visitor_messages_database_v8.xlsx"
bookings_filename = "visitor_bookings_database_v8.xlsx"

# 💵 تحديث سعر الصرف الموازي المعتمد (9.92)
usd_to_lyd_rate = 9.92  
profit_margin = 200.0   

# 📊 قاعدة البيانات الشاملة للفنادق
def get_all_makkah_hotels():
    hotels = [
        ("أبراج مكة", "ساحة الحرم (أجياد)", 0.1, 150),
        ("فندق الشهداء بجوار بالم ريتش مكة", "أجياد", 0.5, 90),
        ("فندق هبة الله مكة المكرمة بإدارة أكورهوتلز", "شارع إبراهيم الخليل", 0.9, 70),
        ("أبراج الميريديان مكة المكرمة", "أجياد كدي", 1.5, 60),
        ("فندق منازل أجياد من إيلاف", "أجياد", 0.6, 75),
        ("فندق مكارم أجياد مكة", "أجياد", 0.5, 85),
        ("برستيج هوتيل (إكس إيلاف المشاعر)", "العزيزية", 3.0, 45),
        ("فندق الصفوة أوركيد", "أبراج البيت", 0.1, 160),
        ("بولمان زمزم مكة", "أبراج البيت", 0.1, 155),
        ("قصر رافلز مكة", "أبراج البيت", 0.05, 250),
        ("فندق دار التوحيد إنتركونتيننتال مكة المكرمة", "ساحة الحرم", 0.05, 260),
        ("فندق صفوة الغفران مكة", "أجياد", 0.1, 140),
        ("فندق مكارم البيت", "العزيزية", 3.2, 40),
        ("برج ساعة مكة الملكي، فندق فيرمونت", "أبراج البيت", 0.05, 230),
        ("المروة ريحان من روتانا", "أبراج البيت", 0.1, 145),
        ("فندق أنجم - مكة المكرمة", "جبل الكعبة", 0.4, 95),
        ("فندق شيراتون مكة جبل الكعبة", "جبل الكعبة", 1.0, 80),
        ("فندق جبل عمر ماريوت، مكة المكرمة", "جبل عمر", 0.5, 110),
        ("حياة ريجنسي جبل عمر مكة", "جبل عمر", 0.4, 120),
        ("كونراد جبل عمر، مكة المكرمة", "جبل عمر", 0.25, 135),
        ("سويس أوتيل مكة", "أبراج البيت", 0.1, 150),
        ("سويس أوتل المقام مكة", "أبراج البيت", 0.1, 150),
        ("فندق دار الهجرة انتركونتيننتال", "المنطقة المركزية - المدينة", 0.2, 110),
        ("فندق المدينة هيلتون", "المنطقة المركزية - المدينة", 0.3, 115),
        ("فندق ميلينيوم طيبة", "المنطقة المركزية - المدينة", 0.1, 105),
        ("فندق دار التقوى", "المنطقة المركزية - المدينة", 0.15, 130),
        ("فندق أنوار المدينة موفنبيك", "المنطقة المركزية - المدينة", 0.2, 110),
        ("فندق أوبروى", "المنطقة المركزية - المدينة", 0.1, 160),
        ("شذا المدينة", "المنطقة المركزية - المدينة", 0.25, 120)
    ]
    
    data = []
    for name, area, d_val, base_price in hotels:
        lyd_base = round(base_price * usd_to_lyd_rate, 2)
        final_price_lyd = round(lyd_base + profit_margin, 2)
        maps_query = urllib.parse.quote(f"{name} مكة المكرمة")
        map_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        
        data.append({
            "اسم الفندق": name,
            "المنطقة / الحي": area,
            "المسافة إلى الحرم (كم)": d_val,
            "السعر الأساسي ($)": base_price,
            "المعادل بالسوق الموازي (د.ل)": lyd_base,
            "سعر الحجز النهائي (طريق الميقات د.ل)": final_price_lyd,
            "توفر حافلة نقل (Shuttle)": "لا" if d_val <= 0.8 else "نعم",
            "موقع الفندق على خرائط جوجل": map_link
        })
    return data

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

def load_bookings():
    return pd.read_excel(bookings_filename) if os.path.exists(bookings_filename) else pd.DataFrame(columns=["الوقت", "اسم المعتمر", "رقم الهاتف", "الفندق المطلوبة", "عدد الأيام", "إجمالي السعر (د.ل)"])

df = load_current_data()

# --- 🔐 صلاحيات المدير ---
st.header("🔐 صلاحيات النظام ودخول الإدارة")
if "logged_in" not in st.session_state: 
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    st.success("✓ وضع المدير نشط حالياً (صلاحيات كاملة بالتعديل والحذف وقراءة الحجوزات والرسائل)")
    if st.button("🔒 تسجيل الخروج والعودة الفورية لوضع الزائر", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
else:
    admin_password = st.text_input("✍️ أدخل كلمة مرور المدير لتعديل البيانات والحذف:", type="password")
    if admin_password == "1234": 
        st.session_state["logged_in"] = True
        st.rerun()

st.info("ℹ️ وضع التصفح الحالي: صلاحية زائر لشركة طريق الميقات (تصفح وفلترة وحجز آلي)")
st.markdown("---")

# --- 🧮 حاسبة الوقت والمسافة وزر الانتقال لخرائط جوجل في الشريط الجانبي ---
st.sidebar.header("🧮 حاسبة الوقت والمسافة للحرم")
calc_dist = st.sidebar.number_input("أدخل المسافة (كم):", min_value=0.1, max_value=20.0, value=1.5, step=0.1)
calc_mode = st.sidebar.radio("وسيلة النقل:", ["🚶 مشياً على الأقدام", "🚌 الحافلة الترددية (Shuttle)"])

if calc_mode == "🚶 مشياً على الأقدام":
    est_time = int(calc_dist * 12)
    st.sidebar.success(f"⏱️ الوقت المتوقع مشياً: **{est_time} دقيقة**")
else:
    est_time = int(calc_dist * 4) + 5
    st.sidebar.success(f"⏱️ الوقت المتوقع بالحافلة: **{est_time} دقيقة** (مع الانتظار)")

# 🗺️ زر الانتقال المباشر لخرائط جوجل حسب الطلب
maps_direct_link = "https://www.google.com/maps/search/?api=1&query=%D8%املسجد+الحرام+مكة+المكرمة"
st.sidebar.markdown(f"[🗺️ فتح وتحديد الموقع في خرائط جوجل]({maps_direct_link})", unsafe_allow_html=True)

st.sidebar.markdown("---")

# --- 🔍 شريط البحث والتصفية الجانبي ---
st.sidebar.header("🔍 خيارات البحث والفرز الشامل")
search_query = st.sidebar.text_input("🔍 ابحث باسم أي فندق:")
selected_district = st.sidebar.multiselect("📍 فرز حسب الحي/المنطقة:", options=df["المنطقة / الحي"].unique() if "المنطقة / الحي" in df.columns else [])
max_distance = st.sidebar.slider("📏 أقصى مسافة عن الحرم (كم):", 0.0, 10.0, 10.0, 0.1)
shuttle_only = st.sidebar.checkbox("🚌 عرض الفنادق التي توفر حافلات فقط")

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
col3.metric("💵 سعر الصرف الموازي (9.92)", f"{usd_to_lyd_rate} د.ل")

# 📋 عرض جدول الفنادق المطور مع الأسعار
st.subheader("📋 جدول الفنادق المتاحة وأسعار الحجز النهائي (طريق الميقات)")

st.data_editor(
    filtered_df,
    use_container_width=True,
    height=450,
    column_config={
        "موقع الفندق على خرائط جوجل": st.column_config.LinkColumn(
            "📍 موقع الفندق على خرائط جوجل",
            help="اضغط هنا لفتح موقع الفندق مباشرة في خرائط جوجل",
            display_text="🗺️ فتح الموقع في خرائط جوجل"
        ),
        "سعر الحجز النهائي (طريق الميقات د.ل)": st.column_config.NumberColumn(
            "💰 السعر النهائي (د.ل)",
            format="%.2f د.ل"
        )
    },
    disabled=True if not st.session_state["logged_in"] else False
)

st.markdown("---")

# 📝 استمارة حجز فندقي مباشر
st.subheader("📝 استمارة طلب حجز فندقي مباشر للمعتمرين")
with st.form("booking_form"):
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        b_name = st.text_input("✍️ اسم المعتمر الثلاثي:")
        b_phone = st.text_input("📞 رقم الهاتف / الواتساب:")
    with b_col2:
        b_hotel = st.selectbox("🏨 اختر الفندق المطلوب:", options=df["اسم الفندق"].unique() if "اسم الفندق" in df.columns else [])
        b_days = st.number_input("📅 عدد أيام الإقامة:", min_value=1, max_value=30, value=3)
    
    submit_booking = st.form_submit_button("🚀 تأكيد وإرسال طلب الحجز للإدارة", use_container_width=True)
    
    if submit_booking:
        if b_name.strip() and b_phone.strip():
            hotel_row = df[df["اسم الفندق"] == b_hotel]
            night_price = hotel_row["سعر الحجز النهائي (طريق الميقات د.ل)"].values[0] if not hotel_row.empty else 0
            total_price = night_price * b_days
            
            df_b = load_bookings()
            new_b = {
                "الوقت": time.strftime("%Y-%m-%d %H:%M:%S"),
                "اسم المعتمر": b_name,
                "رقم الهاتف": b_phone,
                "الفندق المطلوبة": b_hotel,
                "عدد الأيام": b_days,
                "إجمالي السعر (د.ل)": total_price
            }
            pd.concat([df_b, pd.DataFrame([new_b])], ignore_index=True).to_excel(bookings_filename, index=False)
            
            wa_text = urllib.parse.quote(f"طلب حجز جديد من طريق الميقات:\nالاسم: {b_name}\nالهاتف: {b_phone}\nالفندق: {b_hotel}\nالأيام: {b_days}\nالإجمالي: {total_price} د.ل")
            wa_link = f"https://wa.me/?text={wa_text}"
            
            st.success(f"🎉 تم تسجيل طلب حجزك بنجاح! الإجمالي المقدر: **{total_price} دينار ليبي**.")
            st.markdown(f"[📲 اضغط هنا لإرسال تأكيد الحجز مباشرة عبر واتساب الإدارة]({wa_link})")
            st.balloons()
        else:
            st.error("⚠️ يرجى كتابة الاسم ورقم الهاتف لإكمال الطلب.")

st.markdown("---")

if st.session_state["logged_in"]:
    st.subheader("🛠️ لوحة تحكم المدير وقراءة الحجوزات والرسائل الواردة")
    adm_col1, adm_col2, adm_col3 = st.columns(3)
    with adm_col1: 
        st.subheader("📝 طلبات الحجز الفندقي")
        st.dataframe(load_bookings(), use_container_width=True)
    with adm_col2: 
        st.subheader("💬 تقييمات الفنادق")
        st.dataframe(load_comments(), use_container_width=True)
    with adm_col3: 
        st.subheader("📩 رسائل الزوار المباشرة")
        st.dataframe(load_messages(), use_container_width=True)
else:
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

st.sidebar.markdown("---")
if os.path.exists(excel_filename):
    with open(excel_filename, "rb") as file:
        st.sidebar.download_button(label="📥 تنزيل جدول الفنادق والأسعار كملف Excel", data=file, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
