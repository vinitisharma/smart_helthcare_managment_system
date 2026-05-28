import streamlit as st
from components.api_client import register_user, login_user, admin_login, predict_heart, predict_fitness, get_dashboard, get_admin_dashboard, get_all_heart, get_all_fitness, send_feedback, get_all_feedback
import pandas as pd


st.set_page_config(page_title="Smart Healthcare System", layout="wide")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- FUNCTIONS ----------------

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "home"
    st.rerun()


# ---------------- SIDEBAR ----------------

st.sidebar.title("🏥 Navigation")

# BEFORE LOGIN
if not st.session_state.logged_in:

    if st.sidebar.button("👤 User Login"):
        st.session_state.page = "user_login"

    if st.sidebar.button("🛠 Admin Login"):
        st.session_state.page = "admin_login"

# AFTER LOGIN → USER
elif st.session_state.role == "user":

    if st.sidebar.button("🏠 Dashboard"):
        st.session_state.page = "dashboard"

    if st.sidebar.button("❤️ Heart Prediction"):
        st.session_state.page = "heart"

    if st.sidebar.button("🏋️ Fitness Prediction"):
        st.session_state.page = "fitness"

    if st.sidebar.button("📊 Attributes"):
        st.session_state.page = "attributes"

    if st.sidebar.button("💬 Feedback"):
        st.session_state.page = "feedback"

    # ✅ ADD THIS
    if st.sidebar.button("🤖 Chatbot"):
        st.session_state.page = "chatbot"

    if st.sidebar.button("🚪 Logout"):
        logout()

# AFTER LOGIN → ADMIN
elif st.session_state.role == "admin":

    if st.sidebar.button("📊 Admin Dashboard"):
        st.session_state.page = "admin_dashboard"

    if st.sidebar.button("❤️ Heart Records"):
        st.session_state.page = "admin_heart"

    if st.sidebar.button("🏋️ Fitness Records"):
        st.session_state.page = "admin_fitness"

    if st.sidebar.button("💬 Feedback Records"):
        st.session_state.page = "admin_feedback"

    if st.sidebar.button("🚪 Logout"):
        logout()


# ---------------- PAGE ROUTING ----------------

st.title("🏥 Smart Healthcare System")

if st.session_state.page == "home":
    st.info("Welcome! Please login from the sidebar.")


