require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: {
    compilers: [
      {
        version: "0.8.28"
      }
    ]
  },
  networks: {
    // We won't run a local node, so no "hardhat" or "localhost" needed
    sepolia: {
      url: process.env.INFURA_SEPOLIA_URL || "",
      accounts: [process.env.PRIVATE_KEY].filter(Boolean)
    }
  }
};
