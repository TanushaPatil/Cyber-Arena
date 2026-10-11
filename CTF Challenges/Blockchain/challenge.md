# The Vulnerable Vault

## Scenario

A decentralized vault is responsible for holding ETH deposits.

Users can deposit funds and later withdraw their balance.

Unfortunately, the vault was written without properly protecting
its withdrawal logic.

Your objective is to analyze the smart contract and exploit the
vulnerability to completely drain the vault.

## Objective

1. Deploy the vulnerable vault.
2. Understand the deposit and withdrawal logic.
3. Identify the unsafe external call.
4. Deploy the attacker contract.
5. Perform the reentrancy attack.
6. Drain the vault completely.
7. Verify that the vault has been compromised.

## Vulnerability

The withdrawal function sends ETH to the caller before updating
the caller's balance.

This creates a reentrancy condition.

A malicious contract can use its receive() function to call
withdraw() again before the original withdrawal finishes.

## Recommended Tools

- Remix IDE
- MetaMask
- Solidity
- Ethereum Virtual Machine

## Flag

After successfully draining the vault, submit the flag through
the Cyber Arena submission panel.