import numpy as np
import joblib
import os
from datetime import datetime

class FraudDetector:
    """
    Hybrid Fraud Detector:
    - Primary: Trained XGBoost ML model
    - Fallback: Rule-based scoring
    """

    def __init__(self):
        self.model = None
        self.model_path = "app/ml/models/fraud_xgb_model.joblib"
        self.high_amount_threshold = 100000
        self.suspicious_hours = list(range(0, 6))
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print("XGBoost fraud model loaded successfully.")
            except Exception as e:
                print(f"Could not load ML model: {e}")
                self.model = None
        else:
            print("ML model not found. Using rule-based detection only.")

    def _prepare_features(self, amount, transaction_type, account_balance=None, hour=None):
        if hour is None:
            hour = datetime.now().hour

        is_night = 1 if hour < 6 else 0
        type_deposit = 1 if transaction_type == "deposit" else 0
        type_withdrawal = 1 if transaction_type == "withdrawal" else 0
        type_transfer = 1 if transaction_type == "transfer" else 0

        balance = account_balance if account_balance is not None else 50000
        amount_to_balance_ratio = amount / balance if balance > 0 else 0

        # Order must match training features
        features = np.array([[
            amount,
            hour,
            is_night,
            type_deposit,
            type_withdrawal,
            type_transfer,
            balance,
            amount_to_balance_ratio
        ]])
        return features

    def calculate_fraud_score(self, amount: float, transaction_type: str,
                               account_balance: float = None,
                               hour: int = None) -> float:
        """
        Returns fraud score between 0 and 1
        """
        # Try ML model first
        if self.model is not None:
            try:
                features = self._prepare_features(amount, transaction_type, account_balance, hour)
                proba = self.model.predict_proba(features)[0][1]  # probability of fraud
                return round(float(proba), 3)
            except Exception as e:
                print(f"ML prediction failed, falling back to rules: {e}")

        # Fallback: Rule-based
        return self._rule_based_score(amount, transaction_type, account_balance, hour)

    def _rule_based_score(self, amount, transaction_type, account_balance=None, hour=None):
        score = 0.0
        if hour is None:
            hour = datetime.now().hour

        if amount >= self.high_amount_threshold:
            score += 0.4
        elif amount >= 50000:
            score += 0.25

        if hour in self.suspicious_hours:
            score += 0.2

        if transaction_type == "withdrawal" and account_balance:
            if amount > account_balance * 0.7:
                score += 0.3

        if transaction_type == "transfer" and amount >= 80000:
            score += 0.25

        return min(round(score, 3), 1.0)

    def is_fraud(self, score: float, threshold: float = 0.5) -> bool:
        return score >= threshold