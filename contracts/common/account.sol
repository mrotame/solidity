// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

struct AccountStruct {
    address account_address;
    
    uint last_updated;
    uint balance;

    uint mining_power_upgrade;
    uint selling_time_upgrade;
}

library Account {
    function new_account(address addr) public view returns(AccountStruct memory){
        require(addr == address(0), "User already registered");
        AccountStruct memory acc = AccountStruct(addr, block.timestamp, 0, 0, 0);
        return acc;
    }

    
}