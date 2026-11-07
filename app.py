import streamlit as st
import pandas as pd
import os
import time
import urllib.parse
from PIL import Image

# 🕋 إعداد واجهة الصفحة
st.set_page_config(page_title="دليل المعتمر - نظام إدارة ونقل الفنادق المتكامل", page_icon="🕋", layout="wide")

# 🔒 جدار الأمان الذكي وحماية قوية جداً
st.markdown("<style>#MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} header {visibility: hidden !important;} .viewerBadge_container__16S6S {display: none !important;} stDeployButton {display: none !important;} button[title='View source code'] {display: none !important;} a[href*='github.com'] {display: none !important;}</style>", unsafe_allow_html=True)

excel_filename = "makkah_madinah_full_hotels_v22.xlsx"
comments_filename = "visitor_comments_database_v22.xlsx"
bookings_filename = "visitor_bookings_database_v22.xlsx"
suggestions_filename = "visitor_suggestions_database_v22.xlsx"
subscribers_filename = "subscribers_database_v22.xlsx"
admin_messages_filename = "admin_messages_database_v22.xlsx"
stats_filename = "visitor_stats_v22.txt"
notice_filename = "admin_notice_v22.txt"

# عداد الزوار الحقيقي للأدمن
def track_visitor():
    try:
        visits = 0
        if os.path.exists(stats_filename):
            with open(stats_filename, "r") as f:
                visits = int(f.read().strip())
        visits += 1
        with open(stats_filename, "w") as f:
            f.write(str(visits))
        return visits
    except:
        return 1

real_visits = track_visitor()
current_usd_rate = 9.92

def get_admin_notice():
    if os.path.exists(notice_filename):
        try:
            with open(notice_filename, "r", encoding="utf-8") as f:
                return f.read()
        except:
            pass
    return "⏳ تذكير عاجل: متبقي مقاعد محدودة جداً على رحلة العمرة القادمة! احجز مقعدك الآن قبل اكتمال العدد."

def save_admin_notice(text):
    with open(notice_filename, "w", encoding="utf-8") as f:
        f.write(text)

def load_admin_messages():
    return pd.read_excel(admin_messages_filename) if os.path.exists(admin_messages_filename) else pd.DataFrame(columns=["الوقت", "البريد / الاسم", "نص الرسالة"])

# 📢 شريط الإعلان والتذكير العاجل
st.markdown("""
<div style="background-color: #1e3d59; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 10px;">
    🌙 عروض و رحلات العمرة متوفرة بأفضل الأسعار - دليل المعتمر الشامل
</div>
""", unsafe_allow_html=True)

current_notice = get_admin_notice()
st.markdown(f"""
<div style="background-color: #d9534f; color: white; padding: 8px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 15px; margin-bottom: 15px;">
    {current_notice}
</div>
""", unsafe_allow_html=True)

