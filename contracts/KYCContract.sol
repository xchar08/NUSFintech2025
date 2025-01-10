// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * @title KYCContract
 * @dev Stores hashed references to user identity docs, plus a "verified" flag.
 */
contract KYCContract {
    struct KYCRecord {
        bytes32 docHash;    // keccak256 hash of user's identity doc
        bool verified;
        uint256 timestamp;
    }

    mapping(address => KYCRecord) public kycRecords;

    event KYCUpdated(address indexed user, bytes32 docHash, bool verified, uint256 timestamp);

    /**
     * @dev Allows a user to add/update their KYC data (hashed docs).
     * @param _docHash keccak256 hash of user doc.
     * @param _verified whether KYC is verified by some off-chain process.
     */
    function updateKYC(bytes32 _docHash, bool _verified) public {
        kycRecords[msg.sender] = KYCRecord({
            docHash: _docHash,
            verified: _verified,
            timestamp: block.timestamp
        });

        emit KYCUpdated(msg.sender, _docHash, _verified, block.timestamp);
    }

    /**
     * @dev Retrieves a KYC record.
     * @param _user The user address to look up.
     */
    function getKYC(address _user) public view returns (bytes32 docHash, bool verified, uint256 timestamp) {
        KYCRecord memory record = kycRecords[_user];
        return (record.docHash, record.verified, record.timestamp);
    }
}
