// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  // 1. Get signers
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  // 2. Use parseEther (must come from `ethers.utils`)
  const lockedAmount = ethers.parseEther("0.001");  
  console.log("Locked amount:", lockedAmount.toString());

  // 3. Deploy contract example
  const currentTimestampInSeconds = Math.round(Date.now() / 1000);
  const unlockTime = currentTimestampInSeconds + 60;

  const Lock = await ethers.getContractFactory("Lock");
  const lock = await Lock.deploy(unlockTime, { value: lockedAmount });
  await lock.deployed();

  console.log("Lock deployed to:", lock.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
