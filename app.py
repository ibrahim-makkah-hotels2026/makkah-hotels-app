import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time

# إعداد واجهة الصفحة
st.set_page_config(page_title="نظام إدارة ونقل الفنادق المتكامل", layout="wide")
st.title("🏨 النظام المتكامل لإدارة وسائل نقل وفنادق الحرم المكي الشريف")

excel_filename = "hotel_transport_data_v2.xlsx"

# دالة لقراءة البيانات الحالية
def load_current_data():
    if os.path.exists(excel_filename):
        return pd.read_excel(excel_filename)
    else:
        default_hotels = [
            {"اسم الفندق": "فندق أسطورة أعمار", "المنطقة / الحي": "العزيزية", "المسافة إلى الحرم (كم)": 2.0, "الوقت مشياً (دقيقة)": 25, "توفر حافلة نقل (Shuttle)": "نعم", "نوع وسيلة النقل": "حافلات مكة العامة / ترددية", "تكلفة النقل": "مجاني للمعتمرين", "مواعيد الخدمة": "على مدار 24 ساعة", "موقع محطة الحافلة": "ساحة محبس الجن الترددية", "latitude": 21.4165, "longitude": 39.8450}
        ]
        df_init = pd.DataFrame(default_hotels)
        df_init.to_excel(excel_filename, index=False)
        return df_init

df = load_current_data()

# --- شريط البحث والتصفية الجانبي ---
st.sidebar.header("🔍 خيارات البحث والتصفية")
search_query = st.sidebar.text_input("ابحث باسم الفندق:")
selected_district = st.sidebar.multiselect("تصفية حسب الحي/المنطقة:", options=df["المنطقة / الحي"].unique())
max_distance = st.sidebar.slider("أقصى مسافة عن الحرم (كم):", 0.0, 5.0, 5.0, 0.1)
shuttle_only = st.sidebar.checkbox("عرض الفنادق التي توفر حافلات نقل فقط")

# تطبيق الفلاتر
filtered_df = df[df['المسافة إلى الحرم (كم)'] <= max_distance]
if search_query:
    filtered_df = filtered_df[filtered_df['اسم الفندق'].str.contains(search_query, case=False, na=False)]
if selected_district:
    filtered_df = filtered_df[filtered_df['المنطقة / الحي'].isin(selected_district)]
if shuttle_only:
    filtered_df = filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']

# عرض الإحصائيات في الأعلى
col1, col2, col3 = st.columns(3)
col1.metric("📊 إجمالي الفنادق المعروضة", len(filtered_df))
if not filtered_df.empty:
    col2.metric("📍 أقرب فندق متاح", f"{filtered_df['المسافة إلى الحرم (كم)'].min()} كم")
    col3.metric("🚌 فنادق توفر حافلات", len(filtered_df[filtered_df['توفر حافلة نقل (Shuttle)'] == 'نعم']))

# --- القسم التفاعلي الرئيسي (الجدول والخريطة) ---
col_table, col_map = st.columns(2)

with col_table:
    st.subheader("📋 جدول الفنادق المتاحة وتفاصيل النقل")
    st.dataframe(filtered_df, use_container_width=True, height=400)

with col_map:
    st.subheader("🗺️ الخريطة الجغرافية التفاعلية حية")
    st.info("💡 ميزة ذكية: اضغط بالفأرة على أي مكان بالخريطة لتحديد الإحداثيات وتعديل موقع الفندق بالأسفل يدوياً!")
    haram_lat, haram_lon = 21.4225, 39.8262
    m = folium.Map(location=[haram_lat, haram_lon], zoom_start=14, tiles="OpenStreetMap")
    folium.Marker([haram_lat, haram_lon], popup="🕌 المسجد الحرام", tooltip="المسجد الحرام", icon=folium.Icon(color="darkpurple", icon="home", prefix="fa")).add_to(m)
    folium.Circle(radius=3000, location=[haram_lat, haram_lon], color="blue", fill=True, fill_color="cyan", fill_opacity=0.08, dash_array="5, 5").add_to(m)
    
    for idx, row in filtered_df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            # ✨ تم تصحيح الكلمة هنا بدقة لمنع الخطأ
            marker_color = "green" if row['توفر حافلة نقل (Shuttle)'] == "نعم" else "orange"
            popup_text = f"<b>{row['اسم الفندق']}</b><br>المسافة: {row['المسافة إلى الحرم (كم)']} كم"
            folium.Marker([row['latitude'], row['longitude']], popup=popup_text, tooltip=row['اسم الفندق'], icon=folium.Icon(color=marker_color, icon="info-sign")).add_to(m)
            
    map_data = st_folium(m, width=600, height=400, returned_objects=["last_clicked"])

clicked_lat = map_data["last_clicked"]["lat"] if map_data and map_data.get("last_clicked") else 21.4082
clicked_lon = map_data["last_clicked"]["lng"] if map_data and map_data.get("last_clicked") else 39.8239

# --- 📊 ميزة الرسوم البيانية التفاعلية للمقارنة البصرية ---
st.markdown("---")
st.subheader("📊 مقارنة بصرية ذكية بين الفنادق")

if not filtered_df.empty:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("🧱 **المسافة الدقيقة إلى الحرم (بالكيلومتر):**")
        st.bar_chart(filtered_df.set_index("اسم الفندق")["المسافة إلى الحرم (كم)"])
        
    with chart_col2:
        st.write("⏱️ **الوقت التقريبي المستغرق مشياً (بالدقائق):**")
        st.area_chart(filtered_df.set_index("اسم الفندق")["الوقت مشياً (دقيقة)"])
