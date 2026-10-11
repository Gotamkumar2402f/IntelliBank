# 🏦 IntelliBank

**AI-Powered Intelligent Banking System with Real-Time Fraud Detection**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=for-the-badge&logo=xgboost&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00C853?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📖 Project Explanation

**IntelliBank** is an intelligent, AI-powered banking system designed to detect fraudulent transactions in real-time using Machine Learning and Large Language Models. The system provides a modern, professional banking dashboard with fraud detection, AI assistant, PDF analysis, and comprehensive audit capabilities.

### 🎯 Purpose

Traditional banking systems rely on manual fraud detection, which is slow and error-prone. **IntelliBank** solves this by:

- Using **XGBoost ML model** to score every transaction in real-time
- Providing **SHAP explainability** to understand *why* a transaction was flagged
- Integrating **Groq LLM (Llama 3.3 70B)** for natural language queries
- Offering **voice-enabled AI assistant** (Jarvis) for hands-free banking
- Enabling **PDF document analysis** for bank statements and reports

### 💡 How It Works
# 🏦 IntelliBank

**AI-Powered Intelligent Banking System with Real-Time Fraud Detection**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=for-the-badge&logo=xgboost&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00C853?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📖 Project Explanation

**IntelliBank** is an intelligent, AI-powered banking system designed to detect fraudulent transactions in real-time using Machine Learning and Large Language Models. The system provides a modern, professional banking dashboard with fraud detection, AI assistant, PDF analysis, and comprehensive audit capabilities.

### 🎯 Purpose

Traditional banking systems rely on manual fraud detection, which is slow and error-prone. **IntelliBank** solves this by:

- Using **XGBoost ML model** to score every transaction in real-time
- Providing **SHAP explainability** to understand *why* a transaction was flagged
- Integrating **Groq LLM (Llama 3.3 70B)** for natural language queries
- Offering **voice-enabled AI assistant** (Jarvis) for hands-free banking
- Enabling **PDF document analysis** for bank statements and reports

### 💡 How It Works

IntelliBank detects fraud in **6 simple steps**:

1. **Transaction Input** — User submits transaction details (amount, type, hour, account balance)

2. **Feature Extraction** — System prepares 8 key features:
   - Transaction amount
   - Hour of day
   - Night-time flag (12 AM – 6 AM)
   - Transaction type (deposit / withdrawal / transfer)
   - Account balance
   - Amount-to-balance ratio

3. **ML Prediction** — XGBoost model predicts fraud probability between **0.0 (safe)** and **1.0 (fraud)**

4. **SHAP Explanation** — System explains which features pushed the score up or down

5. **Fraud Score** — Final score determines risk level:
   - **≥ 0.5** → 🚨 Fraud Flagged
   - **< 0.5** → ✅ Transaction Safe

6. **Action** — For high-risk transactions:
   - 📧 Email alert sent to admin
   - 📋 Audit log entry created
   - 🔒 Account block recommended

   ### 🎓 Academic Value

- **ML Pipeline**: Complete train → evaluate → deploy cycle
- **Explainable AI**: SHAP values for model transparency
- **LLM Integration**: Real-world AI assistant implementation
- **Full-Stack**: Backend + Frontend + ML + AI
- **Security**: Role-based access, audit logging, secret management

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Fraud Detection** | XGBoost model with real-time scoring |
| 🔍 **SHAP Explainability** | Understand why transactions are flagged |
| 💬 **Jarvis AI Assistant** | Groq LLM (Llama 3.3 70B) with voice + text |
| 📄 **PDF Analysis** | Extract amounts, dates, account numbers |
| 📊 **Real-time Dashboard** | Auto-refresh every 15s with live metrics |
| 🎮 **Fraud Simulator** | Test custom transactions instantly |
| 🔐 **Role-based Login** | Admin and User roles with permissions |
| 📋 **Audit Log** | Complete activity tracking |
| 📥 **Export Reports** | Download as Excel, PDF, or CSV |
| 👤 **Risk Profiling** | Auto-categorize customers by risk tier |

---

🛠️ Tech Stack
Layer	Technologies
Backend	FastAPI, SQLAlchemy, SQLite
Frontend	Streamlit, Plotly
AI/ML	XGBoost, SHAP, scikit-learn, Pandas, NumPy
LLM	Groq API (Llama 3.3 70B)
Voice	SpeechRecognition, gTTS
PDF	PyPDF2, pdfplumber
Security	JWT, passlib, python-jose

🎯 Use Cases
🏦 Banking Sector: Real-time fraud detection for transactions

📚 Education: ML pipeline demonstration for students

🔬 Research: SHAP explainability and LLM integration

💼 Portfolio: Full-stack AI project showcase