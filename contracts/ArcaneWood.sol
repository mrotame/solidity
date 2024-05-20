// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC20/ERC20.sol)

pragma solidity ^0.8.24;

import {ERC20} from "./common/tokens/ERC20.sol";
contract ArcaneWood is ERC20{
   constructor(address[] memory _admins) ERC20("Arcane Wood", "ARW", 18, 0, _admins) {
   }
}