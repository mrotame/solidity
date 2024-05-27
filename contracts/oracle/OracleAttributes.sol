// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;


contract OracleAttributes {
    enum RequestTypes { RANDUINT_SINGLE, RANDUINT_ARRAY }

    mapping(address  => bool) allowedAddresses;

    address callerAccount;
    uint transferNumber;
    uint refoundNumber;

    uint256 currentRequestId;

    mapping (uint requestId => bool) requests;

    mapping (RequestTypes => bytes4) fulfillFunctions;

    mapping (address requester => mapping(RequestTypes requestName => uint costGwei) functionCost) lastCostsPerRequester;
}