else:
    st.info("لا توجد بيانات كافية لعرض الرسوم البيانية.")

st.markdown("---")

# تقسيم الأقسام السفلية الثلاثة: الإدخال، التعديل اليدوي، والحذف
col_form, col_edit, col_delete = st.columns(3)

with col_form:
    st.subheader("➕ إدخال فندق جديد")
    h_name = st.text_input("✍️ اسم الفندق الجديد:", placeholder="مثال: فندق فوكو مكة")
    h_district = st.text_input("📍 المنطقة / الحي بمكة المكرمة:", placeholder="مثال: المسفلة")
    h_dist = st.number_input("📏 المسافة إلى الحرم (كم):", min_value=0.0, max_value=20.0, step=0.1, value=1.3)
    h_time = st.number_input("⏱️ الوقت مشياً (دقيقة):", min_value=0, max_value=120, step=1, value=18)
    h_shuttle = st.selectbox("🚌 توفر حافلة نقل (Shuttle)؟", ["نعم", "لا"])
    h_trans_type = st.text_input("🚍 نوع وسيلة النقل:", placeholder="مثال: حافلات ترددية خاصة")
    h_cost = st.text_input("💰 تكلفة النقل:", value="مجاني للنزلاء")
    h_schedule = st.text_input("⏰ مواعيد الخدمة:", value="على مدار 24 ساعة")
    h_station = st.text_input("🏣 موقع محطة الحافلة:", placeholder="مثال: أمام البرج الرئيسي")

    if st.button("💾 حفظ وتحديد الموقع تلقائياً", use_container_width=True):
        if h_name.strip() == "" or h_district.strip() == "":
            st.error("⚠️ فضلاً، يرجى كتابة اسم الفندق والحي بدقة.")
        else:
            with st.spinner("🔍 جاري تحديد الموقع الجغرافي وحفظ البيانات..."):
                try:
                    geolocator = Nominatim(user_agent="makkah_hotel_locator")
                    search_query_geo = f"{h_name}, {h_district}, Makkah, Saudi Arabia"
                    location = geolocator.geocode(search_query_geo)
                    if location is None:
                        location = geolocator.geocode(f"{h_district}, Makkah, Saudi Arabia")
                    resolved_lat, resolved_lon = (location.latitude, location.longitude) if location else (21.4200, 39.8300)
                    
                    row_to_add = {
                        "اسم الفندق": h_name, "المنطقة / الحي": h_district, "المسافة إلى الحرم (كم)": h_dist,
                        "الوقت مشياً (دقيقة)": h_time, "توفر حافلة نقل (Shuttle)": h_shuttle, "نوع وسيلة النقل": h_trans_type,
                        "تكلفة النقل": h_cost, "مواعيد الخدمة": h_schedule, "موقع محطة الحافلة": h_station,
                        "latitude": resolved_lat, "longitude": resolved_lon
                    }
                    current_df = pd.read_excel(excel_filename)
                    updated_df = pd.concat([current_df, pd.DataFrame([row_to_add])], ignore_index=True)
                    updated_df.to_excel(excel_filename, index=False)
                    st.success(f"🎉 تم رصد وحفظ فندق '{h_name}' بنجاح!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

with col_edit:
    st.subheader("🎯 تعديل موقع فندق يدوياً")
    st.info("قم بالضغط على مكان الفندق الصحيح على الخريطة بالأعلى أولاً، ثم اختر الفندق واضغط تحديث الموقع.")
    hotel_to_update = st.selectbox("🎯 اختر الفندق المراد تعديل مكانه:", options=df["اسم الفندق"].unique(), key="edit_select")
    st.caption(f"📍 خط العرض الملتقط: {clicked_lat:.4f}")
    st.caption(f"📍 خط الطول الملتقط: {clicked_lon:.4f}")
    
    if st.button("🎯 تحديث موقع الفندق إلى النقطة المحددة", use_container_width=True):
        current_df = pd.read_excel(excel_filename)
        current_df.loc[current_df['اسم الفندق'] == hotel_to_update, ['latitude', 'longitude']] = [clicked_lat, clicked_lon]
        current_df.to_excel(excel_filename, index=False)
        st.success(f"🎯 تم بنجاح نقل موقع فندق '{hotel_to_update}' وتحديث الإكسيل!")
        time.sleep(1)
        st.rerun()

with col_delete:
    st.subheader("🗑️ حذف فندق من القائمة")
    st.warning("⚠️ حذف الفندق سيمسحه نهائياً من ملف الـ Excel ومن على الخريطة.")
    hotel_to_delete = st.selectbox("❌ اختر الفندق المراد حذفه نهائياً:", options=df["اسم الفندق"].unique(), key="del_select")
    
    if st.button("🗑️ تأكيد حذف الفندق ومسحه فوراً", use_container_width=True):
        updated_df = df[df["اسم الفندق"] != hotel_to_delete]
        updated_df.to_excel(excel_filename, index=False)
        st.error(f"❌ تم حذف فندق '{hotel_to_delete}' نهائياً وتحديث الخريطة!")
        time.sleep(1)
        st.rerun()

# شريط جانبي لتحميل الجدول للنسخ الاحتياطي
st.sidebar.markdown("---")
st.sidebar.subheader("📥 تحميل ملف البيانات")
with open(excel_filename, "rb") as file:
    st.sidebar.download_button(
        label="تنزيل جدول الفنادق كملف Excel", data=file, file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