elif st.session_state.page == "user_login":

    st.header("👤 User Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN ----------------
    with tab1:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            data = {
                "email": email,
                "password": password
            }

            res = login_user(data)

            if "access_token" in res:
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.session_state.token = res["access_token"]

                st.success("Login successful")
                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error(res.get("error", "Login failed"))

    # ---------------- REGISTER ----------------
    with tab2:
        st.subheader("Register")

        name = st.text_input("Full Name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            data = {
                "name": name,
                "email": email,
                "password": password
            }

            res = register_user(data)

            if "message" in res:
                st.success("Registration successful. Please login.")
            else:
                st.write(res)


elif st.session_state.page == "admin_login":

    st.header("🛠 Admin Login")

    email = st.text_input("Admin Email")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin"):

        data = {
            "email": email,
            "password": password
        }

        res = admin_login(data)

        if "access_token" in res:
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.session_state.token = res["access_token"]

            st.success("Admin login successful")
            st.session_state.page = "admin_dashboard"
            st.rerun()

        else:
            st.error(res.get("error", "Login failed"))


elif st.session_state.page == "dashboard":

    import matplotlib.pyplot as plt

    st.header("📊 Your Health Dashboard")

    data = get_dashboard(st.session_state.token)

    # ❌ ERROR CHECK
    if "error" in data:
        st.error(data["error"])

    else:
        # =========================
        # 📌 TOP STATUS CARDS
        # =========================
        col1, col2 = st.columns(2)

        # ❤️ HEART STATUS
        with col1:
            st.subheader("❤️ Heart Status")

            if data.get("heart"):
                if data["heart"] == "High Risk":
                    st.error(f"⚠️ {data['heart']} ({data['heart_prob']*100:.2f}%)")
                elif data["heart"] == "Moderate Risk":
                    st.warning(f"⚠️ {data['heart']} ({data['heart_prob']*100:.2f}%)")
                else:
                    st.success(f"✅ {data['heart']} ({data['heart_prob']*100:.2f}%)")
            else:
                st.info("No data yet")

        # 🏋️ FITNESS STATUS
        with col2:
            st.subheader("🏋️ Fitness Status")

            if data.get("fitness"):
                if data["fitness"] == "Fit":
                    st.success("✅ Fit")
                elif data["fitness"] == "Moderate":
                    st.warning("⚠️ Moderate")
                else:
                    st.error("❌ Unfit")
            else:
                st.info("No data yet")

        st.markdown("---")

        # =========================
        # 📊 HEART BAR CHART
        # =========================
        if data.get("heart_prob") is not None:
            st.subheader("❤️ Heart Risk Level")

            fig, ax = plt.subplots()
            ax.bar(["Risk"], [data["heart_prob"] * 100])
            ax.set_ylabel("Probability (%)")
            ax.set_title("Heart Disease Risk")

            st.pyplot(fig)

        # =========================
        # 🏋️ FITNESS PIE CHART
        # =========================
        if data.get("fitness_history"):

            st.subheader("🏋️ Fitness History Distribution")

            fitness_values = [f["result"] for f in data["fitness_history"]]

            labels = ["Fit", "Moderate", "Unfit"]
            counts = [
                fitness_values.count("Fit"),
                fitness_values.count("Moderate"),
                fitness_values.count("Unfit")
            ]

            fig, ax = plt.subplots()
            ax.pie(counts, labels=labels, autopct='%1.1f%%')
            ax.set_title("Fitness Distribution")

            st.pyplot(fig)

        # =========================
        # 📈 HEART TREND LINE
        # =========================
        if data.get("heart_history"):

            st.subheader("📈 Heart Risk Trend")

            probs = [h["prob"] * 100 for h in data["heart_history"]]

            fig, ax = plt.subplots()
            ax.plot(probs, marker='o')
            ax.set_ylabel("Risk (%)")
            ax.set_xlabel("Prediction Count")
            ax.set_title("Heart Risk Over Time")

            st.pyplot(fig)

        # =========================
        # ℹ️ NOTE
        # =========================
        st.info("ℹ️ Data shown is based on your past predictions.")



elif st.session_state.page == "heart":

    st.header("❤️ Heart Disease Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        sex = st.selectbox("Sex", ["Male", "Female"])
        cp_options = {
            "Typical Angina": "0",
            "Atypical Angina": "1",
            "Non-anginal Pain": "2",
            "Asymptomatic": "3"
        }
        cp_label = st.selectbox("Chest Pain Type", list(cp_options.keys()))
        cp = cp_options[cp_label]

        bp = st.number_input("Resting BP (mm Hg)", min_value=80, max_value=200, value=120)
        cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=400, value=200)

        fbs = st.selectbox("Fasting Blood Sugar >120", ["No", "Yes"])
        restecg_options = {
            "Normal": "0",
            "ST-T Wave Abnormality": "1",
            "Left Ventricular Hypertrophy": "2"
        }
        restecg_label = st.selectbox("Rest ECG", list(restecg_options.keys()))
        restecg = restecg_options[restecg_label]

    with col2:
        thalach = st.number_input("Max Heart Rate", min_value=60, max_value=220, value=150)
        exang = st.selectbox("Exercise Angina", ["No", "Yes"])
        oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=6.0, value=1.0)
        slope_options = {
            "Upsloping": "0",
            "Flat": "1",
            "Downsloping": "2"
        }
        slope_label = st.selectbox("Slope", list(slope_options.keys()))
        slope = slope_options[slope_label]
        ca = st.selectbox("Major Vessels (0–3)", [0,1,2,3])
        thal_options = {
            "Normal": "1",
            "Fixed Defect": "2",
            "Reversible Defect": "3"
        }
        thal_label = st.selectbox("Thal", list(thal_options.keys()))
        thal = thal_options[thal_label]

    sex_val = 1 if sex == "Male" else 0
    fbs_val = 1 if fbs == "Yes" else 0
    exang_val = 1 if exang == "Yes" else 0

    if st.button("Predict"):

        data = {
            "age": age,
            "sex": sex_val,
            "cp": str(cp),
            "bp": bp,
            "cholesterol": cholesterol,
            "fbs": fbs_val,
            "restecg": str(restecg),
            "thalach": thalach,
            "exang": exang_val,
            "oldpeak": oldpeak,
            "slope": str(slope),
            "ca": ca,
            "thal": str(thal)
        }

        res = predict_heart(data, st.session_state.token)

        if "prediction" in res:

            prob = res["probability"]

            if res["prediction"] == 1:
                st.error(f"⚠️ High Risk ({prob*100:.2f}%)")
            else:
                st.success(f"✅ Low Risk ({prob*100:.2f}%)")

            st.progress(int(prob * 100))
            st.info("ℹ️ This prediction is based on ML model and not a medical diagnosis.")
            # PDF option
            import io
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from datetime import datetime

            buffer = io.BytesIO()

            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()

            # Determine result color text
            result_text = res["result"]
            probability_text = f"{prob*100:.2f}%"

            # Content
            content = []

            # Title
            content.append(Paragraph("❤️ Heart Disease Prediction Report", styles["Title"]))
            content.append(Spacer(1, 0.3 * inch))

            # Date
            content.append(Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles["Normal"]))
            content.append(Spacer(1, 0.2 * inch))

            # Section Header
            content.append(Paragraph("<b>Prediction Summary</b>", styles["Heading2"]))
            content.append(Spacer(1, 0.2 * inch))

            # Result
            content.append(Paragraph(f"<b>Result:</b> {result_text}", styles["Normal"]))
            content.append(Spacer(1, 0.1 * inch))

            # Probability
            content.append(Paragraph(f"<b>Probability:</b> {probability_text}", styles["Normal"]))
            content.append(Spacer(1, 0.3 * inch))

            # Interpretation
            content.append(Paragraph("<b>Interpretation:</b>", styles["Heading2"]))
            content.append(Spacer(1, 0.1 * inch))

            if res["prediction"] == 1:
                content.append(Paragraph(
                    "The model indicates a higher likelihood of heart disease. "
                    "It is recommended to consult a healthcare professional.",
                    styles["Normal"]
                ))
            else:
                content.append(Paragraph(
                    "The model indicates a lower likelihood of heart disease. "
                    "Maintain a healthy lifestyle and regular checkups.",
                    styles["Normal"]
                ))

            content.append(Spacer(1, 0.3 * inch))

            # Footer
            content.append(Paragraph(
                "Note: This is an AI-generated prediction and should not replace medical advice.",
                styles["Italic"]
            ))

            # Build PDF
            doc.build(content)
            buffer.seek(0)

            # Download Button
            st.download_button(
                label="📄 Download Heart Report",
                data=buffer,
                file_name="heart_report.pdf",
                mime="application/pdf"
            )

        else:
            st.error(res.get("error", "Prediction failed"))


