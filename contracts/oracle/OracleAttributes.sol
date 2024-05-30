// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;


contract OracleAttributes {
    uint256 baseGasWeiFee = 100000 * 1 gwei;
    enum RequestTypes { RANDUINT_SINGLE, RANDUINT_ARRAY }
    address callerAccount;
    uint128 currentRequestId;

    mapping(address  => bool) allowedAddresses;
    mapping (uint requestId => address requester) public requests;
}