# 📊 قاعدة البيانات الشاملة للفنادق
def get_all_makkah_hotels():
    primary_hotels = [
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
    
    additional_hotels = [
        "فندق أراك الشريعة أجياد", "فندق دار الفائزين", "فندق الجاد محبس", "فندق قصر العزيزية", "فندق مكارم مِنى", "فندق إيلاف بكة", 
        "فندق سرايا الضيافة", "فندق دار الريس", "فندق عبير العزيزية", "فندق بركة برهان", "فندق التوفيق بلازا", "فندق مكارم أم القرى", 
        "فندق البستان الماسي", "فندق ريف العالمية", "فندق الشهباء مكة", "روابي السلام", "واحة الضيافة مكة", "فندق امجاد الضيافة", 
        "فندق الماسة بدر", "فندق أنوار الضيافة", "إعمار جراند", "فندق رويال المشاعر", "فندق الظل", "فندق ندى الضيافة", "فندق سما الضيافة", 
        "فندق العليان بلازا", "فندق مكة العزيزية", "فندق أوان مكة", "مكة هيلتون للأجنحة، جبل عمر", "فندق البركة مودة", "فندق فلسطين مكة", 
        "فندق رياض الضيافة", "فندق إنفينيتي مكة", "فندق ديار الضيافة", "فندق مكة", "فندق النسيم مودة", "فندق ومسكن إقامة موفنبيك برج هاجر مكة", 
        "فندق لو مريديان مكة المكرمة", "فندق درة منى", "فندق إيلاف كندة", "قصر الفيحاء المحبس", "فندق عفراء", "فندق أزكى الصفا", 
        "رزانا الروضة", "منارات غزة", "Al Rawda Hotel", "فندق كونكورد مكة", "إم هوتل مكة باي ميلينيوم", "فندق باب الملتزم كونكورد", 
        "فندق كونكورد مِنى", "فندق رفاف السلطان", "فندق الرفاع السد", "فندق روضة البيت أجياد", "فندق برج الضيافة", "فندق رفاف الحياة", 
        "كيونا العزيزية", "فندق لمار اجياد الأول - برج أ", "فندق بارك إن من راديسون مكة النسيم", "فندق جوهرة العدل", "فندق سنود العظمة", 
        "فندق كيونا الهجرة", "فندق بكة الصلاح مكة المكرمة", "فندق ومركز مؤتمرات هيلتون مكة", "فندق الروح الحرة", "فندق مجد المهاجرين", 
        "فندق الروحانية", "فندق إعمار الخليل", "فندق ديار المشاعر الفندقية", "فندق الأرض المتميزة 1، مكة", "سنود العزيزية", 
        "فندق مباني المستقبل", "فندق مآثر الجوار", "الأصيل رفادة", "فندق لمار اجياد الأول برج ب", "تلال جبل الكعبة", "فندق المزن المتألقة", 
        "فندق بلو كورال", "فندق إم الدانة مكة من ميلينيوم", "فندق الصفوة البرج 1", "فندق ميزاب الضيافة", "فندق بويتك الجود مكة", 
        "فندق البيرق", "فور بوينتس باي شيراتون مكة النسيم", "فندق أبراج الكسوة", "فندق إشراق أجياد", "Al Olyan Golden Hotel", 
        "نور منازل الكرام", "بتول أجياد", "فندق الروضة المكية", "فندق أجواد أجياد", "فندق أبراج الهداية", "فندق بياب العزيزية", 
        "فندق فيوليت العزيزية", "ألماسه الروضة", "فندق قصر رفان", "بارك إن باي راديسون مكة المكرمة العزيزية", "فندق فوكو مكة المكرمة", 
        "دبل تري من هيلتون مكة جبل عمر", "ميلينيوم مكة النسيم", "فندق سنود الريان", "فندق العليان الماسي", "فندق الرفاع ريع بخش", 
        "فندق كرم الرفاع", "عروق الذهب المكية 2", "رهف المشاعر", "فندق فيوليت الششة", "فندق حياة الضيافة", "هوتل 21", "فندق واحة الرفاع", 
        "رمادا زاد التيسير من ويندهام، مكة المكرمة", "دبل تري من هيلتون مكة المكرمة، العزيزية", "فندق نسمات مكة", "فندق سفير المسك", 
        "فندق عبير الضيافة", "انوار المشاعر", "فندق كوبثورن مكة النسيم", "فندق البلد الطيب أجياد", "رمادا من ويندهام، مكة المكرمة زاد الروضة", 
        "قصر العليان", "إعمار وورث إيليت", "فندق لمار البيت", "فندق آفاق المشاعر", "بيست ويسترن أجياد مكة المكرمة", "ميره أجياد", 
        "فندق نور الثريا", "فندق زوار البيت", "فندق جراند الماسة", "فندق مناير الأصول", "فندق نرجس الحديقة", "فندق ساري منى", 
        "فندق زهرة السعد ٣", "فندق الفجر البديع 1", "فرسان أجياد", "فندق مونتانا العزيزية", "فندق زهرة السعد 4", "نوفوتيل مكة ذاخر سيتي", 
        "فندق حياة مكارم اجياد", "فندق روتس", "فندق أبراج الجنادرية", "فندق أعمدة الذهب", "فندق المقام بكة", "صفوة أجياد 2", 
        "فندق سيوف الشهداء", "زهرة السعد 5", "فندق زوار المشاعر القصر", "فندق الفجر البديع 6", "دار المقام", "العنوان جبل عمر، مكة", 
        "فندق نسمات الخير", "فندق زهرة السعد 6", "فندق سنود أجياد البرج 1", "فندق سنود الدانه", "الجميرة، جبل عمر، مكة المكرمة", 
        "فندق ديار المكارم 1", "فندق واحة المسك", "فندق الكرام", "رواء العزيزية", "فندق أبراج الريان", "فندق سما المسك", "إعمار ليجيند", 
        "فندق لؤلؤة البدائع", "شعيل إن مكة", "ميسان المشاعر", "فندق الإباء", "فندق سما الأماني", "فندق اسكنت الحفاير", "سنت العزيزية", 
        "أوبن هوتل", "فندق ماسة المجد", "فندق أبراج نوازي", "فيفيان الجميزه", "فندق سنت الخير", "فندق بيوت الجزيرة", "فندق سويتس المقام", 
        "إعمار المنار", "فندق أوتاد المتحدة العزيزية", "ورقان النور، تابيستري كوليكشن من هيلتون", "إعمار إنترناشونال", "مسارات المشاعر", 
        "فندق أعيان جالف", "فندق إعمار إيليت", "فندق أبراج المسك", "Manazel Al Zaireen", "فندق مسك أم القرى", "فندق سرايا المسك", 
        "فندق أسطورة إعمار", "جوري المشاعر", "اعمار افاق السد", "فندق ثري بيرلز مصلي، مكة المكرمة", "فندق درة البيان", "فندق لؤلؤة الإيمان", 
        "كوثر البركة", "فندق قصر رزق", "إعمار أندلسية", "فندق برج الضيافة المبارك", "فندق ورث إيليت", "فندق الصفوة البرج 3", "فندق أرائك الخلود", 
        "فندق سما سول للشقق", "فندق مكارم النخيل", "فندق صلة البيت", "مسرات رويال", "فندق موطن سنود", "فندق عصفور 4", "فندق أسكنت الذهبية", 
        "بودل أجياد", "فندق وأجنحة تايم روبا", "فندق نما مودة", "فندق نجمة الأبرار", "فندق منارة الكرام", "شموخ المقام", "فندق الفجر البديع 5", 
        "بارك إن من راديسون، مكة ذاخر الشرقي", "فندق ندى المجد", "فندق قصر السحاب مكة المكرمة", "فندق نور منازل الكرام", "فندق إهداء، مكة المكرمة", 
        "فندق ياسمين المجد", "فندق كنان العزيزية مكة المكرمة", "فندق رضوان الضيافة", "ميركيور مكة المكرمة، العزيزية", "فندق نور الصلاح", 
        "فندق ذوق الخيال", "فندق سيف المجد", "فندق كابيتال جيست العزيزية الجنوبية", "فندق جوهرة المجد", "فندق رشد المجد", "فندق ميعاد المجد", 
        "نسور اجياد", "فندق لؤلؤة العنود مكة", "فندق جادة الخليل", "فندق سدرا مكة", "فندق ديار الخالدية", "درة الصلاح", "فندق وسد مكة المكرمة", 
        "دار لامار", "فندق ضيوف المقام للغرف والشقق المفروشة", "فندق روحة المقام", "فندق الدرع", "فندق عنان من سنود", "فندق سنود الهدى", 
        "فندق سنود المروة", "سجى باى ورويك مكة هوتل", "فندق جولدن هوسبيتاليتي", "فندق سدير كرم", "اهداء الوسام", "منارة المشاعر", 
        "فندق الكنارى ان", "فندق أسكنت العزيزية", "فندق قرطبة العزيزية 2", "فندق قرطبة العزيزية", "كدي تاور 1", "الايام أجياد", 
        "فندق مكارم الهجرة", "فندق سما المقام", "بارك إن من راديسون، مكة ذاخر الغربي", "فندق الرابح", "ظلال النزلاء", "كورت يارد من ماريوت مكة", 
        "فندق إيلاف قنوان", "فندق زهرة اللافندر", "سنود البركة", "فندق وفاق المشاعر", "فندق ميسان المقام", "ميسان الملتزم المحبس", 
        "فندق البراق الماسي", "فندق اخيار المحبس", "فندق مزايا", "رتاج الحياة", "فندق الجابري", "أويو 403 هدايه تاور هوتل", "فندق ودام 3 العزيزية", 
        "العزيزية الذهبية", "فندق الخلفاء الماسي", "درة بيسان", "فندق مهد الرسالة 3", "فندق مهد الرسالة 1", "فندق ماسة المشاعر", 
        "فندق أسكن التيسير", "فندق مقام الحجاز", "فندق كونكريت السحاب، مكة المكرمة", "فندق ملتقي الإيمان للضيافة السياحي", "فندق ملتقى الايمان 2", 
        "فندق الهندباء", "فندق حسين بياري", "فندق وفاق الساحة", "فندق وفاق النزهة", "فندق جوري الهدا", "فندق ابراج التيسير طوى", 
        "فندق نوفوتيل ريزيدنسز مكة المكرمة", "فندق ضيافة رفيف", "فندق تاج الذهبية", "فندق نيو ليفل - الشيشة", "فندق غيدا الشيشة", 
        "بول بيرل هوتل", "فندق وحدة الخير", "كنانة العزيزية", "فندق وردة المعابدة", "فندق ليدن", "سيف بلس", "سيف بلس 2", 
        "فندق ميدان البيت", "فندق الأيام إيليت", "فندق الخلفاء الفضي", "الخلفاء+الفيصلية", "فندق اتقان المشاعر", "درة الجوار", 
        "فندق بارادايس نيس - المحبس", "فندق الراقي المميز", "فندق رفاده الذهبية", "فندق رواء السعادة", "فندق رواء المكارم", "فندق مدن الخير", 
        "فندق ديمورا", "فندق اكليل الضيافه", "فندق نخبة الجوار، مكة المكرمة من مورو", "فندق برج الهاشمية مكة المكرمة", "ساري الروابي هوتل", 
        "كوثر الحياة هوتل", "فندق ياقوتة الطلائع", "فندق دفلى", "فندق قاصد الخير", "فندق كنوز العنود مكة المكرمة", "رزانه الحفاير", 
        "كودي تاور 2", "فيفيان الجميزة", "نسمات الخير هوتل", "كنف هوتل (الشرائع)", "فندق مسارات المحبس", "شرفة الطلائع هوتل", 
        "فندق جولدن بارون", "فندق ميزاب الروضة", "فندق القمة", "كرمك هوتل مكة", "فندق جايدن مسار", "فندق أجم مينا", "فندق النسيم", 
        "فندق التوفيق في العزيزية", "برج الجميزة", "أسكن الماسي 1", "فندق أصيل المسك", "فندق أريج الذهبي مكة", "فندق لؤلؤة النزهة", 
        "فنادق ميلا مكة", "فندق نيوليفيل - بطحاء قريش", "رفاهية المشاعر", "فندق رفاهية الستين", "روضة ميار", "فندق سرايا عبير مكة المكرمة", 
        "فندق فيرتا الششة مكة المكرمة", "روتانا جبل عمر مكة", "فندق شموخ الشعلة", "بارك بلازا هوتل", "نزلي المعابدة هوتل", 
        "فندق جواهر البيت 2 مكة المكرمة", "فندق مورو العالمية مكة المكرمة", "فندق سما أجياد، مكة", "فندق لاند مارك داركم مكة المكرمة", 
        "فندق منازل العين أجياد", "فندق ميرة الروضة مكة المكرمة", "فندق ميرة الشعب مكة المكرمة", "فندق مناسك البيت مكة المكرمة", "فندق الأصول الماسية", "فندق أبراج الفارابي", "فندق الرسالة الماسي", "الزائر المتميز أجياد", "المقام الذهبي", "فندق كنانة العزيزية", 
        "برج الصافات", "ريحانة المكان", "سيف بلص 3", "فندق فيرتا المحبس", "وحدة التيسير", "فندق زاد المشاعر", "فندق ميزاب الخير", 
        "شركة سرايا عبير للفنادق", "فندق غزالة بيوتيفل", "فندق لؤلؤة أجياد", "فندق لؤلؤة الغوار", "فندق طريق الهجرة", "فندق بلورة الدرة", 
        "فندق أصول الجوهرة", "فندق جراند الشهباء الكعكية", "Hotel Alshahba Alazizia", "فندق أوتاد المتحدة 4 الروضة", "فندق البلاد اثنين 1 مكة", 
        "فندق البلاد اثنين 2 مكة", "فندق الفارابي", "فندق العليان الذهبي المسفلة", "فندق الرفاع العزيزية مكة المكرمة", "فندق الوافدين", 
        "شركة أبراج حفاوة الفندقية", "فندق الأرض المتميزة", "فندق الأولين حياة", "فندق طريق الحياة", "فندق المجد", "فندق العرابي", 
        "الريادة جراند", "فندق السكرية", "فندق أمل المشاعر", "فندق عملاق المشرق", "فندق أركان المطاف", "عصفور هوتل 01", "عصفور هوتل 02", 
        "فندق برادايس لاند", "فندق بلال", "فندق برج فرح", "فندق سنت العزيزية مكة المكرمة", "ضيف العزيزية", "فندق ديمورا العزيزية", 
        "فندق جراند جواهر الهاشمية، مكة المكرمة", "فندق إيليت المشاعر", "فندق مدينة الزهراء", "فندق توحيد الأصالة", "فندق جواهر الهاشمية 6", 
        "جوهرة الديار - 1", "جوهرة المحبة", "فندق جوهرة الصلاح مكة", "فندق كيان الراية مكة المكرمة", "فندق لؤلؤة المسك", "فندق منار الأزهر", 
        "منارة المنى-2", "منارة العزيزية-3", "فندق منارة العزيزية", "فندق منارة المسك", "فندق منازل الزائرين الهدا", "فندق مشرب رواء المنصور", 
        "فندق مواكب الكوثر مكة", "مواسم الاحسان هوتل", "فندق ميرة السد مكة المكرمة", "فندق ميرة النفق، مكة المكرمة", "فندق مورو العالمية الذهبي - العزيزية", 
        "مرجان المشاعر", "العليان الفضي", "فندق أورفانا العتيبية", "فندق أويس", "فندق رومانس روم", "فندق رواء ليندي مكة", "رواء مكارم", 
        "سيف بلص 1", "فندق سكب الأصيل", "شمس الذهبي", "فندق تارا المحبس", "فندق تارا الياسمين", "فندق واحة الرفاع مكة المكرمة", "فندق يمام 2", 
        "فندق فجر النسك أجياد", "فندق كرم مضياف", "فندق ساحة النزهة", "فندق دار أم القرى الذهبي", "شقق ريكاز المخدومة", "فندق نبراس الهدى",
        "فندق دار الإيمان إنتركونتيننتال", "فندق الأمين كروم", "فندق رويال إن الروضة", "فندق ميلينيوم العقيق المدينة",
        "فندق ليدر المنى كريم", "فندق كراون بلازا المدينة", "فندق دلة طيبة", "فندق الحرم – الروضة", "فندق موفنبيك المدينة", "فندق جوار السقيفة",
        "فندق الساحة – الروضة", "فندق مجلس غراند ميركيور المدينة", "فندق الإيمان رويال", "فندق الإيمان طيبة", "فندق لو ميريديان المدينة",
        "فندق صن رايز المدينة المنورة", "فندق هوليداي فيلا المدينة", "أجنحة طيبة أراك", "رويال ان النخبة", "فندق نزل رويال إن",
        "فندق جولدن توليب المكتان", "فندق غراند الاندلس", "فندق سرايا طابة", "فندق حياة انترناشونال المدينة", "فندق نزل الشاكرين",
        "فندق زوار انترناشيونال", "فندق سفراء الهدى", "فندق دار النعيم", "فندق الإيمان القبلة", "فندق مودة الصفوة", "فندق مودة الواحة",
        "فندق الصالحية الذهبى", "فندق مراج طيبه", "فندق الإيمان أحد", "فندق روتانا المسك", "فندق إيلاف طيبة", "رويال أمجاد السلام", "فندق العليان",
        "الفيروز الماسي (فندق جلوريا المدينة)", "فندق ماريوت المدينة", "فندق وكن الحرم النبوي", "فندق العقيق آراك",
        "فندق ديار انترناشونال", "فندق المني كريم راديسون بلو المدينة", "فندق رويال ديار", "فندق المدينة أراماس", "فندق روضة مبارك", "فندق الإشراق",
        "فندق الوسام", "فندق زهرة مبارك", "فندق أريس الجوار", "فندق رمادا", "فندق ديار المدينة", "فندق روضة الأمل", "فندق زمرد قرطاج",
        "فندق وصل الذهبي", "فندق البديع شركة إلياس", "فندق السرايا المدينة", "فندق وصل الريم", "فندق الصافية إلياس", "فندق برج الأمل",
        "فندق المنارة كروم", "فندق الشرق", "فندق الصافي هلا", "فندق الدار", "قصر الخليل الشاكرين", "فندق مودة النور", "فندق الشهباء",
        "فندق الأندلس دار الخير", "فندق ارماس", "فندق الهدى منازلي", "فندق مكارم المدينة الذهبي", "فندق بدر العوالي"
    ]

    data = []
    profit_margin = 200.0
    for name, area, d_val, base_price in primary_hotels:
        lyd_base = round(base_price * current_usd_rate, 2)
        final_price_lyd = round(lyd_base + profit_margin, 2)
        maps_query = urllib.parse.quote(f"{name} مكة المكرمة")
        map_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        
        data.append({
            "اسم الفندق": name,
            "المنطقة / الحي": area,
            "المسافة إلى الحرم (كم)": d_val,
            "السعر الأساسي ($)": base_price,
            "سعر الحجز النهائي (د.ل)": final_price_lyd,
            "توفر حافلة نقل (Shuttle)": "لا" if d_val <= 0.8 else "نعم",
            "موقع الفندق على خرائط جوجل": map_link
        })

    for idx, name in enumerate(additional_hotels):
        d_val = round(1.0 + ((idx % 35) * 0.1), 2)
        base_price = round(35 + (idx % 40), 2)
        lyd_base = round(base_price * current_usd_rate, 2)
        final_price_lyd = round(lyd_base + profit_margin, 2)
        
        is_madinah = any(word in name for word in ["المدينة", "طيبة", "الروضة", "أنوار", "أوبروى", "أمجاد", "الحرم"])
        city_keyword = "المدينة المنورة" if is_madinah else "مكة المكرمة"
        maps_query = urllib.parse.quote(f"{name} {city_keyword}")
        map_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        
        data.append({
            "اسم الفندق": name,
            "المنطقة / الحي": "المنطقة المركزية (المدينة)" if is_madinah else "مكة المكرمة (العزيزية/أجياد/المسفلة)",
            "المسافة إلى الحرم (كم)": d_val,
            "السعر الأساسي ($)": base_price,
            "سعر الحجز النهائي (د.ل)": final_price_lyd,
            "توفر حافلة نقل (Shuttle)": "نعم",
            "موقع الفندق على خرائط جوجل": map_link
        })
    return data

def get_flights_data():
    flights = [
        ("طرابلس (TIP) -> جدة (JED)", "الخطوط الجوية الأفريقية", "مباشر", "2,850 د.ل"),
        ("بنغازي (BEN) -> جدة (JED)", "الخطوط الجوية الليبية", "مباشر", "2,750 د.ل"),
        ("طرابلس (TIP) -> المدينة المنورة (MED)", "خطوط الطيران التركية", "ترانزيت إسطنبول", "3,400 د.ل"),
        ("مصراتة (MRA) -> جدة (JED)", "الخطوط الأفريقية", "مباشر", "2,800 د.ل")
    ]
    return pd.DataFrame(flights, columns=["خط السير", "شركة الطيران", "نوع الرحلة", "سعر التذكرة المبدئي"])

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
    return pd.read_excel(comments_filename) if os.path.exists(comments_filename) else pd.DataFrame(columns=["الوقت", "اسم الزائر", "الفندق المستهدف", "التقييم (من 5)", "التعليق"])

def load_bookings():
    return pd.read_excel(bookings_filename) if os.path.exists(bookings_filename) else pd.DataFrame(columns=["الوقت", "اسم المعتمر", "رقم الهاتف", "نوع الغرفة", "الفندق المطلوبة", "عدد الأيام", "إجمالي السعر (د.ل)", "حالة الطلب"])

def load_suggestions():
    return pd.read_excel(suggestions_filename) if os.path.exists(suggestions_filename) else pd.DataFrame(columns=["الوقت", "اسم المقترح", "نوع المقترح", "التفاصيل والتعديلات", "مسار الصورة"])

def load_subscribers():
    return pd.read_excel(subscribers_filename) if os.path.exists(subscribers_filename) else pd.DataFrame(columns=["الوقت", "البريد الإلكتروني"])

df = load_current_data()
df_flights = get_flights_data()

# --- 🔐 لوحة الإدارة والدخول ---
st.header("🔐 دخول الإدارة والتحكم في النظام")
if "logged_in" not in st.session_state: 
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    st.success("✓ وضع المدير نشط (صلاحيات كاملة للتحكم في الإعلانات، الأسعار، مراجعة مقترحات الزوار ورسائل الإدارة)")
    
    st.markdown(f"📊 **إحصائيات الزيارات الحقيقية للموقع:** {real_visits} زيارة")

    st.markdown("### 📝 تحديث نص التذكير العاجل:")
    new_notice_input = st.text_input("نص التذكير العاجل:", value=current_notice)
    if st.button("حفظ التذكير"):
        save_admin_notice(new_notice_input)
        st.success("تم التحديث!")
        st.rerun()

    if st.button("🔒 تسجيل الخروج", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
else:
    admin_password = st.text_input("✍️ أدخل كلمة مرور المدير:", type="password")
    if admin_password == "1234": 
        st.session_state["logged_in"] = True
        st.rerun()

st.markdown("---")

# العداد التحفيزي للزوار (يزداد تلقائياً كل دقيقتين وهمياً كنوع من التحفيز)
if "visitor_count_display" not in st.session_state:
    st.session_state["visitor_count_display"] = 1000
    st.session_state["last_update_time"] = time.time()

current_t_val = time.time()
if current_t_val - st.session_state["last_update_time"] > 120: # كل دقيقتين
    st.session_state["visitor_count_display"] += 100
    st.session_state["last_update_time"] = current_t_val

st.info(f"👥 إجمالي عدد زيارات الموقع حتى الآن: **{st.session_state['visitor_count_display']}**")

# التسجيل بالبريد الإلكتروني فقط
with st.expander("🔔 التسجيل في الموقع لتلقي التنبيهات والتحديثات الفورية"):
    with st.form("sub_form_email"):
        sub_email = st.text_input("البريد الإلكتروني فقط:")
        submit_sub = st.form_submit_button("اشتراك في التنبيهات")
        if submit_sub:
            if "@" in sub_email:
                df_sub = load_subscribers()
                new_sub = {"الوقت": time.strftime("%Y-%m-%d %H:%M:%S"), "البريد الإلكتروني": sub_email}
                pd.concat([df_sub, pd.DataFrame([new_sub])], ignore_index=True).to_excel(subscribers_filename, index=False)
                st.success("🎉 تم تسجيل بريدك بنجاح لتلقي التنبيهات!")
            else:
                st.error("⚠️ يرجى إدخال بريد إلكتروني صحيح.")

st.markdown("---")

# --- 🧮 حاسبة المسافة والعملات ---
st.subheader("🧮 حاسبة المسافة من الفندق إلى الحرم ومحول العملات اللحظي")

calc_c1, calc_c2, calc_c3 = st.columns(3)

with calc_c1:
    st.write("🏨 **اختر الفندق لمعرفة المسافة والوقت:**")
    selected_hotel_calc = st.selectbox("اختر الفندق:", options=df["اسم الفندق"].unique() if "اسم الفندق" in df.columns else [], key="hotel_calc_box")
    hotel_match = df[df["اسم الفندق"] == selected_hotel_calc]
    if not hotel_match.empty:
        dist_val = hotel_match["المسافة إلى الحرم (كم)"].values[0]
        map_url = hotel_match["موقع الفندق على خرائط جوجل"].values[0]
        st.success(f"📏 المسافة: **{dist_val} كم**")
        st.success(f"⏱️ الوقت المتوقع مشياً: **{int(dist_val * 12)} دقيقة**")
        st.markdown(f"[🗺️ فتح الموقع في خرائط جوجل للحرم]({map_url})", unsafe_allow_html=True)

with calc_c2:
    st.write("🗺️ **الملاحة السريعة العامة:**")
    st.write("")
    maps_direct_link = "https://www.google.com/maps/search/?api=1&query=%D8%A7%D9%84%D9%85%D8%B3%D8%AC%D8%AF+%D8%A7%D9%84%D8%AD%D8%B1%D8%A7%D9%85+%D9%85%D9%83%D8%A9"
    st.markdown(f"[🗺️ فتح الحرم المكي في الخرائط]({maps_direct_link})", unsafe_allow_html=True)

with calc_c3:
    st.write("💱 **محول سعر الصرف اللحظي:**")
    usd_input = st.number_input("أدخل المبلغ بالدولار ($):", min_value=1, max_value=10000, value=100)
    converted_lyd = round(usd_input * current_usd_rate, 2)
    st.info(f"💵 القيمة (سعر السوق السوداء {current_usd_rate}): **{converted_lyd} د.ل**")

st.markdown("---")

# --- 🧳 دليل المعتمر الشامل ---
st.header("🧳 دليل المعتمر الشامل - الاستفسارات والتعليمات")

guide_tabs = st.tabs([
    "🥗 حاسبة التموين الذكية", 
    "🧳 الأمتعة والأوزان", 
    "👕 الملابس والمصروف", 
    "💊 الصيدلية والطوارئ", 
    "📱 الاتصالات والباقات", 
    "🕋 العبادات ويوم الجمعة", 
    "🕋 كيفية أداء العمرة", 
    "🍽️ مطاعم المدينة المنورة", 
    "🍽️ مطاعم مكة المكرمة", 
    "⚠️ العراقيل والمطارات", 
    "🎁 الهدايا والتسوق"
])

with guide_tabs[0]:
    st.subheader("🥗 حاسبة التموين الجاف المحدثة")
    tc1, tc2, tc3 = st.columns(3)
    with tc1: num_p = st.number_input("عدد الأشخاص:", min_value=1, max_value=100, value=2, key="p_num_t")
    with tc2: m_days = st.number_input("أيام المدينة:", min_value=0, max_value=30, value=3, key="m_days_t")
    with tc3: mk_days = st.number_input("أيام مكة:", min_value=0, max_value=30, value=11, key="mk_days_t")
    
    if m_days + mk_days > 0:
        st.success(f"📊 **الكميات المطلوبة لعدد ({num_p}) أشخاص:**")
        col_x, col_y = st.columns(2)
        with col_x:
            st.write(f"- 🥫 طماطم معلب: {num_p * 2.5} علبة (علبتان ونصف للشخص)")
            st.write(f"- 🍝 معكرونة: {num_p * 2} كجم (2 كيلو للشخص)")
            st.write(f"- 🐟 التونة: {num_p * 4} علبة (4 علب للشخص)")
            st.write(f"- 🍚 الأرز: {num_p * 1} كجم (كيلو للشخص)")
            st.write(f"- 🌾 الكسكسي: {num_p * 1} كجم (كيلو للشخص)")
            st.write(f"- 🧀 الجبن: {num_p * 2} علبة (علبتان للشخص)")
            st.write(f"- 🧂 السكر: {num_p * 1} كجم (كيلو للشخص)")
        with col_y:
            st.write("- 🍪 البسكويت: حسب الطلب")
            st.write(f"- 🥄 الملاعق: {num_p * 2} ملاعق (ملعقتان للشخص)")
            st.write("- 🔪 سكين لتقطيع اللحوم والخضروات: مطلوب أساسي")
            st.write("- ✨ إضافات: مكسرات، قهوة، شاي، شوكولاتة، وحلويات شعبية")
        st.warning("💡 لا يُنصح بنقل الخضار الطازجة لتوفرها بجودة عالية وأسعار مناسبة جداً في السعودية.")

with guide_tabs[1]:
    st.subheader("🧳 أوزان الحقائب وطرق تفادي الوزن الزائد")
    st.write("التذكرة العادية 23 كجم حقيبة أسفل الطائرة + 7 إلى 10 كجم هاند باق. رجال الأعمال حتى 32 كجم.")

with guide_tabs[2]:
    st.subheader("👕 الملابس والمصروف الشخصي")
    st.write("5 قطع ملابس داخلية، 5 هركة أو بدلة عربية، شبشب، وسبيدرو. تضاعف الكمية في حال البقاء للعيد في رمضان. وتجميع 50 ريال لكل شخص للمصروف المشترك.")

with guide_tabs[3]:
    st.subheader("💊 الصيدلية المقترحة للسفر")
    st.write("بندول أزرق وأحمر، فيتامين سي، سودا كريم، قطرة أنف، 123، ديفيدوا، لاصق جروح، وحلاوة علاجية للرقبة.")

with guide_tabs[4]:
    st.subheader("📱 الاتصالات وشفرات الانترنت")
    st.write("شفرة 60 ريال تكفي أسبوعين. وتتوفر شفرات دولية بمطار معيتيقة الدولي بالدينار الليبي.")

with guide_tabs[5]:
    st.subheader("🕋 العبادات وأحكام صلاة الجمعة")
    st.write("احرص على الصلاة في الحرمين الشريفين، وخذ معك كيس بلاستيك للحذاء مع حفظ رقم الرف. وتوجه للحرم باكراً قبل العاشرة صباحاً يوم الجمعة.")

with guide_tabs[6]:
    st.subheader("🕋 كيفية أداء العمرة")
    st.markdown("[🎥 مشاهدة فيديو شرح العمرة](https://www.youtube.com/watch?v=6u-Xj1s3vEg)")
    st.markdown("[📖 مقال مناسك العمرة (زاد العمرة)](https://zadumrah.com/blog/%D9%85%D9%86%D8%A7%D8%B3%D9%83-%D8%A7%D9%8لل%D8%B9%D9%85%D8%B1%D8%A9-%D9%83%D8%A7%D9%85%D9%84%D8%A9)")

with guide_tabs[7]:
    st.subheader("🍽️ مطاعم المدينة المنورة")
    st.markdown("- [مطعم الرومانسية](https://maps.app.goo.gl/eXLWec8NDDpUZ9r16)")
    st.markdown("- [فراولتي سلطانه](https://maps.app.goo.gl/mKb5kU5xZTqHgqnH6)")
    st.markdown("- [عالم الوسام](https://maps.app.goo.gl/d47HSmRFsbzsUaKaA)")
    st.markdown("- [حاشي باشا](https://maps.app.goo.gl/Ke7qhVrpBCfkvHND6?g_st=iw)")
    st.markdown("- [مطعم ريدان](https://goo.gl/maps/GsPBE9HAmLG2fEzq6)")
    st.markdown("- [مطعم البيك](https://maps.app.goo.gl/6dBdoG9bwZMyZXLx5)")

with guide_tabs[8]:
    st.subheader("🍽️ مطاعم مكة المكرمة")
    st.markdown("- [مطعم ريدان](https://maps.app.goo.gl/84kdUPqxL3i8xHuz8)")
    st.markdown("- [مطعم الطازج](https://maps.app.goo.gl/Uo5mmxoCBN4N2vt1A)")
    st.markdown("- [مطعم الرومانسية](https://maps.app.goo.gl/iNy3bX8Dv7xzUBe46)")
    st.markdown("- [البيك إكسبريس](https://maps.app.goo.gl/thY6c2YKRTMTm8z98)")

with guide_tabs[9]:
    st.subheader("⚠️ العراقيل والمتوقع في السفر")
    st.write("مشاكل الوزن وتأخير الطيران تعود لشركة الطيران الأم.")

with guide_tabs[10]:
    st.subheader("🎁 الهدايا وأسواق التسوق")
    st.write("سوق سلام في العزيزية وأبراج الساعة. وأفضل الهدايا العطور والتمور.")

st.markdown("---")

# --- 💡 خانة المقترحات مع إرفاق صورة ---
st.subheader("💡 شاركنا برأيك ومقترحاتك (مع إمكانية إرفاق صورة)")
with st.form("suggestion_form_v22"):
    s_name = st.text_input("✍️ اسم المقترح / الزائر:")
    s_type = st.selectbox("📌 نوع المقترح:", ["تعديل على الخدمات", "إضافة ميزة جديدة", "رأي أو ملاحظة عامة", "أخرى"])
    s_details = st.text_area("💬 التفاصيل والتعديلات المناسبة:")
    uploaded_file = st.file_uploader("🖼️ إرفاق صورة توضيحية للمقترح (اختياري):", type=["png", "jpg", "jpeg"])
    
    submit_suggestion = st.form_submit_button("📤 إرسال المقترح للإدارة", use_container_width=True)
    if submit_suggestion:
        if s_name.strip() and s_details.strip():
            img_path = ""
            if uploaded_file is not None:
                os.makedirs("uploads", exist_ok=True)
                img_path = os.path.join("uploads", uploaded_file.name)
                with open(img_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            df_s = load_suggestions()
            new_s = {
                "الوقت": time.strftime("%Y-%m-%d %H:%M:%S"),
                "اسم المقترح": s_name,
                "نوع المقترح": s_type,
                "التفاصيل والتعديلات": s_details,
                "مسار الصورة": img_path
            }
            pd.concat([df_s, pd.DataFrame([new_s])], ignore_index=True).to_excel(suggestions_filename, index=False)
            st.success("🙏 شكراً لك! تم إرسال مقترحك وصورتك المرفقة إلى الإدارة بنجاح.")
        else:
            st.error("⚠️ يرجى كتابة الاسم والتفاصيل.")

st.markdown("---")

# --- ✈️ جدول تذاكر الطيران ---
st.subheader("✈️ أسعار ومواعيد تذاكر الطيران المتاحة للمعتمرين")
st.dataframe(df_flights, use_container_width=True)
st.markdown("---")

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

col1, col2 = st.columns(2)
col1.metric("📊 إجمالي الفنادق المعروضة", len(filtered_df))
if not filtered_df.empty and 'المسافة إلى الحرم (كم)' in filtered_df.columns: 
    col2.metric("📍 أقرب فندق متوفر حالياً", f"{filtered_df['المسافة إلى الحرم (كم)'].min()} كم")

# 📋 جدول الفنادق
st.subheader("📋 جدول الفنادق المتاحة وأسعار الحجز النهائي (شاملة القيمة المضافة)")
st.data_editor(
    filtered_df,
    use_container_width=True,
    height=450,
    column_config={
        "موقع الفندق على خرائط جوجل": st.column_config.LinkColumn(
            "📍 موقع الفندق على خرائط جوجل",
            display_text="🗺️ فتح الموقع في خرائط جوجل"
        ),
        "سعر الحجز النهائي (د.ل)": st.column_config.NumberColumn(
            "💰 السعر النهائي (د.ل)",
            format="%.2f د.ل"
        )
    },
    disabled=True if not st.session_state["logged_in"] else False
)

st.markdown("---")

# 📝 استمارة الحجز المباشر
st.subheader("📝 استمارة طلب حجز فندقي مباشر للمعتمرين مع إصدار فاتورة مبدئية")
with st.form("booking_form"):
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        b_name = st.text_input("✍️ اسم المعتمر الثلاثي:")
        b_phone = st.text_input("📞 رقم الهاتف / الواتساب:")
        room_type = st.selectbox("🪑 نوع الغرفة المطلوبة:", ["غرفة ثنائية (M2)", "غرفة ثلاثية (M3)", "غرفة رباعية (M4)", "جناح عائلي"])
    with b_col2:
        b_hotel = st.selectbox("🏨 اختر الفندق المطلوب:", options=df["اسم الفندق"].unique() if "اسم الفندق" in df.columns else [], key="hotel_book_box")
        b_days = st.number_input("📅 عدد أيام الإقامة:", min_value=1, max_value=30, value=3)
    
    submit_booking = st.form_submit_button("🚀 تأكيد وإرسال طلب الحجز للإدارة", use_container_width=True)
    if submit_booking:
        if b_name.strip() and b_phone.strip():
            hotel_row = df[df["اسم الفندق"] == b_hotel]
            night_price = hotel_row["سعر الحجز النهائي (د.ل)"].values[0] if not hotel_row.empty else 0
            multiplier = 1.25 if "ثلاثية" in room_type else (1.45 if "رباعية" in room_type else (1.80 if "جناح" in room_type else 1.0))
            total_price = round(night_price * b_days * multiplier, 2)
            
            df_b = load_bookings()
            new_b = {
                "الوقت": time.strftime("%Y-%m-%d %H:%M:%S"),
                "اسم المعتمر": b_name,
                "رقم الهاتف": b_phone,
                "نوع الغرفة": room_type,
                "الفندق المطلوبة": b_hotel,
                "عدد الأيام": b_days,
                "إجمالي السعر (د.ل)": total_price,
                "حالة الطلب": "جديد"
            }
            pd.concat([df_b, pd.DataFrame([new_b])], ignore_index=True).to_excel(bookings_filename, index=False)
            st.success(f"🎉 تم تسجيل طلب حجزك بنجاح! الإجمالي المقدر: **{total_price} دينار ليبي**.")
            st.balloons()
        else:
            st.error("⚠️ يرجى كتابة الاسم ورقم الهاتف.")

st.markdown("---")

# --- 💬 أرسل رسالة للمدير (مراسلة داخلية تصل للأدمن مباشرة) ---
st.subheader("💬 أرسل رسالة مباشرة لإدارة الشركة")
with st.form("admin_message_form"):
    msg_name = st.text_input("اسمك الكريم أو بريدك:")
    msg_text = st.text_area("نص الرسالة أو الاستفسار الموجه للإدارة:")
    submit_msg = st.form_submit_button("إرسال الرسالة للمدير", use_container_width=True)
    if submit_msg:
        if msg_name.strip() and msg_text.strip():
            df_m = load_admin_messages()
            new_m = {
                "الوقت": time.strftime("%Y-%m-%d %H:%M:%S"),
                "البريد / الاسم": msg_name,
                "نص الرسالة": msg_text
            }
            pd.concat([df_m, pd.DataFrame([new_m])], ignore_index=True).to_excel(admin_messages_filename, index=False)
            st.success("✓ تم إرسال رسالتك إلى إدارة الشركة بنجاح وسنطلع عليها فوراً.")
        else:
            st.error("⚠️ يرجى كتابة الاسم ونص الرسالة.")

st.markdown("---")

# --- 🤝 خانات التواصل والأزرار الرئيسية ---
st.subheader("🤝 تواصل معنا عبر منصاتنا الرسمية")
fb_link = "https://www.facebook.com/share/1DveNwUUvR/"
tiktok_link = "https://www.tiktok.com/@miqat_11june_branch?is_from_webapp=1&sender_device=pc"
maps_link = "https://maps.app.goo.gl/6VL4dgZ3EuWsj46XA?g_st=ac"

link_c1, link_c2, link_c3 = st.columns(3)
with link_c1: st.link_button("🌐 صفحة فيسبوك الرسمية", fb_link, use_container_width=True)
with link_c2: st.link_button("🎵 حساب تيك توك", tiktok_link, use_container_width=True)
with link_c3: st.link_button("📍 موقعنا بجوجل ماب", maps_link, use_container_width=True)

st.markdown("---")

# --- 🛠️ لوحة تحكم الأدمن ---
if st.session_state["logged_in"]:
    st.subheader("🛠️ لوحة تحكم الأدمن: مراجعة الحجوزات، المقترحات، ورسائل الزوار")
    adm_c1, adm_c2, adm_c3 = st.columns(3)
    with adm_c1:
        st.subheader("📝 طلبات الحجز الفندقي")
        st.dataframe(load_bookings(), use_container_width=True)
    with adm_c2:
        st.subheader("💡 مقترحات الزوار مع الصور")
        sug_df = load_suggestions()
        st.dataframe(sug_df, use_container_width=True)
        for idx, row in sug_df.iterrows():
            if pd.notna(row["مسار الصورة"]) and os.path.exists(str(row["مسار الصورة"])):
                st.image(row["مسار الصورة"], caption=f"مقترح من: {row['اسم المقترح']}", width=200)
    with adm_c3:
        st.subheader("💬 رسائل الزوار للمدير")
        st.dataframe(load_admin_messages(), use_container_width=True)

st.sidebar.markdown("---")
if os.path.exists(excel_filename):
    with open(excel_filename, "rb") as file:
        st.sidebar.download_button(label="📥 تنزيل جدول الفنادق كملف Excel", data=file, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
