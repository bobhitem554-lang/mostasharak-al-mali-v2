import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai

# 1. إعدادات الصفحة والاسم الرسمي في علامة تبويب المتصفح
st.set_page_config(page_title="مستشارك المالي الذكي", page_icon="📊", layout="centered")

# إضافة نمط التصميم الفخم المخصص بأسلوب ChatGPT عبر الـ CSS
st.markdown("""
    <style>
    /* تحسين الخلفية العامة للنظام المظلم الفاخر */
    .stApp {
        background-color: #0b0d17;
        color: #f1f5f9;
        font-family: 'Cairo', sans-serif;
    }
    
    /* تصميم العنوان الرئيسي الاستثماري في أعلى الشاشة */
    h1 {
        color: #f59e0b !important;
        text-align: center;
        font-weight: 700;
        font-size: 2.2rem;
        margin-top: 30px;
        text-shadow: 0px 4px 15px rgba(245, 158, 11, 0.2);
    }
    .stCaption {
        color: #94a3b8 !important;
        text-align: center;
        font-size: 1rem !important;
        margin-bottom: 2rem;
    }

    /* صندوق الرسالة الترحيبية التفاعلية في وسط الشاشة */
    .welcome-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(245, 158, 11, 0.15);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .welcome-card h3 {
        color: #fbbf24 !important;
        margin-bottom: 10px;
    }
    .welcome-card p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 5px 0;
    }

    /* تنسيق صناديق التقارير المفسرة والنتائج الصادرة */
    .financial-report {
        background: rgba(22, 28, 45, 0.9);
        border-right: 4px solid #f59e0b;
        padding: 25px;
        border-radius: 16px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* تخصيص مكونات الرفع الافتراضية لتبدو كعلامة زائد أنيقة */
    .stFileUploader section {
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    }
    .stFileUploader button {
        background: #1e293b !important;
        color: #f59e0b !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        font-size: 1.4rem !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease;
    }
    .stFileUploader button:hover {
        background: #f59e0b !important;
        color: #0b0d17 !important;
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.6);
    }

    /* زر الإرسال الجانبي الصغير السهم */
    div.stButton > button:first-child {
        background: #f59e0b !important;
        color: #0b0d17 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        font-size: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        background: #fbbf24 !important;
        transform: scale(1.05) !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي 👑
st.markdown("<h1>👑 مستشارك المالي الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p class='stCaption'>الواجهة الحوارية النخبوية لدراسات الجدوى وتحليل الميزانيات الاقتصادية</p>", unsafe_allow_html=True)

# المفتاح السري الفعال والصحيح 
API_KEY = "AQ.Ab8RN6IpaIcC-826hp7Sm4JSyb4ns6qWGyPgXyUx3a27Ioh_7w"

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        
        excel_data_str = ""
        uploaded_image = None

        st.markdown("<div style='margin-bottom: 120px;'>", unsafe_allow_html=True)

        # عرض الرسالة الترحيبية التفاعلية في وسط الشاشة
        st.markdown("""
            <div class='welcome-card'>
                <h3>👋 مرحباً بك في منصتك الاستشارية</h3>
                <p>أنا مستشارك المالي الذكي، كيف يمكنني مساعدتك اليوم في ريادة أعمالك؟</p>
                <p>💡 <b>يمكنك الآن:</b> كتابة فكرة مشروعك للحصول على دراسة جدوى فورية وتكلفة تقديرية.</p>
                <p>➕ <b>تحليل متقدم:</b> اضغط على علامة (+) بالأسفل لإرفاق ملفات Excel أو صور القوائم المالية.</p>
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("", type=["xlsx", "csv", "png", "jpg", "jpeg"])

        if uploaded_file is not None:
            if uploaded_file.name.endswith(('.xlsx', '.csv')):
                try:
                    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                    st.success("📈 تم دمج وقراءة جدول البيانات بنجاح!")
                    with st.expander("👀 استعراض الأسطر الأولى من الملف"):
                        st.dataframe(df.head(5))
                    excel_data_str = df.to_string()
                except Exception as e:
                    st.error(f"خطأ في قراءة ملف الإكسل: {e}")
            else:
                try:
                    uploaded_image = Image.open(uploaded_file)
                    st.success("📸 تم فحص مستند القائمة المالية الورقية بنجاح!")
                    with st.expander("👀 استعراض المستند الممسوح"):
                        st.image(uploaded_image, use_container_width=True)
                except Exception as e:
                    st.error(f"خطأ في قراءة الصورة المرفوعة: {e}")

        # بناء شريط الإدخال السفلي
        col_file, col_input, col_send = st.columns()

        with col_file:
            st.markdown("<p style='font-size:0.75rem; text-align:center; color:#94a3b8; margin:0; padding-top:10px;'>إرفاق (+)</p>", unsafe_allow_html=True)

        with col_input:
            user_query = st.text_input(
                "",
                placeholder="✍️ اكتب فكرة مشروعك أو استفسارك الاستثماري هنا...",
                label_visibility="collapsed"
            )

        with col_send:
            submit_button = st.button("➔")

        if submit_button:
            if not user_query and uploaded_file is None:
                st.warning("الرجاء كتابة استفسارك أو رفع وثيقة مالية ليتمكن المستشار من إجابتك.")
            else:
                with st.spinner("⏳ جاري تحليل المؤشرات وإعداد التقرير الاستثماري النخبوي..."):
                    try:
                        system_prompt = (
                            "أنت خبير اقتصادي ومستشار مالي مرموق تقدم تقارير استشارية دقيقة وموثوقة. "
                            "قم بتحليل طلب المستخدم، واذكر أرقام وتكاليف تقديرية واضحة ومفصلة للمشاريع المطلوبة، "
                            "وخطط تشغيلية، وحساب لنقطة التعادل وفترة استرداد رأس المال بأسلوب احترافي وبند عريض. "
                            "يجب أن تكون الإجابة كاملة باللغة العربية ومنسقة بشكل رائع ومنظم كتقرير موجه لرجال الأعمال.\n\n"
                        )
                        
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        content_inputs = [system_prompt]
                        
                        if excel_data_str:
                            content_inputs.append(f"بيانات مستند الإكسل المرفق:\n{excel_data_str}\n\n")
                        if uploaded_image:
                            content_inputs.append(uploaded_image)
                            content_inputs.append("قم بتحليل وفحص بنود الميزانية الظاهرة في صورة هذه الوثيقة.\n")
                        
                        content_inputs.append(f"طلب العميل الحالي: {user_query}")
                        response = model.generate_content(content_inputs)
                        
                        st.markdown("<div class='financial-report'>", unsafe_allow_html=True)
                        st.subheader("👑 التقرير الاستثماري الصادر عن المنصة:")
                        st.write(response.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.error(f"عذراً، واجه المستشار المالي مشكلة أثناء التحليل: {e}")
                        
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات الذكية: {e}")
else:
    st.info("الرجاء إدخال مفتاح التفعيل لبدء تشغيل المستشار المالي.")
