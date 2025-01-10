import os
import json
from flask import Flask, request, jsonify
from web3 import Web3
from dotenv import load_dotenv
import numpy as np

from ml_engine import FraudDetectionModel

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

#######################################
# 1. Configure Web3
#######################################
WEB3_PROVIDER = os.getenv("WEB3_PROVIDER", "https://sepolia.infura.io/v3/YOUR_ID")
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

# The deployed TransactionContract address (from Hardhat logs)
TX_CONTRACT_ADDR = os.getenv("TX_CONTRACT_ADDR", "0xYourTransactionContractAddress")

# Load the TransactionContract ABI from a JSON file
# Replace "TransactionContractABI.json" with the name/ path to your ABI file
try:
    with open("TransactionContractABI.json", "r") as f:
        tx_abi = json.load(f)
    transaction_contract = w3.eth.contract(address=TX_CONTRACT_ADDR, abi=tx_abi)
except FileNotFoundError:
    transaction_contract = None
    print("[Warning] TransactionContract ABI file not found. On-chain calls may fail.")

#######################################
# 2. Initialize ML Model
#######################################
# You can specify your real model path if you have "fraud_model.joblib"
model = FraudDetectionModel("fraud_model.joblib")

#######################################
# 3. Define Flask Routes
#######################################

@app.route("/api/transaction", methods=["POST"])
def handle_transaction():
    """
    Expects JSON:
    {
      "amount": 100,
      "receiver": "0xRecipientAddress...",
      "features": [5000, 2, 1, 0]
    }

    1) Compute ML risk score using 'features'
    2) (Optional) Interact with the transaction_contract to record data on-chain
    3) Return the risk score or transaction hash, as needed
    """
    data = request.json or {}
    amount = data.get("amount", 0)
    receiver = data.get("receiver", "")
    features = data.get("features", [0, 0, 0, 0])

    # Convert to numpy array for the ML model
    np_features = np.array(features, dtype=float)
    risk_score = model.predict_score(np_features)

    # If you only need the ML score, just return it here:
    # return jsonify({"risk_score": risk_score})

    # Example: If you want to also store this info on-chain, you'll need:
    # 1) A private key
    # 2) A contract function call (e.g., recordTransaction)
    # 3) Enough test ETH in that private key's address for gas
    # 
    # (Below is pseudo-code; adapt as needed.)

    return jsonify({
        "status": "success",
        "risk_score": risk_score,
        # "transactionHash": "...",
        # "blockNumber": ...
    })

#######################################
# 4. Run the Flask App
#######################################
if __name__ == "__main__":
    app.run(port=5000, debug=True)
