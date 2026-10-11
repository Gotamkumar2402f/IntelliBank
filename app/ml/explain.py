import shap
import numpy as np
import joblib
import os
from datetime import datetime

_explainer = None
_model = None

MODEL_PATH = "app/ml/models/fraud_xgb_model.joblib"


def _load():
    """Load model and create SHAP explainer."""
    global _explainer, _model
    if _explainer is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
        _explainer = shap.TreeExplainer(_model)
    return _explainer


def explain_transaction(amount, transaction_type, account_balance=50000, hour=None):
    """
    Explain why a transaction was flagged using SHAP values.

    Returns list of dicts:
        [{"feature": "Amount", "value": 80000, "impact": 0.35, "direction": "increases"}, ...]
    """
    if hour is None:
        hour = datetime.now().hour

    is_night = 1 if hour < 6 else 0
    type_deposit = 1 if transaction_type == "deposit" else 0
    type_withdrawal = 1 if transaction_type == "withdrawal" else 0
    type_transfer = 1 if transaction_type == "transfer" else 0
    balance = account_balance if account_balance else 50000
    amount_to_balance_ratio = amount / balance if balance > 0 else 0

    X = np.array([[
        amount, hour, is_night,
        type_deposit, type_withdrawal, type_transfer,
        balance, amount_to_balance_ratio
    ]])

    feature_names = [
        "Amount", "Hour", "Is Night",
        "Type: Deposit", "Type: Withdrawal", "Type: Transfer",
        "Account Balance", "Amount/Balance Ratio"
    ]

    try:
        explainer = _load()
        shap_values = explainer.shap_values(X)[0]
    except Exception as e:
        return [{"feature": "Error", "value": str(e), "impact": 0.0, "direction": "unknown"}]

    contributions = []
    for name, val, impact in zip(feature_names, X[0], shap_values):
        contributions.append({
            "feature": name,
            "value": float(val),
            "impact": float(impact),
            "direction": "increases" if impact > 0 else "decreases",
        })

    contributions.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return contributions