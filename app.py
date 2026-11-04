import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time

st.set_page_config(page_title="نظام إدارة ونقل الفنادق المتكامل", page_icon="🕋", layout="wide")
st.title("🕋 النظام المتكامل لإدارة وسائل نقل وفنادق الحرم المكي الشريف")

excel_filename = "hotel_transport_data_v2.xlsx"
comments_filename = "hotel_visitor_comments.xlsx"
messages_filename = "hotel_visitor_messages.xlsx"

def load_current_data():
    if os.path.exists(excel_filename): return pd.read_excel(excel_filename)
    else:
        df_init = pd.DataFrame([{"اسم الفندق": "فندق أسطورة أعمار", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 2.0, "الوقت مشياً (دقيقة)": 25, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات مكة العامة", "تكلفة النقل": "مجاني", "مواعيد الخدمة": "24 ساعة", "موقع محطة الحافلة": "محبس الجن", "latitude": 21.4165, "longitude": 39.8450}])
        df_init.to_excel(excel_filename, index=False)
        return df_init

def load_comments():
    if os.path.exists(comments_filename): return pd.read_excel(comments_filename)
    else:
        df_init = pd.DataFrame(columns=["الوقت", "الفندق المستهدف", "التقييم", "التعليق"])
        df_init.to_excel(comments_filename, index=False)
        return df_init

def load_messages():
    if os.path.exists(messages_filename): return pd.read_excel(messages_filename)
    else:
        df_init = pd.DataFrame(columns=["الوقت", "الاسم", "نص الرسالة"])
        df_init.to_excel(messages_filename, index=False)
        return df_init

df = load_current_data()

st.sidebar.header("🔐 تسجيل دخول الإدارة")
admin_password = st.sidebar.text_input("أدخل كلمة مرور المدير لتعديل البيانات:", type="password")
is_admin = (admin_password == "1234") 

if is_admin: st.sidebar.success("✓ وضع المدير نشط (صلاحيات كاملة)")
else: st.sidebar.info("ℹ️ وضع التصفح الحالي: صلاحية زائر (عرض فقط)")

st.sidebar.markdown("---")
st.sidebar.header("🔍 خيارات البحث والتصفية")
search_query = st.sidebar.text_input("ابحث باسم الفندق:")
selected_district = st.sidebar.multiselect("تصفية حسب الحي:", options=df["المنطقة / الحي"].unique())
max_distance = st.sidebar.slider("أقصى مسافة (كم):", 0.0, 5.0, 5.0, 0.1)
shuttle_only = st.sidebar.checkbox("الفنادق التي توفر حافلات فقط")

filtered_df = df[df['المسافة إلى الحرم (كم)'] <= max_distance]
if search_query: filtered_df = filtered_df[filtered_df['اسم الفندق'].str.contains(search_query, case=False, na=False)]
if selected_district: filtered_df = filtered_df[filtered_df['المنطقة / الحي'].isin(selected_district)]
if shuttle_only: filtered_df = filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']

col1, col2, col3 = st.columns(3)
col1.metric("📊 إجمالي الفنادق المعروضة", len(filtered_df))
if not filtered_df.empty:
    col2.metric("📍 أقرب مسافة", f"{filtered_df['المسافة إلى الحرم (كم)'].min()} كم")
    col3.metric("🚌 فنادق توفر حافلات", len(filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']))

col_table, col_map = st.columns(2)
with col_table:
    st.subheader("📋 جدول الفنادق المتاحة وتفاصيل النقل")
    st.dataframe(filtered_df, use_container_width=True, height=400)

with col_map:
    st.subheader("🗺️ الخريطة الجغرافية التفاعلية حية")
    haram_lat, haram_lon = 21.4225, 39.8262
    m = folium.Map(location=[haram_lat, haram_lon], zoom_start=14, tiles="OpenStreetMap")
    folium.Marker([haram_lat, haram_lon], popup="🕌 المسجد الحرام", tooltip="المسجد الحرام", icon=folium.Icon(color="darkpurple", icon="home", prefix="fa")).add_to(m)
    folium.Circle(radius=3000, location=[haram_lat, haram_lon], color="blue", fill=True, fill_color="cyan", fill_opacity=0.08).add_to(m)
    
    for idx, row in filtered_df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            color = "green" if row['توفر hافلة نقل (Shuttle)'] == "نعم" else "orange"
            folium.Marker([row['latitude'], row['longitude']], popup=f"<b>{row['اسم الفندق']}</b>", icon=folium.Icon(color=color, icon="info-sign")).add_to(m)
            
    map_data = st_folium(m, width=600, height=400, returned_objects=["last_clicked"])

clicked_lat = map_data["last_clicked"]["lat"] if map_data and map_data.get("last_clicked") else 21.4082
clicked_lon = map_data["last_clicked"]["lng"] if map_data and map_data.get("last_clicked") else 39.8239

st.markdown("---")
st.subheader("📊 مقارنة بصرية ذكية بين الفنادق")
if not filtered_df.empty:
    ch1, ch2 = st.columns(2)
    with ch1: st.bar_chart(filtered_df.set_index("اسم الفندق")["المسافة إلى الحرم (كم)"])
    with ch2: st.area_chart(filtered_df.set_index("اسم الفندق")["الوقت مشياً (دقيقة)"])

st.markdown("---")

if is_admin:
    st.subheader("🛠️ لوحة تحكم المدير (تعديل وحذف وقراءة الرسائل والتعليقات الواردة)")
    c_form, c_edit, c_del = st.columns(3)
    with c_form:
        st.subheader("➕ إدخال فندق جديد")
        h_name = st.text_input("✍️ اسم الفندق الجديد:")
        h_district = st.text_input("📍 المنطقة / الحي:")
        h_dist = st.number_input("📏 المسافة إلى الحرم (كم):", value=1.5)
        h_time = st.number_input("⏱️ الوقت مشياً (دقيقة):", value=15)
        h_shuttle = st.selectbox("🚌 توفر حافلة نقل؟", ["نعم", "لا"])
        h_trans_type = st.text_input("🚍 نوع وسيلة النقل:")
        h_cost = st.text_input("💰 تكلفة النقل:", value="مجاني للنزلاء")
        h_schedule = st.text_input("⏰ مواعيد الخدمة:", value="على مدار 24 ساعة")
        h_station = st.text_input("🏣 موقع محطة الحافلة:")
        if st.button("💾 حفظ الفندق تلقائياً"):
            if h_name.strip() and h_district.strip():
                try:
                    geolocator = Nominatim(user_agent="makkah_hotel_locator")
                    loc = geolocator.geocode(f"{h_name}, {h_district}, Makkah")
                    lat, lon = (loc.latitude, loc.longitude) if loc else (21.4200, 39.8300)
                    row = {"اسم الفندق": h_name, "المنطقة / الحي": h_district, "المسافة إلى الحرم (كم)": h_dist, "الوقت مشياً (دقيقة)": h_time, "توفر حافلة نقل (Shuttle)": h_shuttle, "نوع وسيلة النقل": h_trans_type, "تكلفة النقل": h_cost, "مواعيد الخدمة": h_schedule, "موقع محطة الحافلة": h_station, "latitude": lat, "longitude": lon}
                    pd.DataFrame([row]).to_excel(excel_filename, index=False) if not os.path.exists(excel_filename) else pd.concat([pd.read_excel(excel_filename), pd.DataFrame([row])], ignore_index=True).to_excel(excel_filename, index=False)
                    st.success("🎉 تم حفظ الفندق الجديد بنجاح!")
                    st.rerun()
                except Exception as e: st.error(f"خطأ: {e}")
    with c_edit:
        st.subheader("🎯 تعديل موقع فندق يدوياً")
        hotel_to_update = st.selectbox("🎯 اختر الفندق لتعديل مكانه:", options=df["اسم الفندق"].unique())
        if st.button("🎯 تحديث موقع الفندق إلى النقطة المحددة"):
            cdf = pd.read_excel(excel_filename)
            cdf.loc[cdf['اسم الفندق'] == hotel_to_update, ['latitude', 'longitude']] = [clicked_lat, clicked_lon]
            cdf.to_excel(excel_filename, index=False)
            st.success("🎯 تم بنجاح تعديل الموقع ورسمه على الخريطة!")
            st.rerun()
    with c_del:
        st.subheader("🗑️ حذف فندق من القائمة")
        hotel_to_delete = st.selectbox("❌ اختر الفندق لحذفه نهائياً:", options=df["اسم الفندق"].unique())
        if st.button("🗑️ تأكيد الحذف فوراً"):
            cdf = pd.read_excel(excel_filename)
            cdf[cdf["اسم الفندق"] != hotel_to_delete].to_excel(excel_filename, index=False)
            st.error("❌ تم حذف الفندق وتحديث البيانات!")
            st.rerun()
    st.markdown("---")
    adm_col1, adm_col2 = st.columns(2)
    with adm_col1: st.subheader("💬 تعليقات وتقييمات الفنادق الواردة"); st.dataframe(load_comments(), use_container_width=True)
    with adm_col2: st.subheader("📩 رسائل واستفسارات الزوار المباشرة"); st.dataframe(load_messages(), use_container_width=True)
else:
    st.subheader("🤝 لوحة تواصل الزوار والروابط الاجتماعية الرسمية لشركة طريق الميقات")
    fb_link = "https://facebook.com"
    tiktok_link = "https://tiktok.com"
    maps_link = "https://goo.gl"
    
    link_c1, link_c2, link_c3, link_c4 = st.columns(4)
    with link_c1: st.link_button("🌐 تابعنا على صفحة فيسبوك", fb_link, use_container_width=True)
    with link_c2: st.link_button("🎵 تابعنا على حساب تيك توك", tiktok_link, use_container_width=True)
    with link_c3: st.link_button("📍 زيارة موقعنا", maps_link, use_container_width=True)
    with link_c4: 
        if st.button("👍 الإعجاب", use_container_width=True):
            st.toast("❤️ شكرًا لك على إعجابك وتثمينك لخدمات شركة طريق الميقات فرع 11 يونيو!")
            st.balloons()
            
    st.markdown("---")
    visitor_c1, visitor_c2 = st.columns(2)
    with visitor_c1:
        st.subheader("💬 إضافة تعليق ومراجعة لفندق")
        v_hotel = st.selectbox("🎯 اختر الفندق المراد تقييمه:", options=df["اسم الفندق"].unique())
        v_rating = st.select_slider("⭐ اختر تقييمك للفندق:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
        v_comment = st.text_area("✍️ اكتب مراجعتك أو تعليقك هنا:")
        if st.button("💬 نشر وإرسال التعليق فوراً", use_container_width=True):
            if v_comment.strip() == "": st.error("⚠️ فضلاً، اكتب نص تعليقك أولاً.")
            else:
                df_c = load_comments()
                new_c = {"الوقت": time.strftime("%Y-%m-%d %H:%M:%S"), "الفندق المستهدف": v_hotel, "التقييم": v_rating, "التعليق": v_comment}
                pd.concat([df_c, pd.DataFrame([new_c])], ignore_index=True).to_excel(comments_filename, index=False)
                st.success("🎉 شكرًا لك! تم تسجيل تعليقك بنجاح.")
                st.balloons()
    with visitor_c2:
        st.subheader("📩 إرسال رسالة مباشرة إلى الإدارة")
        v_name = st.text_input("✍️ اسمك الموقر (اختياري):", placeholder="مثال: زائر من ليبيا")
        v_msg = st.text_area("✉️ اكتب نص رسالتك أو استفسارك هنا:")
