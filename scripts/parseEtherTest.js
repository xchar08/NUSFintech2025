const { ethers } = require("hardhat");

async function main() {
  console.log("Testing parseEther...");

  console.log("ethers:", ethers);  // Should be an object
  console.log("ethers.utils:", ethers.utils);  // Should be an object

  const amount = ethers.parseEther("0.001");
  console.log("Parsed:", amount.toString());
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
