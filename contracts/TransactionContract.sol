// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract TransactionContract {
    struct TransactionInfo {
        address sender;
        address receiver;
        uint256 amount;
        uint256 timestamp;
        uint256 mlRiskScore; // Off-chain ML score stored on-chain
    }

    TransactionInfo[] public transactions;

    event TransactionRecorded(
        address indexed sender,
        address indexed receiver,
        uint256 amount,
        uint256 timestamp,
        uint256 mlRiskScore
    );

    function recordTransaction(
        address _receiver,
        uint256 _amount,
        uint256 _mlRiskScore
    ) public {
        TransactionInfo memory newTx = TransactionInfo({
            sender: msg.sender,
            receiver: _receiver,
            amount: _amount,
            timestamp: block.timestamp,
            mlRiskScore: _mlRiskScore
        });

        transactions.push(newTx);

        emit TransactionRecorded(
            msg.sender,
            _receiver,
            _amount,
            block.timestamp,
            _mlRiskScore
        );
    }

    function getTransactionCount() public view returns (uint256) {
        return transactions.length;
    }

    function getTransaction(uint256 _index)
        public
        view
        returns (
            address sender,
            address receiver,
            uint256 amount,
            uint256 timestamp,
            uint256 mlRiskScore
        )
    {
        require(_index < transactions.length, "Invalid index");
        TransactionInfo storage txn = transactions[_index];
        return (
            txn.sender,
            txn.receiver,
            txn.amount,
            txn.timestamp,
            txn.mlRiskScore
        );
    }
}
