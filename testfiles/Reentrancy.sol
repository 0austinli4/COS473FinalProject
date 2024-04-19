pragma solidity ^0.8.18;

// SPDX-License-Identifier: UNLICENSED or appropriate license

contract Reentrance {
    mapping (address => uint) userBalance;
   
    function getBalance(address u) public view returns (uint) {
        return userBalance[u];
    }

    function addToBalance() public payable {
        userBalance[msg.sender] = msg.value;
    }   

    function withdrawBalance() public {
        uint balance = userBalance[msg.sender];
        userBalance[msg.sender] = 0;

        // Using require to ensure the call succeeds
        
        require(success, "Failed to send Ether");
    }   

    function withdrawBalance_fixed() public {
        uint amount = userBalance[msg.sender];
        userBalance[msg.sender] = 0;

        // Ensuring the call succeeds
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Failed to send Ether");
    }   

    function withdrawBalance_fixed_2() public {
        uint balance = userBalance[msg.sender];
        userBalance[msg.sender] = 0;

        // Cast msg.sender to payable address
        address payable sender = payable(msg.sender);
        sender.transfer(balance);
    }   
}