elif st.session_state.page == "fitness":

    st.header("🏋️ Fitness Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=10, max_value=80, value=23)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=150, value=70)
        body_fat = st.number_input("Body Fat %", min_value=5.0, max_value=50.0, value=20.0)

    with col2:
        diastolic = st.number_input("Diastolic BP", min_value=50, max_value=120, value=80)
        systolic = st.number_input("Systolic BP", min_value=80, max_value=200, value=120)
        grip = st.number_input("Grip Strength", min_value=10.0, max_value=70.0, value=30.0)
        flexibility = st.number_input("Flexibility (cm)", min_value=0.0, max_value=50.0, value=20.0)
        situps = st.number_input("Sit-ups Count", min_value=0, max_value=200, value=30)
        jump = st.number_input("Broad Jump (cm)", min_value=50, max_value=350, value=150)

    if st.button("Predict Fitness"):

        data = {
            "age": age,
            "gender": 1 if gender == "Male" else 0,
            "height": height,
            "weight": weight,
            "body_fat": body_fat,
            "diastolic": diastolic,
            "systolic": systolic,
            "gripForce": grip,
            "flexibility": flexibility,
            "situps": situps,
            "jump": jump
        }

        res = predict_fitness(data, st.session_state.token)

        if "prediction" in res:

            result = res["prediction"]

            if result == "Fit":
                st.success("✅ You are FIT")
            elif result == "Moderate":
                st.warning("⚠️ You are MODERATE")
            else:
                st.error("❌ You are UNFIT")

            bmi = weight / ((height/100)**2)
            st.write(f"📊 BMI: {bmi:.2f}")
            # BMI classification (WHO)
            if bmi < 18.5:
                bmi_status = "Underweight"
                bmi_msg = "⚠️ You are underweight"
            elif 18.5 <= bmi < 25:
                bmi_status = "Normal"
                bmi_msg = "✅ Healthy BMI"
            elif 25 <= bmi < 30:
                bmi_status = "Overweight"
                bmi_msg = "⚠️ Overweight"
            else:
                bmi_status = "Obese"
                bmi_msg = "❌ Obese"

            st.info(f"{bmi_msg} (BMI: {bmi:.2f})")
            st.info("ℹ️ Fitness result is based on physical performance indicators.")
            # PDF option
            import io
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from datetime import datetime

            buffer = io.BytesIO()

            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()

            result_text = result  # Fit / Moderate / Unfit

            content = []

            # 🏋️ Title
            content.append(Paragraph("🏋️ Fitness Assessment Report", styles["Title"]))
            content.append(Spacer(1, 0.3 * inch))

            # 📅 Date
            content.append(Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles["Normal"]))
            content.append(Spacer(1, 0.2 * inch))

            # 📊 Section Header
            content.append(Paragraph("<b>Assessment Summary</b>", styles["Heading2"]))
            content.append(Spacer(1, 0.2 * inch))

            # Result
            content.append(Paragraph(f"<b>Fitness Level:</b> {result_text}", styles["Normal"]))
            content.append(Spacer(1, 0.3 * inch))

            # 🧠 Interpretation
            content.append(Paragraph("<b>Interpretation:</b>", styles["Heading2"]))
            content.append(Spacer(1, 0.1 * inch))

            if result_text == "Fit":
                content.append(Paragraph(
                    "You are in good physical condition. Maintain your current lifestyle, "
                    "including regular exercise and a balanced diet.",
                    styles["Normal"]
                ))

            elif result_text == "Moderate":
                content.append(Paragraph(
                    "Your fitness level is average. Consider improving your routine with "
                    "regular physical activity and a healthier diet.",
                    styles["Normal"]
                ))

            else:  # Unfit
                content.append(Paragraph(
                    "Your fitness level is below recommended standards. It is advisable "
                    "to start a structured fitness plan and consult a professional if needed.",
                    styles["Normal"]
                ))

            content.append(Spacer(1, 0.3 * inch))

            # 🏃 Recommendations
            content.append(Paragraph("<b>Recommendations:</b>", styles["Heading2"]))
            content.append(Spacer(1, 0.1 * inch))

            if result_text == "Fit":
                tips = [
                    "- Continue regular exercise (3-5 times/week)",
                    "- Maintain balanced nutrition",
                    "- Stay hydrated",
                    "- Regular health checkups"
                ]
            elif result_text == "Moderate":
                tips = [
                    "- Increase physical activity",
                    "- Improve diet (reduce junk food)",
                    "- Add strength training",
                    "- Monitor weight and BP"
                ]
            else:
                tips = [
                    "- Start light exercise (walking, yoga)",
                    "- Consult a fitness expert",
                    "- Focus on weight management",
                    "- Avoid sedentary lifestyle"
                ]

            for tip in tips:
                content.append(Paragraph(tip, styles["Normal"]))

            content.append(Spacer(1, 0.3 * inch))

            # ⚠️ Disclaimer
            content.append(Paragraph(
                "Note: This is an AI-generated fitness assessment and should not replace professional medical or fitness advice.",
                styles["Italic"]
            ))

            # Build PDF
            doc.build(content)
            buffer.seek(0)

            # 📥 Download Button
            st.download_button(
                label="📄 Download Fitness Report",
                data=buffer,
                file_name="fitness_report.pdf",
                mime="application/pdf"
            )

        else:
            st.error(res.get("error", "Prediction failed"))

