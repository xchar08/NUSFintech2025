import os
import json
from flask import Flask, request, jsonify
from web3 import Web3
from dotenv import load_dotenv
import numpy as np

from ml_engine import FraudDetectionModel

load_dotenv()

app = Flask(__name__)

WEB3_PROVIDER = os.getenv("WEB3_PROVIDER", "https://sepolia.infura.io/v3/YOUR_ID")
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

# Example of loading a contract (if you want to interact with it)
# In practice, you'd copy the contract's "abi" from your Hardhat artifacts
LOCK_CONTRACT_ADDR = os.getenv("LOCK_CONTRACT_ADDR", "0xYourLockAddress")

try:
    with open("LockABI.json", "r") as f:
        lock_abi = json.load(f)
    lock_contract = w3.eth.contract(address=LOCK_CONTRACT_ADDR, abi=lock_abi)
except FileNotFoundError:
    lock_contract = None

model = FraudDetectionModel()

@app.route("/api/score", methods=["POST"])
def score_transaction():
    data = request.json or {}
    features = data.get("features", [0, 0, 0, 0])
    np_features = np.array(features, dtype=float)

    risk_score = model.predict_score(np_features)
    return jsonify({"risk_score": risk_score})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
