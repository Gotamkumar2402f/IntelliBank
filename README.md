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
2. **Feature Extraction** — System prepares 8 key features (amount, hour, night flag, type, balance, ratio)
3. **ML Prediction** — XGBoost model predicts fraud probability between **0.0 (safe)** and **1.0 (fraud)**
4. **SHAP Explanation** — System explains which features pushed the score up or down
5. **Fraud Score** — Score ≥ 0.5 = 🚨 Fraud Flagged, Score < 0.5 = ✅ Safe
6. **Action** — High-risk triggers email alert, audit log, and account block recommendation

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

## 🚀 Setup

```bash
# 1. Clone the repository
git clone https://github.com/Gotamkumar2402f/IntelliBank.git
cd IntelliBank

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Add your GROQ_API_KEY in .env

# 5. Run the application
streamlit run dashboard.py