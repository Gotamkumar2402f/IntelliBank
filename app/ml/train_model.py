import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from xgboost import XGBClassifier
import joblib
import os
from datetime import datetime, timedelta
import random

def generate_synthetic_data(n_samples=2000):
    """Generate realistic synthetic banking transaction data"""
    data = []
    
    for i in range(n_samples):
        amount = round(random.uniform(500, 200000), 2)
        hour = random.randint(0, 23)
        is_night = 1 if hour < 6 else 0
        txn_type = random.choice(["deposit", "withdrawal", "transfer"])
        
        # Type encoding
        type_deposit = 1 if txn_type == "deposit" else 0
        type_withdrawal = 1 if txn_type == "withdrawal" else 0
        type_transfer = 1 if txn_type == "transfer" else 0
        
        balance = round(random.uniform(1000, 500000), 2)
        amount_to_balance = amount / balance if balance > 0 else 0
        
        # Fraud logic for labels (realistic patterns)
        is_fraud = 0
        if amount > 100000 and is_night:
            is_fraud = 1
        elif amount > 80000 and type_withdrawal and amount_to_balance > 0.6:
            is_fraud = 1
        elif amount > 150000:
            is_fraud = 1
        elif random.random() < 0.03:  # some random fraud
            is_fraud = 1
            
        data.append({
            "amount": amount,
            "hour": hour,
            "is_night": is_night,
            "type_deposit": type_deposit,
            "type_withdrawal": type_withdrawal,
            "type_transfer": type_transfer,
            "balance": balance,
            "amount_to_balance_ratio": round(amount_to_balance, 4),
            "is_fraud": is_fraud
        })
    
    return pd.DataFrame(data)

def train():
    print("Generating synthetic data...")
    df = generate_synthetic_data(2500)
    
    print(f"Total samples: {len(df)}")
    print(f"Fraud samples: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.1f}%)")
    
    features = ["amount", "hour", "is_night", "type_deposit", 
                "type_withdrawal", "type_transfer", "balance", "amount_to_balance_ratio"]
    
    X = df[features]
    y = df["is_fraud"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("\nTraining XGBoost model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        scale_pos_weight=10,  # handle imbalance
        random_state=42,
        eval_metric="logloss"
    )
    
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n===== Model Evaluation =====")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC:  {roc_auc_score(y_test, y_prob):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Safe", "Fraud"]))
    
    # Save model
    os.makedirs("app/ml/models", exist_ok=True)
    model_path = "app/ml/models/fraud_xgb_model.joblib"
    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Feature importance
    importance = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    print("\nFeature Importance:")
    print(importance.to_string(index=False))
    
    return model

if __name__ == "__main__":
    train()