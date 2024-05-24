// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC20/ERC20.sol)

pragma solidity ^0.8.24;

import {ArcaneResource} from "../common/tokens/arcane_resource.sol";
   

contract ArcaneWood is ArcaneResource{
    constructor(address[] memory _admins) ArcaneResource("Arcane Wood", "ARW", 18, 0, _admins) {
   }
}