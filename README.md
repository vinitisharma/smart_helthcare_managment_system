# 🏥 Smart Healthcare System (AI + ML Project)

## 📌 Overview

The **Smart Healthcare System** is a full-stack AI-powered web application that predicts:

* ❤️ **Heart Disease Risk**
* 🏋️ **Fitness Level**

It also includes:

* 📊 Interactive dashboard with charts
* 🤖 AI Health Assistant (Chatbot)
* 📄 PDF report generation
* 💬 Feedback system
* 🔐 Authentication (User & Admin)

This project combines **Machine Learning + FastAPI + Streamlit + SQLite** into a real-world healthcare solution.

---

# 🚀 Features

## 👤 User Features

* Predict **Heart Disease Risk** (Low / Moderate / High)
* Predict **Fitness Level** (Fit / Moderate / Unfit)
* View **Dashboard with charts**
* Download **PDF reports**
* Use **AI Chatbot for health guidance**
* Submit **feedback**

---

## 🛠️ Admin Features

* View all users
* See prediction records
* Monitor system usage
* View feedback submissions

---

# 🤖 AI Chatbot (Special Feature)

* Context-aware responses
* Uses user prediction data
* Provides personalized advice
* Includes:

  * Quick action buttons
  * Typing animation
  * Health improvement plans

---

# 🧠 Machine Learning Models

## ❤️ Heart Disease Model

* Algorithm: SVM / Random Forest (pipeline-based)
* Preprocessing:

  * OneHotEncoding (categorical)
  * StandardScaler (numerical)
* Output:

  * Risk Probability
  * Risk Category (Low / Moderate / High)

---

## 🏋️ Fitness Model

* Algorithm: Random Forest
* Inputs:

  * Body metrics + physical performance
* Output:

  * Fit / Moderate / Unfit

---

# 🏗️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI

### Database

* SQLite

### ML Libraries

* Scikit-learn
* Pandas
* NumPy

### Other

* ReportLab (PDF)
* Matplotlib (charts)
* JWT Authentication

---


# ⚙️ Installation & Setup

## 1️⃣ Clone Project

```bash
git clone <your-repo-link>
cd smart_healthcare_system
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

👉 Runs at:

```
http://127.0.0.1:8000
```

---

## 5️⃣ Run Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

---

# 🔐 Authentication

### User Login

* Register new user
* Login with email & password

### Admin Login

* Uses `.env` credentials:

```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

---

# 📊 How It Works

1. User enters health data
2. Data sent to FastAPI backend
3. ML model processes input
4. Prediction stored in SQLite
5. Result displayed in UI + dashboard
6. Chatbot uses this data for personalized advice

---

# 📈 Dashboard

* ❤️ Heart Risk Chart
* 🏋️ Fitness Distribution
* 📈 Trend analysis
* Real-time updates

---

# 📄 PDF Reports

* Downloadable reports
* Includes:

  * Prediction result
  * Probability
  * Health summary

---

# 🧪 Sample Inputs

## Heart Prediction

```json
{
  "age": 45,
  "sex": 1,
  "cp": "2",
  "bp": 130,
  "cholesterol": 220,
  "fbs": 0,
  "restecg": "1",
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": "1",
  "ca": 0,
  "thal": "2"
}
```

---

## Fitness Prediction

```json
{
  "age": 23,
  "gender": 1,
  "height": 175,
  "weight": 68,
  "body_fat": 15,
  "diastolic": 72,
  "systolic": 110,
  "gripForce": 45,
  "flexibility": 30,
  "situps": 50,
  "jump": 200
}
```

---

# 🧠 Key Highlights

* End-to-end ML project
* Real-time prediction system
* Full-stack architecture
* AI chatbot integration
* Clean UI/UX
* Production-ready structure

---

# ⚠️ Disclaimer

This system is for **educational purposes only** and does not replace professional medical advice.

---

# 👨‍💻 Author

**Mohnish**

---

# ⭐ If you like this project

Give it a ⭐ on GitHub!
