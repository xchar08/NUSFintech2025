import os
import json
import numpy as np
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from web3 import Web3
import hashlib

from ml_engine import FraudDetectionModel

load_dotenv()

app = Flask(__name__)

#######################################
# 1. Web3 Setup
#######################################
WEB3_PROVIDER = os.getenv("WEB3_PROVIDER", "https://sepolia.infura.io/v3/YOUR_ID")
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
TX_CONTRACT_ADDR = os.getenv("TX_CONTRACT_ADDR", "")
KYC_CONTRACT_ADDR = os.getenv("KYC_CONTRACT_ADDR", "")
MODEL_PATH = os.getenv("MODEL_PATH", "fraud_model.joblib")

if not w3.is_connected():
    print("[Error] Could not connect to Web3 provider. Check WEB3_PROVIDER.")
    exit(1)

# Load the ABIs
try:
    with open("TransactionContractABI.json", "r") as f:
        tx_abi = json.load(f)
    transaction_contract = w3.eth.contract(address=TX_CONTRACT_ADDR, abi=tx_abi)
except FileNotFoundError:
    print("[Error] TransactionContractABI.json not found.")
    transaction_contract = None

try:
    with open("KYCContractABI.json", "r") as f:
        kyc_abi = json.load(f)
    kyc_contract = w3.eth.contract(address=KYC_CONTRACT_ADDR, abi=kyc_abi)
except FileNotFoundError:
    print("[Error] KYCContractABI.json not found.")
    kyc_contract = None

if not PRIVATE_KEY:
    print("[Warning] PRIVATE_KEY not set. Transactions may fail if signing is needed.")

#######################################
# 2. ML Model
#######################################
model = FraudDetectionModel(MODEL_PATH)

#######################################
# 3. Helper Functions
#######################################
def sign_and_send(tx_build, private_key):
    """
    Utility to sign and send a transaction, then wait for receipt.
    """
    account = w3.eth.account.from_key(private_key)
    sender = account.address
    nonce = w3.eth.get_transaction_count(sender)

    tx_build['nonce'] = nonce
    tx_build['from'] = sender
    if 'gas' not in tx_build:
        tx_build['gas'] = 300000
    # Removed gasPrice assignment due to unknown kwargs error

    signed_tx = w3.eth.account.sign_transaction(tx_build, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash, receipt

#######################################
# 4. AML Watchlist Endpoints
#######################################
@app.route("/api/flag-address", methods=["POST"])
def flag_address():
    # Minimal implementation for testing
    # Replace this with actual logic to flag/unflag addresses on-chain as needed
    return jsonify({"status": "dummy success for flag-address"}), 200

#######################################
# 5. KYC Endpoint
#######################################
@app.route("/api/kyc", methods=["POST"])
def update_kyc():
    # Minimal implementation for testing
    # Replace this with actual logic to update KYC information on-chain as needed
    return jsonify({"status": "dummy success for update-kyc"}), 200

#######################################
# 6. Transaction Endpoint (with checksum handling)
#######################################
@app.route("/api/transaction", methods=["POST"])
def handle_transaction():
    """
    Expects JSON:
    {
      "amount": 200,
      "receiver": "0xReceiverAddress...",
      "features": [5000, 2, 1, 0]
    }
    """
    if not transaction_contract:
        return jsonify({"error": "Transaction contract not configured"}), 500
    if not PRIVATE_KEY:
        return jsonify({"error": "No PRIVATE_KEY set"}), 400

    data = request.json or {}
    amount = data.get("amount", 0)
    receiver = data.get("receiver", "")
    features = data.get("features", [])

    # Convert features to numpy array for ML
    try:
        np_features = np.array(features, dtype=float)
    except ValueError:
        return jsonify({"error": "Invalid features array"}), 400

    # Generate risk score
    risk_score = model.predict_score(np_features)

    # Convert receiver address to checksummed address
    try:
        receiver = w3.to_checksum_address(receiver)
    except Exception as e:
        return jsonify({"error": f"Invalid receiver address: {e}"}), 400

    # Build transaction for recordTransaction(receiver, amount, risk_score)
    try:
        tx_build = transaction_contract.functions.recordTransaction(
            receiver,
            int(amount),
            int(risk_score)
        ).build_transaction({})
        tx_hash, receipt = sign_and_send(tx_build, PRIVATE_KEY)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "status": "success",
        "transactionHash": tx_hash.hex(),
        "riskScore": risk_score,
        "blockNumber": receipt.blockNumber
    })

#######################################
# 7. Run Flask
#######################################
if __name__ == "__main__":
    app.run(port=5000, debug=True)
