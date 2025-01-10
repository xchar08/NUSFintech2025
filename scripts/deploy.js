// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  // Deploy KYCContract
  const KYCFactory = await ethers.getContractFactory("KYCContract");
  const kycInstance = await KYCFactory.deploy();  // returns a Contract
  await kycInstance.waitForDeployment();          // Ethers v6 replaces .deployed()
  const kycAddress = await kycInstance.getAddress();
  console.log("KYCContract deployed to:", kycAddress);

  // Deploy TransactionContract
  const TxFactory = await ethers.getContractFactory("TransactionContract");
  const txInstance = await TxFactory.deploy();    // returns a Contract
  await txInstance.waitForDeployment();
  const txAddress = await txInstance.getAddress();
  console.log("TransactionContract deployed to:", txAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
