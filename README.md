 # 🚀 Loan Eligibility Prediction System

### **AI-Powered Loan Advisor with ML, Flask, Streamlit, MySQL & Gemini Chatbot**
## 📌 **Overview**

This project is an end-to-end **Loan Eligibility Prediction System** built using:

* **Machine Learning (Logistic Regression / Random Forest)**
* **Flask Backend (REST APIs + Authentication)**
* **Streamlit Frontend**
* **MySQL Database using SQLAlchemy ORM**
* **Gemini AI Chatbot integration**
* **Secure Login, Prediction History & Explanation Engine**

The system predicts whether a user's loan application will get **Approved** or **Rejected**, provides **AI-generated explanations**, and offers an interactive **chatbot** to guide users.

## ✨ **Key Features**

### 🔐 **User Authentication**

* Signup, Login, Logout
* Password hashing using Werkzeug
* Session-based authentication

### 🤖 **AI-Powered Chatbot**

* Uses **Google Gemini Flash 2.5**
* Provides explanations for predictions
* Users can ask finance/loan questions

### 🧠 **Loan Prediction Engine**

* ML model trained on historical loan data
* Feature engineering:

  * Log transforms
  * One-hot encoding
  * Credit-score flagging
* Predicts: **Approved / Rejected**

### 📊 **Store Loan Applications**

Each submission is saved in MySQL with:

* User ID
* Input parameters
* Prediction result
* Timestamp

### 🖥️ **Streamlit UI**

* Clean, interactive interface
* User-friendly sliders & dropdowns
* Result visualization (success/error)
* Balloon animation on approval

### 🧱 **Flask Backend**

* REST API for predictions
* Chatbot API
* Authentication API routes
* Integration with Streamlit frontend

## 📁 **Project Structure**

```
project/
│
├── flask_app.py                # Flask server (backend)
├── chatflask.py                #Gemini chatbot logic
├── streamlitapp.py             # Streamlit UI (frontend)
├── chatbot.py                  # Gemini chatbot logic
├── model.pkl                   # ML model
├── static/                     # CSS, JS, assets
├── templates/                  # HTML templates (Flask)
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

---

## 🗃️ **Database Schema (MySQL)**

### **User Table**

| Column        | Type     |
| ------------- | -------- |
| id            | INT (PK) |
| email         | VARCHAR  |
| password_hash | TEXT     |

### **LoanApplication Table**

| Column            | Type               |
| ----------------- | ------------------ |
| id                | INT (PK)           |
| user_id           | INT (FK → User.id) |
| gender            | VARCHAR            |
| married           | VARCHAR            |
| dependents        | VARCHAR            |
| education         | VARCHAR            |
| employed          | VARCHAR            |
| credit            | FLOAT              |
| area              | VARCHAR            |
| ApplicantIncome   | FLOAT              |
| CoapplicantIncome | FLOAT              |
| LoanAmount        | FLOAT              |
| Loan_Amount_Term  | INT                |
| prediction_result | VARCHAR            |
| timestamp         | DATETIME           |

---

## 🛠️ **Tech Stack**

| Layer          | Technology                  |
| -------------- | --------------------------- |
| **Frontend**   | Streamlit                   |
| **Backend**    | Flask                       |
| **ML Model**   | scikit-learn                |
| **Database**   | MySQL + SQLAlchemy          |
| **AI Chatbot** | Google Gemini 2.5 Flash     |
| **Security**   | Password hashing (Werkzeug) |

---

## ⚙️ **Setup & Installation**

### **1️⃣ Clone the Repository**

```bash
git clone <repo-url>
cd loan-prediction
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Configure MySQL Database**

Create DB:

```sql
CREATE DATABASE loan_prediction_db;
```

Update credentials in `flask_app.py`:

```
mysql+pymysql://<username>:<password>@localhost:3306/loan_prediction_db
```

Initialize tables:

```python
from flask_app import db, app
with app.app_context():
    db.create_all()
```

### **4️⃣ Add Your Gemini API Key**

In `chatbot.py` or `chatflask.py`:

```python
genai.configure(api_key="YOUR_API_KEY")
```

### **5️⃣ Run Flask Backend**

```bash
python flask_app.py
```

Runs on → **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### **6️⃣ Run Streamlit Frontend**

```bash
streamlit run streamlitapp.py
```

Runs on → **[http://localhost:8501](http://localhost:8501)**

## 🧪 **How It Works**

### **User Flow**

1. User signs up and logs in
2. Enters loan details
3. Backend applies:

   * numerical encoding
   * log transforms
   * credit-score logic
4. ML model generates prediction
5. Streamlit shows result
6. Data is saved to MySQL
7. Gemini chatbot gives detailed explanation

## 📦 **Dependencies**

```
Flask
Flask-SQLAlchemy
Werkzeug
PyMySQL
scikit-learn
numpy
pandas
Streamlit
google-generativeai
grpcio
```
## 🎯 **Future Enhancements**

* Add loan EMI calculator
* Multi-user analytics dashboard
* Model retraining from stored applications
* JWT-based authentication
* Deployment on AWS/GCP
