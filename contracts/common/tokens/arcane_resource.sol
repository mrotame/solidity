// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC20/ERC20.sol)

pragma solidity ^0.8.24;

import {ERC20} from "./ERC20.sol";
   

contract ArcaneResource is ERC20{
    uint private tax_fee_percent = 5;
    address private tax_address;
   
    constructor(string memory _token_name, string memory _token_symbol, uint8 _decimals, uint _max_supply, address[] memory _admins) ERC20(_token_name, _token_symbol, _decimals, _max_supply, _admins) {
        tax_address = contractOwner;
   }

    function update_tax_address(address _new_addr) public isOwner(_new_addr){
        tax_address = _new_addr;
    }

    function transferFrom(address _from, address _to, uint256 _value) override public returns (bool success) {
        uint tax_amount = (_value * tax_fee_percent) / 100;
        uint value_without_tax = _value - tax_amount;

        if (!admin_addrs[msg.sender]) {
            super.transferFrom(_from, tax_address, tax_amount);
            return super.transferFrom(_from, _to, value_without_tax);
        }
        return super.transferFrom(_from, _to, _value);
    }
}