elif st.session_state.page == "attributes":

    st.header("📊 Attributes & Restrictions")

    st.divider()

    # ❤️ HEART SECTION
    st.subheader("❤️ Heart Disease Prediction")

    st.markdown("""
- **Age** → Age of patient (years)
- **Sex** → Male / Female
- **Chest Pain (cp)** → Type of chest pain (0–3)
- **BP (trestbps)** → Resting blood pressure (mm Hg)
- **Cholesterol** → Serum cholesterol (mg/dl)
- **FBS** → Fasting blood sugar >120 (Yes/No)
- **RestECG** → ECG results (0–2)
- **Thalach** → Max heart rate achieved
- **Exang** → Exercise induced angina (Yes/No)
- **Oldpeak** → ST depression
- **Slope** → Slope of peak exercise
- **CA** → Major vessels (0–3)
- **Thal** → Blood disorder type
""")

    st.divider()

    # 🏋️ FITNESS SECTION
    st.subheader("🏋️ Fitness Prediction")

    st.markdown("""
- **Age** → Age in years
- **Gender** → Male / Female
- **Height** → cm
- **Weight** → kg
- **Body Fat** → %
- **Diastolic BP** → Lower BP value
- **Systolic BP** → Upper BP value
- **Grip Strength** → Hand strength
- **Flexibility** → Sit & bend distance
- **Sit-ups** → Count
- **Jump** → Broad jump distance
""")


