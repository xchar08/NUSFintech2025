import joblib
import numpy as np

class FraudDetectionModel:
    def __init__(self, model_path="fraud_model.joblib"):
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            print(f"[Warning] {model_path} not found. Using dummy model.")
            self.model = None

    def predict_score(self, features: np.ndarray) -> int:
        if self.model is None:
            return 500
        fraud_prob = self.model.predict_proba(features.reshape(1, -1))[0][1]
        return int(fraud_prob * 1000)
