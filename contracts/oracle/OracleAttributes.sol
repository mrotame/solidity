// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;


contract OracleAttributes {
    uint256 baseGasWeiFee = 100000 * 1 gwei;
    uint256 currentRequestId;
    enum RequestTypes { RANDUINT_SINGLE, RANDUINT_ARRAY, MINT_CHARACTER, MINT_LAND }
    address callerAccount;
    
    mapping(address  => bool) allowedAddresses;
    mapping (uint requestId => address requester) public requests;
}