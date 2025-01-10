# quick_train.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

X = np.random.rand(1000, 4)
y = np.random.randint(0, 2, 1000)
model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "fraud_model.joblib")
print("Dummy model saved.")
