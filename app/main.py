from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.api import accounts, transactions, fraud
from app.api import accounts, transactions, fraud, jarvis
from app.api import accounts, transactions, fraud, jarvis, pdf_api

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Banking System with Conversational AI & Fraud Detection",
    version="1.0.0"
)

app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(fraud.router)
app.include_router(jarvis.router) 
app.include_router(pdf_api.router)    

@app.get("/")
def root():
    return {
        "message": "Welcome to IntelliBank API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}