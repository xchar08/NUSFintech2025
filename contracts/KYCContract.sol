// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract KYCContract {
    struct KYCRecord {
        bytes32 userHash;    // hashed user data (e.g., passport, SSN)
        bool verified;
        uint256 verificationTimestamp;
    }

    mapping(address => KYCRecord) public kycRecords;

    event KYCUpdated(address indexed user, bool verified, uint256 timestamp);

    function updateKYC(bytes32 _userHash, bool _verified) public {
        KYCRecord storage record = kycRecords[msg.sender];
        record.userHash = _userHash;
        record.verified = _verified;
        record.verificationTimestamp = block.timestamp;

        emit KYCUpdated(msg.sender, _verified, block.timestamp);
    }
}
