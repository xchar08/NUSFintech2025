# python/ml_engine.py
import joblib
import numpy as np

class FraudDetectionModel:
    def __init__(self, model_path: str = "fraud_model.joblib"):
        """
        Attempt to load a pre-trained ML model (RandomForest, XGBoost, etc.).
        """
        try:
            self.model = joblib.load(model_path)
            print(f"[Info] Loaded model from {model_path}")
        except FileNotFoundError:
            print(f"[Warning] Model file {model_path} not found. Using dummy logic.")
            self.model = None

    def predict_score(self, features: np.ndarray) -> int:
        """
        Return a risk score [0..1000].
        If self.model is None, we default to a dummy score of 500.
        """
        if self.model is None:
            # fallback
            return 500
        else:
            # Assume model has predict_proba(...) for binary classification
            prob = self.model.predict_proba(features.reshape(1, -1))[0][1]
            return int(prob * 1000)