elif st.session_state.page == "chatbot":
    from utils.chatbot import run_chatbot
    run_chatbot()


elif st.session_state.page == "feedback":

    st.header("💬 Feedback System")

    message = st.text_area("Enter your feedback")

    if st.button("Submit Feedback"):

        if not message:
            st.warning("Please enter feedback")
        else:
            res = send_feedback(
                {"message": message},
                st.session_state.token
            )

            if "message" in res:
                st.success("✅ Feedback submitted successfully")
            else:
                st.error(res.get("error", "Failed to submit feedback"))


elif st.session_state.page == "admin_dashboard":

    st.header("📊 Admin Dashboard")

    data = get_admin_dashboard(st.session_state.token)

    if "error" in data:
        st.error(data["error"])

    else:
        import matplotlib.pyplot as plt

        # =========================
        # KPI CARDS
        # =========================
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Users", data["total_users"])
        col2.metric("Heart Predictions", data["total_heart"])
        col3.metric("Fitness Predictions", data["total_fitness"])

        st.divider()

        # =========================
        # CHARTS SECTION
        # =========================
        col1, col2 = st.columns(2)

        # ❤️ HEART DISTRIBUTION (PIE)
        with col1:
            if data.get("heart_distribution"):
                st.subheader("❤️ Heart Risk Distribution")

                labels = list(data["heart_distribution"].keys())
                values = list(data["heart_distribution"].values())

                if sum(values) > 0:
                    fig, ax = plt.subplots()
                    ax.pie(values, labels=labels, autopct='%1.1f%%')
                    ax.set_title("Heart Risk Breakdown")

                    st.pyplot(fig)
                else:
                    st.info("No heart data available")

        # 🏋️ FITNESS DISTRIBUTION (BAR)
        with col2:
            if data.get("fitness_distribution"):
                st.subheader("🏋️ Fitness Distribution")

                labels = list(data["fitness_distribution"].keys())
                values = list(data["fitness_distribution"].values())

                if sum(values) > 0:
                    fig, ax = plt.subplots()
                    ax.bar(labels, values)
                    ax.set_title("Fitness Levels")

                    st.pyplot(fig)
                else:
                    st.info("No fitness data available")

        st.divider()

        # =========================
        # SYSTEM OVERVIEW
        # =========================
        st.subheader("📊 System Overview")

        fig, ax = plt.subplots()

        labels = ["Users", "Heart", "Fitness"]
        values = [
            data["total_users"],
            data["total_heart"],
            data["total_fitness"]
        ]

        ax.bar(labels, values)
        ax.set_title("Platform Usage")

        st.pyplot(fig)

elif st.session_state.page == "admin_heart":

    st.header("❤️ Heart Prediction Records")

    data = get_all_heart(st.session_state.token)

    if isinstance(data, list):
        df = pd.DataFrame(data)
        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

    else:
        st.error(data.get("error"))

elif st.session_state.page == "admin_fitness":

    st.header("🏋️ Fitness Records")

    data = get_all_fitness(st.session_state.token)

    if isinstance(data, list):
        df = pd.DataFrame(data)
        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )
    else:
        st.error(data.get("error"))

elif st.session_state.page == "admin_feedback":

    st.header("💬 Feedback Submissions")

    data = get_all_feedback(st.session_state.token)

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.info("No feedback available")