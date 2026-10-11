# 🏦 IntelliBank

**AI-Powered Intelligent Banking System with Real-Time Fraud Detection**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=for-the-badge&logo=xgboost&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white)

---

## ✨ Features

- 🤖 AI Fraud Detection (XGBoost + SHAP)
- 💬 Jarvis AI Assistant (Groq LLM, Voice + Text)
- 📄 PDF Document Analysis
- 📊 Real-time Dashboard with auto-refresh
- 🎮 Fraud Simulator
- 🔐 Role-based Login (Admin/User)
- 📋 Audit Log
- 📥 Export Reports (Excel/PDF/CSV)

---

## 🚀 Setup

```bash
# 1. Clone
git clone https://github.com/YOUR-USERNAME/IntelliBank.git
cd IntelliBank

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add GROQ_API_KEY in .env

# 5. Run
streamlit run dashboard.py

🛠️ Tech Stack
Backend: FastAPI, SQLAlchemy, SQLite

Frontend: Streamlit, Plotly

AI/ML: XGBoost, SHAP, scikit-learn

LLM: Groq (Llama 3.3 70B)

Voice: SpeechRecognition, gTTS

📁 Project Structure:

IntelliBank/
├── app/
│   ├── api/          # FastAPI endpoints
│   ├── core/         # Config & DB
│   ├── models/       # SQLAlchemy models
│   ├── ml/           # Fraud detection
│   ├── jarvis/       # AI assistant
│   ├── services/     # PDF analysis
│   └── utils/        # Helpers
├── dashboard.py      # Streamlit UI
├── requirements.txt
└── README.md

👨‍💻 Author
Gotam Kumar

📄 License:

MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.