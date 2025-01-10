// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * @title TransactionContract
 * @dev Stores transactions with ML risk scores. Also includes AML watchlist logic.
 */
contract TransactionContract {
    struct TransactionInfo {
        address sender;
        address receiver;
        uint256 amount;
        uint256 timestamp;
        uint256 mlRiskScore;
    }

    TransactionInfo[] public transactions;

    mapping(address => bool) public flaggedAddresses; // watchlist

    address public owner;

    event TransactionRecorded(
        address indexed sender,
        address indexed receiver,
        uint256 amount,
        uint256 timestamp,
        uint256 mlRiskScore
    );

    event AddressFlagged(address indexed addr, bool flagged);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    /**
     * @dev Adds or removes an address from the AML watchlist.
     * @param _addr The address to flag/unflag.
     * @param _flag true if flagged, false if unflagging.
     */
    function setFlaggedAddress(address _addr, bool _flag) external onlyOwner {
        flaggedAddresses[_addr] = _flag;
        emit AddressFlagged(_addr, _flag);
    }

    /**
     * @dev Records a transaction along with an ML-generated risk score.
     * @param _receiver The address receiving the funds.
     * @param _amount The numeric amount (for reference).
     * @param _mlRiskScore The ML risk score (0..1000).
     */
    function recordTransaction(
        address _receiver,
        uint256 _amount,
        uint256 _mlRiskScore
    ) public {
        // AML check: ensure neither sender nor receiver is flagged
        require(!flaggedAddresses[msg.sender], "Sender is flagged");
        require(!flaggedAddresses[_receiver], "Receiver is flagged");

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

    /**
     * @dev Returns the total number of transactions recorded.
     */
    function getTransactionCount() public view returns (uint256) {
        return transactions.length;
    }

    /**
     * @dev Retrieves a transaction by index.
     */
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
